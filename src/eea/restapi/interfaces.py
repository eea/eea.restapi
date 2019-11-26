# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

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

import json


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


@provider(IFormFieldProvider)
class IDataConnector(model.Schema):
    """ A generic discodata connector
    """

    endpoint_url = schema.TextLine(
        title=u"Discodata endpoint URL", required=True,
        default=u"http://discomap.eea.europa.eu/App/SqlEndpoint/query"
    )
    sql_query = schema.Text(
        title=u"SQL Query",
        required=True,
    )

    # directives.fieldset('dataconnector', label="Data connector", fields=[
    #     'endpoint_url', 'query',
    # ])


class IBasicDataProvider(Interface):
    """ A data provider concept
    """


class IDataProvider(IBasicDataProvider):
    """ An export of data for remote purposes
    """

    provided_data = Attribute(u'Data made available by this data provider')


class IFileDataProvider(IBasicDataProvider):
    """ Marker interface for objects that provide data to visualizations
    """


class IConnectorDataProvider(IBasicDataProvider):
    """ Marker interface for objects that provide data to visualizations
    """


VIZ_SCHEMA = json.dumps({"type": "object", "properties": {}})


@provider(IFormFieldProvider)
class IDataVisualization(model.Schema):
    """ A data visualization (chart)
    """

    visualization = JSONField(title=u"Visualization", required=False,
                              default={},
                              schema=VIZ_SCHEMA)


FACETED_SCHEMA = json.dumps({'type': 'list'})


@provider(IFormFieldProvider)
class IFacetedCollection(model.Schema):
    """ Can specify indexes to be shown as facets on a collection
    """

    facets = JSONField(
        title=_(u'Facets'),
        description=u"Facets configuration",
        schema=FACETED_SCHEMA,
        # value_type=schema.Choice(
        #     vocabulary='plone.app.contenttypes.metadatafields'),
        required=False,
    )
