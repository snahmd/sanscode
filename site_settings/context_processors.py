from wagtail.models import Page
from blogpage.models import BlogCategories, BlogDetail, BlogIndex, Ads
from contact.models import ContactPage
from home.models import HomePage

def featuredPages(request):
    language = request.LANGUAGE_CODE
    pages = Page.objects.live().public().in_menu().filter(locale__language_code=language).order_by('-first_published_at')
    blog_pages = BlogDetail.objects.live().public().in_menu().filter(locale__language_code=language).order_by('-first_published_at')
    categories = BlogCategories.objects.all().filter(locale__language_code=language)
    homePage = HomePage.objects.live().public().filter(locale__language_code=language).first()
    blogIndexPage = BlogIndex.objects.live().public().filter(locale__language_code=language).first()
    contactPage = ContactPage.objects.live().public().filter(locale__language_code=language).last()
    ad = Ads.objects.all().filter(locale__language_code=language).first()
    return {
        "featured_pages": pages,
        "all_categories": categories,
        "blog_pages": blog_pages,
        "home_page": homePage,
        "blog_index_page": blogIndexPage,
        "contact_page": contactPage,
        'ad': ad
    }
