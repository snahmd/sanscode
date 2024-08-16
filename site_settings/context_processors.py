from wagtail.models import Page
from blogpage.models import BlogCategories

def featuredPages(request):
    language = request.LANGUAGE_CODE
    pages = Page.objects.live().public().in_menu().filter(locale__language_code=language).order_by('-first_published_at')
    categories = BlogCategories.objects.all().filter(locale__language_code=language)
    return {
        "featured_pages": pages,
        "all_categories": categories
    }
