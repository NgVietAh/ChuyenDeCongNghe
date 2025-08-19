import os
import django
import asyncio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from myapp.models import Entry, Blog
from django.db.models import F, Min, OuterRef, Subquery, Sum
from asgiref.sync import sync_to_async

async def main():
    print("Example 1: F expression")
    entries_same_year_qs = Entry.objects.filter(pub_date__year=F("mod_date__year"))
    async for entry in entries_same_year_qs:
        print(entry)

    print("Example 2: Aggregate")
    first_year = await sync_to_async(Entry.objects.aggregate)(
        first_published_year=Min("pub_date__year")
    )
    print(first_year)

    print("Example 3: Subquery")
    entries_summary_qs = Entry.objects.values("pub_date__year").annotate(
        top_rating=Subquery(
            Entry.objects.filter(pub_date__year=OuterRef("pub_date__year"))
            .order_by("-rating")
            .values("rating")[:1]
        ),
        total_comments=Sum("number_of_comments")
    )
    async for item in entries_summary_qs:
        print(item)

    print("Example 4 : PK Lookup")
    try:
        blog = await Blog.objects.aget(pk=3)
        print(blog)
    except Blog.DoesNotExist:
        print("Blog không tồn tại.")

    print("Example 5 : LIKE escape")
    percent_entries_qs = Entry.objects.filter(headline__contains="%")
    async for entry in percent_entries_qs:
        print(entry)

if __name__ == "__main__":
    asyncio.run(main())
