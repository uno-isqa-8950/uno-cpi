from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.blocks import (
    CharBlock, ChoiceBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock,
)

class ColumnBlock(StreamBlock):
    heading = CharBlock(classname="full title")
    paragraph = RichTextBlock(
        icon="fa-paragraph",
        template="blocks/paragraph_block.html"
    )
    image = ImageChooserBlock()

    class Meta:
        template = "blocks/column.html"


class TwoColumnBlock(StructBlock):

    left_column = RichTextBlock(icon='arrow-right', label='Left column content')
    right_column = RichTextBlock(icon='arrow-right', label='Right column content')

    class Meta:
        icon = 'placeholder'
        label = 'Two Columns'
        template = "blocks/two_column_block.html"

class ThreeColumnBlock(StructBlock):

    left_column = RichTextBlock(icon='arrow-right', label='Left column content')
    middle_column = RichTextBlock(icon='arrow-up', label='Middle column content')
    right_column = RichTextBlock(icon='arrow-right', label='Right column content')

    class Meta:
        icon = 'placeholder'
        label = 'Three Columns'
        template = "blocks/three_column_block.html"

class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = "blocks/image_block.html"


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4')
    ], blank=True, required=False)

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"


class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """
    text = TextBlock()
    attribute_name = CharBlock(
        blank=True, required=False, label='e.g. Mary Berry')

    class Meta:
        icon = "fa-quote-left"
        template = "blocks/blockquote.html"


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    heading_block = HeadingBlock()
    two_column_block = TwoColumnBlock()
    three_column_block = ThreeColumnBlock()
    paragraph_block = RichTextBlock(
        icon="fa-paragraph",
        template="blocks/paragraph_block.html"
    )
    image_block = ImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',
        icon="fa-s15",
        template="blocks/embed_block.html")