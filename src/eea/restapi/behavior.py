""" behavior module """
import csv
import logging
from collections import defaultdict
from io import StringIO
from plone.app.dexterity.behaviors.metadata import DCFieldProperty
from plone.app.dexterity.behaviors.metadata import MetadataBase
from plone.dexterity.interfaces import IDexterityContent
from plone.rfc822.interfaces import IPrimaryFieldInfo
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from .interfaces import IFacetedCollection
from .interfaces import IFileDataProvider
from .interfaces import IHTMLEmbed
from .interfaces import ISimpleFacetedCollection


logger = logging.getLogger(__name__)


class FacetedCollection(MetadataBase):
    """Facetes based on indexes for collections"""

    facets = DCFieldProperty(IFacetedCollection["facets"])


class SimpleFacetedCollection(MetadataBase):
    """Simple Faceted Collection"""

    filter = DCFieldProperty(ISimpleFacetedCollection["filter"])


class HTMLEmbed(MetadataBase):
    """HTML Embed"""

    embed_code = DCFieldProperty(IHTMLEmbed["embed_code"])
