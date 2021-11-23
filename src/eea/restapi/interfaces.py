# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
import json
from eea.restapi import _
from eea.api.dataconnector.interfaces import IBasicDataProvider \
    as IEeaDataConnectorBasicDataProvider
from eea.api.dataconnector.interfaces import IDataProvider \
    as IEeaDataConnectorDataProvider
from eea.api.dataconnector.interfaces import IFileDataProvider \
    as IEeaDataConnectorFileDataProvider
from eea.api.dataconnector.interfaces import IConnectorDataProvider \
    as IEeaDataConnectorConnectorDataProvider
from plone.app.z3cform.widget import QueryStringFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.schema import JSONField
from plone.supermodel import model
from zope import schema
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import provider
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IEEARestapiLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IMosaicSettings(model.Schema):
    """Settings for mosaic tiles"""

    form.widget(styles="z3c.form.browser.textlines.TextLinesFieldWidget")
    styles = schema.Set(
        title=_("Styles"),
        description=_(
            "Enter a list of styles to appear in the style pulldown. "
            "Format is title|className, one per line."
        ),
        required=False,
        default=set(
            [
                "default|default-tile",
                "Border|border-tile",
                "Green border|green-border-tile",
                "Filled|filled-tile",
                "Drop Shadow|drop-shadow-tile",
            ]
        ),
        value_type=schema.ASCIILine(title=_("CSS Classes")),
    )


class ILocalSectionMarker(Interface):
    """A local section marker. To be used with @localnavigation."""


class NotGiven(Interface):
    """Just pass"""
    pass


class IBasicDataProvider(IEeaDataConnectorBasicDataProvider):
    """A data provider concept"""


class IDataProvider(IEeaDataConnectorDataProvider):
    """An export of data for remote purposes"""

    provided_data = Attribute("Data made available by this data provider")


class IFileDataProvider(IEeaDataConnectorFileDataProvider):
    """Marker interface for objects that provide data to visualizations"""


class IConnectorDataProvider(IEeaDataConnectorConnectorDataProvider):
    """Marker interface for objects that provide data to visualizations"""


GENERIC_LIST_SCHEMA = json.dumps({"type": "list"})


@provider(IFormFieldProvider)
class IFacetedCollection(model.Schema):
    """Can specify indexes to be shown as facets on a collection"""

    facets = JSONField(
        title=_("Facets"),
        description="Facets configuration",
        schema=GENERIC_LIST_SCHEMA,
        # value_type=schema.Choice(
        #     vocabulary='plone.app.contenttypes.metadatafields'),
        required=False,
    )


@provider(IFormFieldProvider)
class ISimpleFacetedCollection(model.Schema):
    """ISimpleFacetedCollection."""

    filter = schema.Choice(
        title="Collection facet",
        vocabulary="plone.app.contenttypes.metadatafields",
        required=False,
    )


@provider(IFormFieldProvider)
class IHTMLEmbed(model.Schema):
    """A generic HTML embed field"""

    embed_code = schema.Text(
        title="Embed code",
        description="Any HTML code, typically an IFRAME tag",
        required=True,
    )


class IClonedBlocks(Interface):
    """Content that reuses blocks from a template

    The general architecture is the following:

    - Let's say I have some content that I want to replicate and reuse as a
    template inside the portal.
    - I should be able to click a button and this template is saved as a new
      content type. This content type retains a property that ties it to the
      original source. This property should be stored in the registry as a key
      ``eea.clonedblocks.<portal_type_name>`` and
      value is the UID of the content item.
    - The content type should not have the IBlocks behavior assigned. This
      causes Volto to use the regular metadata editor for it. That's fine. We
      enter the title, the data connector parameters. In its serialization we
      will receive from the serializer two fields: cloned_blocks and
      cloned_blocks_layout. The view template will know to fake the real blocks
      and blocks_layout based on these.
    - We can have a button that "disconnects" the content type from the
      template. This will copy the blocks data to the content type. By copying
      the blocks fields, Volto will show the visual editor (either regular or
      mosaic).

    """

    cloned_blocks = Attribute("Cloned blocks property")
    cloned_blocks_layout = Attribute("Cloned blocks_layout property")


class IBlockValidator(Interface):
    """IBlockValidator."""

    def clean(self, value):
        """Returns a cleaned value"""
