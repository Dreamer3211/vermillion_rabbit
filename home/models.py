from django.db import models
from django.core.cache.utils import make_template_fragment_key
from django.core.cache import cache 

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel


from streams import blocks

new_table_options = {
    'minSpareRows': 0,
    'startRows' : 4,
    'startCols': 4,
    'colHeaders': True,
    'rowHeaders' : True,
    'contextMenu' : [
        'rowAbove',
        'rowBelow',
        '--------',
        'col_left',
        'col_right',
        '---------',
        'remove_row',
        'remove_col',
        '----------',
        'undo',
        'redo',
    ],
    'editor': 'text',
    'stretchH': 'all',
    'renderer': 'text',
    'autoColumnSize': False,
}

class HomePage(Page):
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["flex.FlexPage", "services.ServiceListingPage",
    "contact.ContactPage"]
    max_count = 1
    lead_text = models.CharField(
        max_length=140, 
        blank=True,
        help_text="SubText under banner title"
    )
    button = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        related_name='+',
        help_text='Select optional page to link to',
        on_delete=models.SET_NULL,
    )
    button_text = models.CharField(
        max_length=50,
        default='Read More',
        blank=False,
        help_text='Button text',
    )
    banner_background_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        related_name='+',
        help_text='Banner Background image',
        on_delete=models.SET_NULL,
    )

    body = StreamField([
        ("title", blocks.TitleBlocks()),
        ("cards", blocks.CardsBlock()),
        ("images_and_text", blocks.ImageAndTextBlock()),
        ("call_to_action_block", blocks.CallToActionBlock()),
        ("testimonial",SnippetChooserBlock(
            target_model='testimonials.Testimonial',
            template = "streams/testimonial_block.html")),
        ("pricing_table", blocks.PricingTableBlock(table_options=new_table_options)),
        ], null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("lead_text"),
        PageChooserPanel("button"),
        FieldPanel("button_text"),
        ImageChooserPanel("banner_background_image"),
        StreamFieldPanel("body"),
    ]

    def save(self,*args,**kwargs):

        key = make_template_fragment_key(
            "home_page_streams",
            [self.id],        
            )
        cache.delete(key)


        return super().save( *args, **kwargs)
