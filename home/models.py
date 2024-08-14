from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.images import get_image_model
from blogpage.models import BlogDetail, BlogCategories, BlogAuthor
from standardpage.models import StandardPage
from contact.models import ContactPage



# Create your models here.

class HomePage(Page):

    # template = 'home/home_page.html'
    max_count = 1

    subtitle = models.CharField(max_length=150, blank=True, null=True)
    subtitle_light = models.CharField(max_length=150, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    body = RichTextField(blank=True)

    image = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('subtitle_light'),
        FieldPanel('description'),
        FieldPanel('body'),
        FieldPanel('image'),
    ]
     # context ile template'e veri gönderme
    def get_context(self, request):
        context = super().get_context(request)
        context['blogpages'] = BlogDetail.objects.live().public().filter(locale__language_code=request.LANGUAGE_CODE).order_by('-first_published_at')
        context['categories'] = BlogCategories.objects.all()
       
        context["featuredOwner"] = "admin"
        context["myName"] = "_sanscode"
        context["subtitle"] = self.subtitle
        context["subtitle_light"] = self.subtitle_light
        context["description"] = self.description
       
        # # send in homepage img to template
        # context['homeImage'] = self.image
        context['featured_posts_for_header'] = BlogDetail.objects.live().public().order_by('-first_published_at').filter(locale__language_code=request.LANGUAGE_CODE)[:6]
        context["standardpages"] = StandardPage.objects.live().public().filter(locale__language_code=request.LANGUAGE_CODE)
        context["contactpage"] = ContactPage.objects.live().public().filter(locale__language_code=request.LANGUAGE_CODE)
        
        


        return context
