from django import forms
from wagtail.core import blocks
from wagtail.core.blocks.field_block import TextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock

class TitleBlocks(blocks.StructBlock):
    text = blocks.CharBlock(
        required = True,
        help_text = "Text to display",
    )

    class Meta:
        template = "streams/title_block.html"
        icon ='edit'
        label= 'Title'
        help_text= 'Centered to display on page'

class LinkValue(blocks.StructValue):
    """Additional Logic for link"""
    def url(self) -> str:
        internal_page = self.get("internal_page")
        external_link = self.get("external_link")
        if internal_page:
            return internal_page.url
        elif external_link:
            return external_link
        return ""
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList 


class Link(blocks.StructBlock):
 link_text = blocks.CharBlock(
      max_length=50,
      default="More detail here"
 )
 internal_page = blocks.PageChooserBlock(
      required=False
 )
 external_link = blocks.URLBlock(
      required=False
 )   

 class Meta:
     value_class = LinkValue

 def clean(self, value):
     internal_page = value.get("internal_page")
     external_link = value.get("external_link")
     errors = {}
     if internal_page and external_link :
         errors["internal_page"] = ErrorList([
             "Both fields cannot be selected simultaneously.Please select either an internal page or an external_link"])
         errors["external_link"] = ErrorList([
             "Both fields cannot be selected simultaneously.Please select either an internal page or an external_link"])
     elif not internal_page and not external_link:
         errors["internal_page"] = ErrorList([
             "Please select a page or enter a URL for one of these options"])
         errors["external_link"] = ErrorList([
             "Please select a page or enter a URL for one of these options"])

     if errors:
         raise ValidationError("Validation error in your link", params=errors)

     return super().clean(value)


class Card(blocks.StructBlock):
 title = blocks.CharBlock(
     max_length=100, 
     help_text="Bold title text for card, max 100chars.",
 )
 text = blocks.TextBlock(
     max_length=255, 
     help_text="Optional text for card. Max Length 255 chars", 
     required=False
 )
 image = ImageChooserBlock(
      help_text="Image cropped to scale"
 )
        
 link = Link(help_text="Enter a link or select a page")     

class CardsBlock(blocks.StructBlock):

    cards = blocks.ListBlock(
        Card()
    )
    class Meta:
        template = "streams/cards_block.html"
        icon = "image"
        label = "standard cards"

class RadioSelectBlock(blocks.ChoiceBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.field.widget = forms.RadioSelect(
            choices=self.field.widget.choices 
        )

class ImageAndTextBlock(blocks.StructBlock):

    image = ImageChooserBlock(help_text = "image cropped to scale")
    image_alignment = RadioSelectBlock(
        choices = (
            ("left", "Image to the left"),
            ("right", "Image to the right"),
        ),   
        default='left',
        help_text = "Image either left with text on right. Or image right and text on left."
        )
    title = blocks.CharBlock(max_length=60, help_text="Max length of 60 characters.")
    text = blocks.CharBlock(max_length= 140,required=False,help_text="Max length of 60 characters.")
    link = Link()

    class Meta:
        template="streams/image_and_text_block.html"
        icon = "image"
        label = "Image & Text"

class CallToActionBlock(blocks.StructBlock):

    title=blocks.CharBlock(max_length=200,help_text="Max length of 200 characters.")
    link= Link()

    class Meta:
        template = "streams/call_to_action_block.html"
        icon = "plus"
        label = "Call to Action"

class PricingTableBlock(TableBlock):
    """ Prcing Table Block"""

    class Meta:
        template = "streams/pricing_table_block.html"
        label = "Pricing Table"
        icon = "table"
        help_text = "Pricing table should have 4 columns"

