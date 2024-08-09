# Generated by Django 5.0.7 on 2024-08-08 15:53

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogpage', '0013_blogcategories_blogdetailcategoriesplacement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogdetail',
            name='body',
            field=wagtail.fields.StreamField([('text', 0), ('rich_text', 1), ('image', 2), ('embed', 3), ('code', 6), ('blockquote', 7), ('carousel', 9)], blank=True, block_lookup={0: ('wagtail.blocks.TextBlock', (), {}), 1: ('wagtail.blocks.RichTextBlock', (), {}), 2: ('wagtail.images.blocks.ImageChooserBlock', (), {}), 3: ('wagtail.embeds.blocks.EmbedBlock', (), {}), 4: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('bash', 'Bash/Shell'), ('css', 'CSS'), ('diff', 'diff'), ('html', 'HTML'), ('javascript', 'Javascript'), ('json', 'JSON'), ('python', 'Python'), ('scss', 'SCSS'), ('yaml', 'YAML')], 'help_text': 'Coding language', 'identifier': 'language', 'label': 'Language'}), 5: ('wagtail.blocks.TextBlock', (), {'identifier': 'code', 'label': 'Code'}), 6: ('wagtail.blocks.StructBlock', [[('language', 4), ('code', 5)]], {}), 7: ('wagtail.blocks.BlockQuoteBlock', (), {}), 8: ('wagtail.blocks.StructBlock', [[('quote', 0), ('cite', 0)]], {'icon': 'openquote'}), 9: ('wagtail.blocks.StreamBlock', [[('image', 2), ('quotation', 8)]], {})}, null=True),
        ),
    ]