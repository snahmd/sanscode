from django.db import models
from wagtail.models import Page, Orderable

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.images import get_image_model
# import register for django
from wagtail.snippets.models import register_snippet



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class MessageUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

register_snippet(MessageUser)
    
class BlogAuthor(models.Model):
    name = models.CharField(max_length=100)
    website = models.EmailField(max_length=100)
    image = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return self.name

register_snippet(BlogAuthor)

class BlogDetailAuthorPlacement(models.Model):
    page = ParentalKey('BlogDetail', related_name='author_placement')
    author = models.ForeignKey(
        'blogpage.BlogAuthor',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        FieldPanel('author'),
    ]

    def __str__(self):
        return self.author.name
    
class BlogCategories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

register_snippet(BlogCategories)

class BlogDetailCategoriesPlacement(models.Model):
    page = ParentalKey('BlogDetail', related_name='categories_placement')
    categories = models.ForeignKey(
        'blogpage.BlogCategories',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        FieldPanel('categories'),
    ]

    def __str__(self):
        return self.categories.name    


  

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
        # filter with locale.language_code
        context['blogpages'] = context['blogpages'].filter(locale__language_code=request.LANGUAGE_CODE)
        tag = request.GET.get('tag')
        if tag:
            # ignore case sensitive
            if tag != "all":
                context['blogpages'] = context['blogpages'].filter(tags__name__iexact=tag)
        # filter category
        category = request.GET.get('category')
        if category:
            # ignore case sensitive
            if category != "all":
                context['blogpages'] = context['blogpages'].filter(categories_placement__categories__slug__iexact=category)    

        context["blog_categories"] = BlogCategories.objects.all()
        context["featuredOwner"] = "admin"
        context["myName"] = "San"
        context["tag"] = tag if tag else "all"
        context["category"] = category if category else "all"

        # Pagination
        page = request.GET.get('p')
        paginator = Paginator(context['blogpages'], 9)
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
        context['featured_posts_for_header'] = BlogDetail.objects.live().public().order_by('-first_published_at').filter(locale__language_code=request.LANGUAGE_CODE)[:6]

        

        return context

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey 
from taggit.models import TaggedItemBase

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'blogpage.BlogDetail',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

from wagtail.fields import StreamField
from wagtail.blocks import TextBlock, BlockQuoteBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtailcodeblock.blocks import CodeBlock

from wagtail import blocks

from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    website = models.EmailField(max_length=100)
    image = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
   

    def __str__(self):
        return self.name


from wagtail.contrib.forms.models import AbstractFormField
# class SubscribeFormField(AbstractFormField):
    
#     page = ParentalKey(
#         "BlogDetail", 
#         related_name="form_fields",
#         on_delete=models.CASCADE
#         )
class Subscribe(models.Model):
    
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.email

 

    

     
register_snippet(Subscribe)


from blocks import blocks as custom_blocks
class BlogDetail(Page):
    


    # template = 'home/home_page.html'
    template = 'blogpage/blog_detail.html'
    parent_page_type = ['blogpage.BlogIndex']
    subpage_types = []

    
   
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    # body = RichTextField(
    #     blank=True,
    #     features=['h2', 'h3', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed', 'code', 'blockquote', 'superscript', 'subscript', 'strikethrough']
    # )

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    image = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    body = StreamField(
        [
            # ('text', TextBlock()),
            ('rich_text', RichTextBlock()),
            # ('image', ImageChooserBlock()),
            ('text', custom_blocks.TextBlock()),
            ('document', DocumentChooserBlock()),
            ('page', blocks.PageChooserBlock( required=False)),
            ('author', SnippetChooserBlock('blogpage.Author')),
            ('info', custom_blocks.InfoBlock()),
            ('faq', custom_blocks.FAQListBlock()),
            ('carousel', custom_blocks.CarouselBlock()),
            ('image', custom_blocks.ImageBlock()),
            ('embed', EmbedBlock()),
            ('code', CodeBlock()),
            ('blockquote', BlockQuoteBlock()),
            ('quotation', blocks.StructBlock(
                        [
                            ('quote', RichTextBlock()),
                            ('cite', TextBlock(required=False)),
                        ],
                        icon='openquote',
                        template='blocks/blockquote.html',
            )),
            # ("carousel", blocks.StreamBlock(
            #     [
            #         ('image', ImageChooserBlock()),
            #         ('quotation', blocks.StructBlock(
            #             [
            #                 ('quote', TextBlock()),
            #                 ('cite', TextBlock()),
            #             ],
            #             icon='openquote',
            #         )),
            #     ],
            # )),
            # ('info', custom_blocks.InfoBlock()),
            # ('faq', custom_blocks.FAQListBlock()),
            ('call_to_action_1', custom_blocks.CallToAction1())
            # ('call_to_action_1', blocks.StructBlock(
            #     [
            #         ('text', blocks.RichTextBlock( features=['bold', 'italic'], required=True)),
            #         ('page', blocks.PageChooserBlock()),
            #         ('button_text' , blocks.CharBlock(required=False, max_length=100)),
            #     ],
            #     label="CTA #1",
                
            # ))

        ],
        # block_counts= {
        #     "text": {"min_num": 1, "max_num": 5},
        #     "image": {"max_num": 1},
        # }
        use_json_field= True,
        null=True,
        blank=True,
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
        # FieldPanel('image'),
        FieldPanel('cta_url_one'),
        FieldPanel('cta_url_two'),
        FieldPanel('cta_url_three'),
        FieldPanel('cta_url_four'),
        FieldPanel('tags'),
        # InlinePanel('author_placement', label="Author"),
        InlinePanel('categories_placement', label="Categories"),
    ] 
    # context ile template'e veri gönderme
    def get_context(self, request):
        context = super().get_context(request)
        context['blogDetailPost'] = BlogDetail.objects.live().public().order_by('-first_published_at')
        # filter with locale.language_code
        context['blogDetailPost'] = context['blogDetailPost'].filter(locale__language_code=request.LANGUAGE_CODE)
        print(context['blogDetailPost'])
        
        context['featured_posts_for_header'] = BlogDetail.objects.live().public().order_by('-first_published_at').filter(locale__language_code=request.LANGUAGE_CODE)[:6]
        # context["prevPost"] = BlogDetail.objects.live().public().filter(first_published_at__lt=self.first_published_at).order_by('-first_published_at').first()
        # if prevPost exist then send it
        context["prevPost"] = context['blogDetailPost'].filter(first_published_at__lt=self.first_published_at).order_by('-first_published_at').first()
        context["nextPost"] = context['blogDetailPost'].filter(first_published_at__gt=self.first_published_at).order_by('first_published_at').first()
        context["blog_categories"] = BlogCategories.objects.all()
        # with context send data to blog_index_page.html für subscribe 
        context["subscribe"] = Subscribe.objects.all()

        

        return context   