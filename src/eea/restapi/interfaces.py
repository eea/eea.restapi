# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from eea.restapi import _
from plone.autoform import directives as form
from plone.supermodel import model
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IEEARestapiLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IMosaicSettings(model.Schema):
    """ Settings for mosaic tiles
    """

    form.widget(styles='z3c.form.browser.textlines.TextLinesFieldWidget')
    styles = schema.Set(
        title=_(u'Styles'),
        description=_(
            u'Enter a list of styles to appear in the style pulldown. '
            u'Format is title|className, one per line.'),
        required=False,
        default=set([
            "default|default-tile",
            "Border|border-tile",
            "Green border|green-border-tile",
            "Filled|filled-tile",
            "Drop Shadow|drop-shadow-tile",
        ]),
        value_type=schema.ASCIILine(title=_(u'CSS Classes')),
    )


class ILocalSectionMarker(Interface):
    """ A local section marker. To be used with @localnavigation.
    """
