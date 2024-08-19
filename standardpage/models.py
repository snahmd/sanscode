from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from blocks import blocks as custom_blocks
from wagtail.fields import StreamField
from wagtail.fields import StreamField
from wagtail.blocks import TextBlock, BlockQuoteBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtailcodeblock.blocks import CodeBlock

from wagtail import blocks

from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.images import get_image_model

# Create your models here.


class StandardPage(Page):

    template = "standardpage/standard_page.html"
    parent_page_type = ['home.HomePage']

    subtitle = models.CharField(max_length=100, blank=True)
    # body = RichTextField(blank=True, features=['h1', 'h2', 'h3', 'bold', 'italic', 'link', 'code', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed'])

    image = StreamField(
        [
            ('image', ImageChooserBlock()),
        ],
        null=True,
        blank=True,
    )


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

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('image'),
        FieldPanel('body'),
    ]

    # context made
    def get_context(self, request):
        context = super().get_context(request)
        context["standardpages"] = StandardPage.objects.live().public().filter(locale__language_code=request.LANGUAGE_CODE)
        

        return context