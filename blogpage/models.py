from django.db import models
from wagtail.models import Page, Orderable

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.images import get_image_model
# import register for django
from wagtail.snippets.models import register_snippet

from wagtail.contrib.routable_page.models import RoutablePageMixin, path, re_path
from django.template.defaultfilters import slugify


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.models import TranslatableMixin, BootstrapTranslatableMixin  

from standardpage.models import StandardPage












  
class BlogAuthor(TranslatableMixin, models.Model):

    
    name = models.CharField(max_length=100)
    website = models.EmailField(max_length=100)
    bio = models.TextField(max_length=200, default="Bio")
    image = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    x = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    linkedin = models.CharField(max_length=100, blank=True, null=True)
    github = models.CharField(max_length=100, blank=True, null=True)
    behance = models.CharField(max_length=100, blank=True, null=True)
    dribbble = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)

    slug = models.SlugField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    # update url on slug change


    


    def __str__(self):
        return self.name
    
    class Meta(TranslatableMixin.Meta):
        verbose_name = "Author"
        verbose_name_plural = "Authors"
    

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
    

class Ads(TranslatableMixin, models.Model):
    title = models.CharField(max_length=100)
    title_bold = models.CharField(max_length=100)
    ad_image = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return self.title + " " + self.title_bold
    
    class Meta(TranslatableMixin.Meta):
        verbose_name = "Ad"
        verbose_name_plural = "Ads"

register_snippet(Ads)
    
