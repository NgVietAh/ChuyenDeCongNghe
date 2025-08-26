import os
import django

# Thiết lập Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

# Import model sau khi setup
from polls.models import Poll

# Tạo Poll mới
p = Poll(question="Bài kiểm tra đầu tiên")
p.save()

print(f"Poll đã được tạo với ID: {p.id}")
