# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
import json
from eea.restapi import _
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


class IBlockValidator(Interface):
    """IBlockValidator."""

    def clean(self, value):
        """Returns a cleaned value"""