class BlogCategories(TranslatableMixin, models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
   
    category_image = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return self.name
    
    class Meta(TranslatableMixin.Meta):
        verbose_name = "Category"
        verbose_name_plural = "Categories"

register_snippet(BlogCategories)

class BlogDetailCategoriesPlacement(models.Model):
    page = ParentalKey('BlogDetail', related_name='categories_placement')
    category = models.ForeignKey(
        'blogpage.BlogCategories',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='blogs',
    )
    
    panels = [
        FieldPanel('category'),
    ]

    def __str__(self):
        return self.category.name    


  

class BlogIndex(RoutablePageMixin, Page):

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

    @path('tag/<str:tag>/', name='tag')
    def blog_posts_by_tag(self, request, tag=None):

        posts = BlogDetail.objects.live().public().filter(tags__name__iexact=tag).filter(locale__language_code=request.LANGUAGE_CODE)
        paginator = Paginator(posts, 3)
        page = request.GET.get('p')
        try:
            blogpages = paginator.page(page)
            currentPage = int(page)
        except PageNotAnInteger:
            blogpages = paginator.page(1)
            currentPage = 1
        except EmptyPage:
            blogpages = paginator.page(paginator.num_pages)
            currentPage = paginator.num_pages
        print(posts)
        return self.render(
            request, 
            context_overrides={
                'posts': blogpages,
                'currentPage': currentPage,
                "tag": tag
            },
            template= "blogpage/blog_tag_page.html"
        )
    
    @path('category/<str:category>/', name='category')
    def blog_posts_by_category(self, request, category=None):
        print(".....adsl;adsl")
        posts = BlogDetail.objects.live().public().filter(categories_placement__category__slug__iexact=category).filter(locale__language_code=request.LANGUAGE_CODE)
        paginator = Paginator(posts, 4)
        page = request.GET.get('p')
        try:
            blogpages = paginator.page(page)
            currentPage = int(page)
        except PageNotAnInteger:
            blogpages = paginator.page(1)
            currentPage = 1
        except EmptyPage:
            blogpages = paginator.page(paginator.num_pages)
            currentPage = paginator.num_pages
        return self.render(
            request, 
            context_overrides={
                'posts': blogpages,
                "category": category,
                'currentPage': currentPage,
            },
            template= "blogpage/blog_category_page.html"
        )
    
    
    # @path('author/<int:author_id>/<str:author_slug>/', name='author')

    # def blog_posts_by_author(self, request, author_id=None, author_slug=None):
    #     posts = BlogDetail.objects.live().public().filter(author_placement__author__id=author_id).filter(locale__language_code=request.LANGUAGE_CODE)
    #     author_instance = BlogAuthor.objects.get(id=author_id)
       



    #     return self.render(
    #         request, 
    #         context_overrides={
    #             'posts': posts,
    #             "author": author_instance
    #         },
    #         template= "blogpage/author_page.html"
    #     )
    @path('author/<str:author>/', name='author')
    def blog_posts_by_author(self, request, author=None):
        print("lkadskldaskadskkladskasdkl")
        posts = BlogDetail.objects.live().public().filter(author_placement__author__slug__iexact=author).filter(locale__language_code=request.LANGUAGE_CODE)
        print("all post of author:")
        print(BlogDetail.objects.live().public().filter(author_placement__author__slug__iexact=author))
        print("yazarin postlari:")
        print(posts)
        print("------")
        paginator = Paginator(posts, 9)
        page = request.GET.get('p')
        try:
            blogpages = paginator.page(page)
            currentPage = int(page)
        except PageNotAnInteger:
            blogpages = paginator.page(1)
            currentPage = 1
        except EmptyPage:
            blogpages = paginator.page(paginator.num_pages)
            currentPage = paginator.num_pages
        print("blogpages:")
        print(blogpages)
        print("------")
        # get all objects
        author_instance = BlogAuthor.objects.all().filter(slug__iexact=author).filter(locale__language_code=request.LANGUAGE_CODE).first()
        print("....")
        print(author_instance)
        print(author_instance.url)
        # change page url according to author
        
        
       


        return self.render(
            request, 
            context_overrides={
                'posts': posts,
                "author": author_instance,
                'currentPage': currentPage,
            },
            template= "blogpage/author_page.html"
            
        )


    # context ile template'e veri gönderme
    def get_context(self, request):
        
        context = super().get_context(request)
        context["homepage"] = self.get_parent().specific


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
                context['blogpages'] = context['blogpages'].filter(categories_placement__category__slug__iexact=category)    

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
        context["standardpages"] = StandardPage.objects.live().public().filter(locale__language_code=request.LANGUAGE_CODE)
        context["blogmodel"] = BlogIndex.objects.live().public().filter(locale__language_code=request.LANGUAGE_CODE).first()
        # use home.HomePage or parent_page
        context["homemodel"] = self.get_parent().specific
        # get all childrens
        childs_count = context["homemodel"].get_children_count()
       
        print(context["homemodel"])
        # context["contactmodel"] = ContactPage.objects.live().public().filter(locale__language_code=request.LANGUAGE_CODE).first()
        
        

        return context

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey 
from taggit.models import TaggedItemBase

class BlogPageTag(TranslatableMixin, TaggedItemBase):
    content_object = ParentalKey(
        'blogpage.BlogDetail',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )
    url = models.CharField(max_length=100, blank=True, null=True)

    
    class Meta(TranslatableMixin.Meta):
        verbose_name = "Tag"
        verbose_name_plural = "Tags" 

register_snippet(BlogPageTag)      

from wagtail.fields import StreamField
from wagtail.blocks import TextBlock, BlockQuoteBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtailcodeblock.blocks import CodeBlock

from wagtail import blocks

from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock






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

    # ads = StreamField(
    #     [
    #         ('sponsored_ads', blocks.StructBlock(
    #                     [
    #                         ('ads_text', TextBlock(required=False)),
    #                         ('ads_image', ImageChooserBlock(required=False, null=True, blank=True, on_delete=models.SET_NULL)),
    #                     ],
    #                     icon='openquote',
    #                     template='blocks/sponsored_ads.html',
    #         )),
    #     ]
    # )         

    body = StreamField(
        [
            # ('text', TextBlock()),
            ('rich_text', RichTextBlock()),
            # ('image', ImageChooserBlock()),
            ('text', custom_blocks.TextBlock()),
            ('document', DocumentChooserBlock()),
            ('page', blocks.PageChooserBlock( required=False)),
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
        FieldPanel('image'),
        FieldPanel('cta_url_one'),
        FieldPanel('cta_url_two'),
        FieldPanel('cta_url_three'),
        FieldPanel('cta_url_four'),
        FieldPanel('tags'),
        InlinePanel('author_placement', label="Author"),
        InlinePanel('categories_placement', label="Categories"),
    ] 
    # context ile template'e veri gönderme
    def get_context(self, request):
        context = super().get_context(request)
        context["parent"] = self.get_parent().specific
        context["parent_parent"] = self.get_parent().get_parent().specific
        context["categories"] = [category.category for category in self.categories_placement.all()]
        context["authors"] = [author.author for author in self.author_placement.all()]
        context["tags"] = self.tags.all()
        context["prevPost"] = BlogDetail.objects.live().public().filter(first_published_at__lt=self.first_published_at).order_by('-first_published_at').first()
        context["nextPost"] = BlogDetail.objects.live().public().filter(first_published_at__gt=self.first_published_at).order_by('first_published_at').first()






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
        context["standardpages"] = StandardPage.objects.live().public().filter(locale__language_code=request.LANGUAGE_CODE)
        

       



        return context   