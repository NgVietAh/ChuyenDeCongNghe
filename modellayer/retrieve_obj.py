
import os
import django
from datetime import date

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from myapp.models import Blog, Entry

#select all entry
all_entries = Entry.objects.all()
print("All Entries:")
for e in all_entries:
    print(f"- {e.headline} ({e.pub_date})")

# filter entries 2006
entries_2006 = Entry.objects.filter(pub_date__year=2006)
print("\nEntries from 2006:")
for e in entries_2006:
    print(f"- {e.headline} ({e.pub_date})")

# chain entrie & exclude
entries_filtered = Entry.objects.filter(headline__startswith="What") \
                                .exclude(pub_date__gte=date.today()) \
                                .filter(pub_date__gte=date(2005, 1, 30))

print("\nFiltered Entries (chained filters):")
for e in entries_filtered:
    print(f"- {e.headline} ({e.pub_date})")

# Minh họa queryset unique
q1 = Entry.objects.filter(headline__startswith="What")
q2 = q1.exclude(pub_date__gte=date.today())
q3 = q1.filter(pub_date__gte=date.today())

print("\nUnique QuerySets:")
print("q1:", list(q1))  # đánh giá q1
print("q2:", list(q2))  # đánh giá q2
print("q3:", list(q3))  # đánh giá q3

# Minh họa queryset lazy
q_lazy = Entry.objects.filter(headline__icontains="AI")
# Lúc này chưa truy vấn database
print("\nQuerySet before evaluation (lazy):", q_lazy)  # Django chỉ hiển thị QuerySet, chưa lấy dữ liệu
# Lấy 1 đối tượng duy nhất
# one_entry = Entry.objects.get(pk=1)

# Giới hạn queryset
# Lấy 5 object đầu tiên
# Entry.objects.all()[:5]
# # Lấy thứ 6 đến 10
# Entry.objects.all()[5:10]

# Lấy 1 obj từ queryset đã order
# first_entry = Entry.objects.order_by("headline")[0]


# Negative index không được hỗ trợ
# Entry.objects.all()[-1] -> lỗi


# Khi đánh giá (iter, list, print)
print("Evaluated QuerySet (lazy):")
for e in q_lazy:
    print(f"- {e.headline} ({e.pub_date})")

# Lọc entry thuộc blog “Beatles Blog” và in ra
# entries_beatles = Entry.objects.filter(blog__name="Beatles Blog")
# print("\nEntries from 'Beatles Blog':")
# for e in entries_beatles:
#     print(f"- {e.headline} ({e.pub_date})")

# Lọc blog có entry chứa “Lennon” và in ra
# blogs_lennon = Blog.objects.filter(entry__headline__contains="Lennon")
# print("\nBlogs with entries containing 'Lennon':")
# for b in blogs_lennon:
#     print(f"- {b.name}")

# Blog thỏa 2 điều kiện: entry chứa “Lennon” và xuất bản năm 2008
# blogs_lennon_2008 = Blog.objects.filter(entry__headline__contains="Lennon", entry__pub_date__year=2008)
# print("\nBlogs with entries containing 'Lennon' published in 2008:")
# for b in blogs_lennon_2008:
#     print(f"- {b.name}")

# Exclude example
# blogs_not_lennon_2008 = Blog.objects.exclude(entry__headline__contains="Lennon", entry__pub_date__year=2008)
# print("\nBlogs excluding entries containing 'Lennon' published in 2008:")
# for b in blogs_not_lennon_2008:
#     print(f"- {b.name}")
