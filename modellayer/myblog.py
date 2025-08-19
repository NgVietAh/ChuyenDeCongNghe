# run_blog.py
import os
import django
from datetime import date

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from myapp.models import Blog, Author, Entry

blog1 = Blog.objects.create(name="Beatles Blog", tagline="All the latest Beatles news.")
blog2 = Blog.objects.create(name="Cheddar Talk", tagline="Cheese lovers unite!")

author1 = Author.objects.create(name="Joe", email="joe@example.com")
author2 = Author.objects.create(name="John", email="john@example.com")
author3 = Author.objects.create(name="Paul", email="paul@example.com")
author4 = Author.objects.create(name="George", email="george@example.com")
author5 = Author.objects.create(name="Ringo", email="ringo@example.com")

entry1 = Entry.objects.create(blog=blog1, headline="New Album Released", body_text="Check out the new album!", pub_date=date.today())
entry1.authors.add(author1)  # ManyToManyField add single author

entry2 = Entry.objects.create(blog=blog2, headline="Cheddar Festival", body_text="Cheddar cheese festival this weekend.", pub_date=date.today())
entry2.authors.add(author2, author3, author4, author5)  # ManyToManyField add multiple authors

#update data
entry1.blog = blog2
entry1.save()

#select data    
print("All Blogs:")
for b in Blog.objects.all():
    print(f"- {b.name}: {b.tagline}")

print("\nEntries with rating >= 5:")
for e in Entry.objects.filter(rating__gte=5):
    author_names = ", ".join(a.name for a in e.authors.all())
    print(f"- {e.headline} by {author_names}")

print("\nAuthors of 'Cheddar Festival':")
festival_entry = Entry.objects.get(headline="Cheddar Festival")
for a in festival_entry.authors.all():
    print(f"- {a.name}")
