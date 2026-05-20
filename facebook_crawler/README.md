# Facebook Personal Post Crawler

Chương trình crawl dữ liệu từ bài post cá nhân Facebook sử dụng **Robot Framework** và **SeleniumLibrary**.

## Tính năng

- Đăng nhập tự động vào Facebook
- Truy cập trang cá nhân từ link user
- Crawl từng bài post với:
  - **Nội dung bài viết** (text content)
  - **Thời gian đăng** (timestamp)
  - **Link ảnh** (image URLs)
  - **Link bài viết** (post permalink)
- Tự động scroll để tải thêm bài viết
- Tải ảnh về máy (tùy chọn)
- Xuất kết quả ra file **JSON** hoặc **CSV**
- Hỗ trợ chế độ headless (chạy không hiển thị trình duyệt)

## Cấu trúc dự án

```
facebook_crawler/
├── README.md                          # Hướng dẫn sử dụng
├── requirements.txt                   # Dependencies
├── run_crawler.sh                     # Script chạy nhanh
├── config/
│   ├── config.yaml                    # Cấu hình mặc định
│   ├── config.local.yaml              # Cấu hình cá nhân (không commit)
│   └── .gitignore
├── resources/
│   ├── variables.resource             # Biến và locators
│   └── facebook_keywords.resource     # Custom keywords
├── libraries/
│   ├── __init__.py
│   ├── FacebookCrawler.py             # Thư viện chính xử lý crawl
│   └── DataProcessor.py              # Xử lý và làm sạch dữ liệu
├── tasks/
│   └── crawl_facebook_posts.robot     # Task chính
├── output/                            # Kết quả crawl (JSON/CSV)
└── downloaded_images/                 # Ảnh đã tải về
```

## Yêu cầu hệ thống

- Python >= 3.9
- Google Chrome browser
- ChromeDriver (tự động cài đặt qua webdriver-manager)

## Cài đặt

### 1. Cài đặt dependencies

```bash
cd facebook_crawler
pip install -r requirements.txt
```

### 2. Cấu hình

Copy file config mẫu và điền thông tin:

```bash
cp config/config.yaml config/config.local.yaml
```

Chỉnh sửa `config/config.local.yaml`:

```yaml
facebook:
  email: "your_email@example.com"
  password: "your_password"
  profile_url: "https://www.facebook.com/target_username"

crawler:
  max_posts: 20           # Số bài post tối đa cần crawl
  scroll_pause_time: 3    # Thời gian chờ giữa các lần scroll (giây)
  headless: false         # true = chạy ẩn trình duyệt

output:
  output_format: "json"   # json hoặc csv
  download_images: true   # Tải ảnh về hay chỉ lưu link
```

## Sử dụng

### Cách 1: Dùng script chạy nhanh

```bash
chmod +x run_crawler.sh

# Cú pháp: ./run_crawler.sh <email> <password> <profile_url> [max_posts] [headless]
./run_crawler.sh "email@example.com" "password" "https://www.facebook.com/username" 20 false
```

### Cách 2: Chạy trực tiếp bằng Robot Framework

```bash
# Truyền tham số qua command line
robot \
    --variable EMAIL:"email@example.com" \
    --variable PASSWORD:"password" \
    --variable PROFILE_URL:"https://www.facebook.com/username" \
    --variable MAX_POSTS:20 \
    --variable HEADLESS:false \
    --outputdir output \
    tasks/crawl_facebook_posts.robot
```

### Cách 3: Sử dụng file config

Sau khi đã cấu hình `config/config.local.yaml`:

```bash
robot --outputdir output tasks/crawl_facebook_posts.robot
```

## Kết quả đầu ra

### JSON Output

```json
{
  "crawl_info": {
    "total_posts": 15,
    "crawled_at": "2024-01-15T10:30:00",
    "profile_url": "https://www.facebook.com/username"
  },
  "posts": [
    {
      "id": 1,
      "content": "Nội dung bài viết...",
      "post_time": "2 giờ trước",
      "post_url": "https://www.facebook.com/username/posts/123",
      "image_urls": [
        "https://scontent.xx.fbcdn.net/v/t1.xxx/image.jpg"
      ],
      "downloaded_images": [
        "downloaded_images/post_1_abc123.jpg"
      ],
      "crawled_at": "2024-01-15T10:30:00"
    }
  ]
}
```

### CSV Output

| ID | Content | Post Time | Post URL | Image URLs | Downloaded Images | Crawled At |
|----|---------|-----------|----------|------------|-------------------|------------|
| 1  | Nội dung... | 2 giờ trước | https://... | https://... | path/to/img.jpg | 2024-01-15 |

## DOM Locators

Chương trình sử dụng Robot Framework để tìm các DOM elements trên Facebook:

| Element | Locator Strategy |
|---------|-----------------|
| Post container | `div[role='article']` |
| Post content | `div[data-ad-preview='message']`, `div[dir='auto']` |
| Post time | `a[href*='/posts/']` aria-label, `abbr` |
| Post images | `img` with filtering (skip emoji, icon, small images) |
| Post link | `a[href*='/posts/']`, `a[href*='permalink']` |

> **Lưu ý**: Facebook thường xuyên thay đổi cấu trúc DOM. Nếu crawler không hoạt động, bạn có thể cần cập nhật các locators trong file `resources/variables.resource`.

## Lưu ý quan trọng

1. **Bảo mật**: Không commit file `config.local.yaml` chứa credentials lên Git.
2. **Rate Limiting**: Facebook có thể block tài khoản nếu crawl quá nhiều. Hãy sử dụng `scroll_pause_time` phù hợp.
3. **Quyền riêng tư**: Chỉ crawl dữ liệu công khai hoặc dữ liệu bạn có quyền truy cập.
4. **DOM thay đổi**: Facebook thường xuyên cập nhật giao diện. Các CSS selectors có thể cần được cập nhật.
5. **Two-Factor Auth**: Nếu tài khoản bật 2FA, bạn cần xử lý thêm bước xác thực.

## Xử lý lỗi thường gặp

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-------------|-----------|
| Login failed | Sai email/password | Kiểm tra lại credentials |
| No posts found | Profile private hoặc DOM thay đổi | Kiểm tra quyền truy cập, cập nhật locators |
| ChromeDriver error | Version không khớp | Cập nhật webdriver-manager |
| Timeout | Mạng chậm | Tăng `page_load_timeout` trong config |

## Công nghệ sử dụng

- **Robot Framework** - Framework automation chính
- **SeleniumLibrary** - Thư viện tương tác browser cho Robot Framework
- **Selenium WebDriver** - Điều khiển trình duyệt Chrome
- **Python** - Custom libraries cho xử lý dữ liệu
- **PyYAML** - Đọc file cấu hình
- **Requests** - Tải ảnh từ URL
