from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.images import get_image_model
from blogpage.models import BlogDetail

class HomePage(Page):

    # template = 'home/home_page.html'
    max_count = 1

    subtitle = models.CharField(max_length=100, blank=True, null=True)
    body = RichTextField(blank=True)

    image = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('subtitle', read_only=True),
        FieldPanel('body'),
        FieldPanel('image'),
    ]
     # context ile template'e veri gönderme
    def get_context(self, request):
        context = super().get_context(request)
        context['blogpages'] = BlogDetail.objects.live().public()
        context["featuredOwner"] = "admin"
        context["myName"] = "_sanscode"
       
        # # send in homepage img to template
        # context['homeImage'] = self.image
        context['featured_posts_for_header'] = BlogDetail.objects.live().public().order_by('-first_published_at')[:6]
       
        return context
