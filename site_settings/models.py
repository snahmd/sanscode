from django.db import models

from wagtail.contrib.settings.models import register_setting, BaseGenericSetting, BaseSiteSetting
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model


@register_setting
class GenericFooterLogoSettings(BaseGenericSetting):
    footer_logo = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Logo to display in the footer of the site.",
    )

    panels = [
        FieldPanel("footer_logo"),
    ]

@register_setting
class GenericFooterInfoSettings(BaseSiteSetting):
    footer_info = models.TextField(
        blank=True,
        null=True,
        help_text="Text to display in the footer of the site.",
    )
    copyright_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Copyright text to display in the footer of the site.",   
    )
    copyright_link_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Text for the copyright link.",
    )
    copyright_link = models.URLField(
        blank=True,
        null=True,
        help_text="Link for the copyright text.",
    )
    main_link_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Title for the main link.",   
    )
    site_settings_link_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Title for the site settings link.",
    )

    panels = [
        FieldPanel("footer_info"),
        FieldPanel("copyright_text"),
        FieldPanel("copyright_link_text"),
        FieldPanel("copyright_link"),
        FieldPanel("main_link_title"),
        FieldPanel("site_settings_link_title"),
    ]

@register_setting
class SocialMediaSettings(BaseSiteSetting):
    facebook = models.URLField(
        blank=True,
        null=True,
        help_text="Facebook URL",
    )
    x = models.URLField(
        blank=True,
        null=True,
        help_text="X URL",
    )
    linkedin = models.URLField(
        blank=True,
        null=True,
        help_text="LinkedIn URL",
    )
    xing = models.URLField(
        blank=True,
        null=True,
        help_text="Xing URL",
    )
    instagram = models.URLField(
        blank=True,
        null=True,
        help_text="Instagram URL",
    )
    github = models.URLField(
        blank=True,
        null=True,
        help_text="GitHub URL",
    )
    behance = models.URLField(
        blank=True,
        null=True,
        help_text="Behance URL",
    )
    dribbble = models.URLField(
        blank=True,
        null=True,
        help_text="Dribbble URL",
    )
    figma = models.URLField(
        blank=True,
        null=True,
        help_text="Figma URL",
    )
    unsplash = models.URLField(
        blank=True,
        null=True,
        help_text="Unsplash URL",
    )
    youtube = models.URLField(
        blank=True,
        null=True,
        help_text="YouTube URL",
    )
    tiktok = models.URLField(
        blank=True,
        null=True,
        help_text="TikTok URL",
    )


    panels = [
        FieldPanel("facebook"),
        FieldPanel("x"),
        FieldPanel("linkedin"),
        FieldPanel("instagram"),
        FieldPanel("github"),
        FieldPanel("behance"),
        FieldPanel("dribbble"),
        FieldPanel("figma"),
        FieldPanel("unsplash"),
        FieldPanel("youtube"),
        FieldPanel("tiktok"),
    ]    