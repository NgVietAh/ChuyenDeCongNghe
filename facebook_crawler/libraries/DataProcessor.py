"""
DataProcessor - Utility library for processing and cleaning crawled data.
"""

import re
from datetime import datetime


class DataProcessor:
    """Robot Framework library for processing crawled Facebook data."""

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def clean_post_content(self, raw_content):
        """Clean and normalize post content text.

        Args:
            raw_content: Raw text extracted from Facebook post.

        Returns:
            str: Cleaned post content.
        """
        if not raw_content:
            return ""

        content = raw_content.strip()
        content = re.sub(r"\s+", " ", content)
        content = re.sub(r"\n{3,}", "\n\n", content)

        # Remove common Facebook UI text artifacts
        ui_artifacts = [
            "See more",
            "Xem thêm",
            "See less",
            "Thu gọn",
            "Like",
            "Comment",
            "Share",
            "Thích",
            "Bình luận",
            "Chia sẻ",
        ]
        for artifact in ui_artifacts:
            content = content.replace(artifact, "").strip()

        return content

    def parse_facebook_time(self, time_text):
        """Parse Facebook's relative time format to a readable format.

        Args:
            time_text: Time text from Facebook (e.g., '2 hours ago', '3d', 'Yesterday').

        Returns:
            str: Parsed time string.
        """
        if not time_text:
            return ""

        time_text = time_text.strip()

        # Already a date format
        date_patterns = [
            r"\d{1,2}\s+tháng\s+\d{1,2}",
            r"\d{1,2}/\d{1,2}/\d{4}",
            r"\w+\s+\d{1,2},?\s+\d{4}",
            r"\d{1,2}\s+\w+\s+\d{4}",
        ]
        for pattern in date_patterns:
            if re.search(pattern, time_text):
                return time_text

        return time_text

    def filter_duplicate_urls(self, url_list):
        """Remove duplicate URLs from a list.

        Args:
            url_list: List of URLs (or comma-separated string).

        Returns:
            list: Deduplicated list of URLs.
        """
        if isinstance(url_list, str):
            url_list = [u.strip() for u in url_list.split(",") if u.strip()]

        seen = set()
        unique = []
        for url in url_list:
            normalized = url.split("?")[0]
            if normalized not in seen:
                seen.add(normalized)
                unique.append(url)
        return unique

    def create_post_summary(self, posts):
        """Create a summary of crawled posts.

        Args:
            posts: List of post dictionaries.

        Returns:
            dict: Summary information.
        """
        total = len(posts)
        with_images = sum(1 for p in posts if p.get("image_urls"))
        with_content = sum(1 for p in posts if p.get("content"))
        total_images = sum(len(p.get("image_urls", [])) for p in posts)

        return {
            "total_posts": total,
            "posts_with_content": with_content,
            "posts_with_images": with_images,
            "total_images": total_images,
            "generated_at": datetime.now().isoformat(),
        }

    def truncate_content(self, content, max_length=200):
        """Truncate content to a maximum length for display.

        Args:
            content: Text content to truncate.
            max_length: Maximum length (default: 200).

        Returns:
            str: Truncated content with ellipsis if needed.
        """
        if not content or len(content) <= max_length:
            return content or ""
        return content[:max_length] + "..."
