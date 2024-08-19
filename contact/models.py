from django.db import models
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.fields import RichTextField
from modelcluster.fields import ParentalKey
from blogpage.models import BlogDetail, BlogIndex
from standardpage.models import StandardPage

# Create your models here.

class FormField(AbstractFormField):
    
    page = ParentalKey(
        "ContactPage", 
        related_name="form_fields",
        on_delete=models.CASCADE
        )


class ContactPage(AbstractEmailForm):
    template = "contact/contact_page.html"
    subpage_types = []
    parent_page_types = ["home.HomePage"]

    subtitle = models.CharField(max_length=255, blank=True, null=True)
    thank_you_text = RichTextField(blank=True)

    
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("subtitle"),
        InlinePanel("form_fields", label="Form fields" , classname="input-default"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel("from_address", classname="col6"),
                FieldPanel("to_address", classname="col6"),
            ]),
            FieldPanel("subject"),
        ]), 
    ]

    class Meta:
        verbose_name = "Contact Page"
        verbose_name_plural = "Contact Pages"
    
    def get_context(self, request):
        context = super().get_context(request)
        
        context['featured_posts_for_header'] = BlogDetail.objects.live().public().order_by('-first_published_at')[:6]
        context["standardpages"] = StandardPage.objects.live().public().filter(locale__language_code=request.LANGUAGE_CODE)
        context["parent"] = self.get_parent().specific
        
       
        return context