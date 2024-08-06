from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.images import get_image_model

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class BlogIndex(Page):

    # template = 'home/home_page.html'
    template = 'blogpage/blog_index_page.html'
    max_count = 1
    parent_page_type = ['home.HomePage']
    subpage_types = ['blogpage.BlogDetail']


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
        FieldPanel('subtitle'),
        FieldPanel('body'),
        FieldPanel('image'),
    ]
    # context ile template'e veri gönderme
    def get_context(self, request):
        context = super().get_context(request)
        context['blogpages'] = BlogDetail.objects.live().public().order_by('-first_published_at')
        context["featuredOwner"] = "admin"
        context["myName"] = "San"

        # Pagination
        page = request.GET.get('p')
        paginator = Paginator(context['blogpages'], 2)
        try:
            blogpages = paginator.page(page)
            context["currentPage"] = int(page)
        except PageNotAnInteger:
            blogpages = paginator.page(1)
            context["currentPage"] = 1
        except EmptyPage:
            blogpages = paginator.page(paginator.num_pages)
            context["currentPage"] = paginator.num_pages
        context['blogpages'] = blogpages 
        
        

        return context

class BlogDetail(Page):

    # template = 'home/home_page.html'
    template = 'blogpage/blog_detail.html'
    parent_page_type = ['blogpage.BlogIndex']
    subpage_types = []
   
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    body = RichTextField(blank=True)

    image = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    cta_url_one = models.ForeignKey(
        'blogpage.BlogDetail',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    cta_url_two = models.ForeignKey(
        'blogpage.BlogDetail',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    cta_url_three = models.ForeignKey(
        'blogpage.BlogDetail',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    cta_url_four = models.ForeignKey(
        'blogpage.BlogDetail',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('body'),
        FieldPanel('image'),
        FieldPanel('cta_url_one'),
        FieldPanel('cta_url_two'),
        FieldPanel('cta_url_three'),
        FieldPanel('cta_url_four'),
    ] 
    # context ile template'e veri gönderme
    def get_context(self, request):
        context = super().get_context(request)
        context['blogDetailPost'] = BlogDetail.objects.live().public().order_by('-first_published_at')
        # context["prevPost"] = BlogDetail.objects.live().public().filter(first_published_at__lt=self.first_published_at).order_by('-first_published_at').first()
        # if prevPost exist then send it
        context["prevPost"] = BlogDetail.objects.live().public().filter(first_published_at__lt=self.first_published_at).order_by('-first_published_at').first()
        context["nextPost"] = BlogDetail.objects.live().public().filter(first_published_at__gt=self.first_published_at).order_by('first_published_at').first()
        

        return context   