from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel



# Create your models here.


class StandardPage(Page):

    template = "standardpage/standard_page.html"

    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(blank=True, features=['h1', 'h2', 'h3', 'bold', 'italic', 'link', 'code', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed'])

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('body'),
    ]

    # context made
    def get_context(self, request):
        context = super().get_context(request)
        context["standardpages"] = StandardPage.objects.live().public().filter(locale__language_code=request.LANGUAGE_CODE)
        

        return context