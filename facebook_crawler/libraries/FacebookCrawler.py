"""
FacebookCrawler - Python library for Robot Framework
Handles data extraction, image downloading, and post processing from Facebook.
"""

import json
import csv
import os
import re
import time
import hashlib
from datetime import datetime
from urllib.parse import urlparse, urljoin

import requests
import yaml


class FacebookCrawler:
    """Robot Framework library for crawling Facebook posts."""

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self.posts = []
        self.config = {}
        self.session = requests.Session()
        self.output_dir = "output"
        self.images_dir = "downloaded_images"

    def load_config(self, config_path):
        """Load configuration from YAML file.

        Args:
            config_path: Path to the YAML configuration file.

        Returns:
            dict: The loaded configuration.
        """
        # Try local config first, fall back to default
        local_config = config_path.replace(".yaml", ".local.yaml")
        if os.path.exists(local_config):
            config_path = local_config

        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        self.output_dir = self.config.get("output", {}).get("output_dir", "output")
        self.images_dir = self.config.get("output", {}).get(
            "images_dir", "downloaded_images"
        )

        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)

        return self.config

    def get_config_value(self, section, key):
        """Get a specific configuration value.

        Args:
            section: The configuration section (e.g., 'facebook', 'crawler').
            key: The configuration key within the section.

        Returns:
            The configuration value.
        """
        return self.config.get(section, {}).get(key, "")

    def add_post(self, content, post_time, image_urls, post_url=""):
        """Add a crawled post to the collection.

        Args:
            content: The text content of the post.
            post_time: The timestamp of the post.
            image_urls: Comma-separated string of image URLs or a list.
            post_url: URL of the post.
        """
        if isinstance(image_urls, str):
            image_urls = [url.strip() for url in image_urls.split(",") if url.strip()]

        post = {
            "id": len(self.posts) + 1,
            "content": content.strip() if content else "",
            "post_time": post_time.strip() if post_time else "",
            "post_url": post_url.strip() if post_url else "",
            "image_urls": image_urls,
            "downloaded_images": [],
            "crawled_at": datetime.now().isoformat(),
        }

        self.posts.append(post)
        return post

    def download_image(self, image_url, post_id):
        """Download an image from URL and save locally.

        Args:
            image_url: URL of the image to download.
            post_id: ID of the post this image belongs to.

        Returns:
            str: Local path to the downloaded image, or empty string on failure.
        """
        if not image_url or image_url == "NONE":
            return ""

        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
            }

            response = self.session.get(
                image_url, headers=headers, timeout=30, stream=True
            )
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")
            ext = self._get_image_extension(content_type, image_url)

            url_hash = hashlib.md5(image_url.encode()).hexdigest()[:10]
            filename = f"post_{post_id}_{url_hash}{ext}"
            filepath = os.path.join(self.images_dir, filename)

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return filepath
        except (requests.RequestException, OSError) as e:
            print(f"Failed to download image {image_url}: {e}")
            return ""

    def download_all_images(self):
        """Download all images from all crawled posts.

        Returns:
            int: Total number of images downloaded.
        """
        total_downloaded = 0
        for post in self.posts:
            for img_url in post["image_urls"]:
                local_path = self.download_image(img_url, post["id"])
                if local_path:
                    post["downloaded_images"].append(local_path)
                    total_downloaded += 1
                time.sleep(0.5)
        return total_downloaded

    def save_results_to_json(self, filename=""):
        """Save crawled posts to a JSON file.

        Args:
            filename: Output filename (without extension).

        Returns:
            str: Path to the saved JSON file.
        """
        if not filename:
            filename = self.config.get("output", {}).get(
                "output_filename", "facebook_posts"
            )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.output_dir, f"{filename}_{timestamp}.json")

        output_data = {
            "crawl_info": {
                "total_posts": len(self.posts),
                "crawled_at": datetime.now().isoformat(),
                "profile_url": self.config.get("facebook", {}).get("profile_url", ""),
            },
            "posts": self.posts,
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        return filepath

    def save_results_to_csv(self, filename=""):
        """Save crawled posts to a CSV file.

        Args:
            filename: Output filename (without extension).

        Returns:
            str: Path to the saved CSV file.
        """
        if not filename:
            filename = self.config.get("output", {}).get(
                "output_filename", "facebook_posts"
            )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.output_dir, f"{filename}_{timestamp}.csv")

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "ID",
                    "Content",
                    "Post Time",
                    "Post URL",
                    "Image URLs",
                    "Downloaded Images",
                    "Crawled At",
                ]
            )

            for post in self.posts:
                writer.writerow(
                    [
                        post["id"],
                        post["content"],
                        post["post_time"],
                        post["post_url"],
                        " | ".join(post["image_urls"]),
                        " | ".join(post["downloaded_images"]),
                        post["crawled_at"],
                    ]
                )

        return filepath

    def save_results(self):
        """Save results in the configured format.

        Returns:
            str: Path to the saved output file.
        """
        output_format = self.config.get("output", {}).get("output_format", "json")
        if output_format == "csv":
            return self.save_results_to_csv()
        return self.save_results_to_json()

    def get_total_posts(self):
        """Get the total number of crawled posts.

        Returns:
            int: Number of posts crawled.
        """
        return len(self.posts)

    def get_posts(self):
        """Get all crawled posts.

        Returns:
            list: List of post dictionaries.
        """
        return self.posts

    def clear_posts(self):
        """Clear all crawled posts."""
        self.posts = []

    def extract_image_urls_from_elements(self, elements_text):
        """Extract image URLs from a string containing element attributes.

        Args:
            elements_text: String containing image element src attributes.

        Returns:
            list: List of image URLs.
        """
        urls = []
        url_pattern = re.compile(r'https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|gif|webp)[^\s"\'<>]*', re.IGNORECASE)
        found = url_pattern.findall(elements_text)
        for url in found:
            if "emoji" not in url.lower() and "icon" not in url.lower():
                urls.append(url)
        return urls

    def should_download_images(self):
        """Check if image downloading is enabled in config.

        Returns:
            bool: True if images should be downloaded.
        """
        return self.config.get("output", {}).get("download_images", True)

    def get_max_posts(self):
        """Get the maximum number of posts to crawl.

        Returns:
            int: Maximum posts count (0 = unlimited).
        """
        return self.config.get("crawler", {}).get("max_posts", 20)

    def is_valid_post_content(self, content):
        """Check if the extracted content is valid post content.

        Args:
            content: The extracted text content.

        Returns:
            bool: True if content is valid.
        """
        if not content or not content.strip():
            return False
        if len(content.strip()) < 2:
            return False
        return True

    def _get_image_extension(self, content_type, url):
        """Determine image file extension from content type or URL.

        Args:
            content_type: HTTP Content-Type header value.
            url: The image URL.

        Returns:
            str: File extension including the dot.
        """
        type_map = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/gif": ".gif",
            "image/webp": ".webp",
        }

        for mime, ext in type_map.items():
            if mime in content_type:
                return ext

        parsed = urlparse(url)
        path = parsed.path.lower()
        for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
            if ext in path:
                return ext

        return ".jpg"
