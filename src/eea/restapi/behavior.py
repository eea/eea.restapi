""" behavior module """
import logging
from plone.app.dexterity.behaviors.metadata import DCFieldProperty
from plone.app.dexterity.behaviors.metadata import MetadataBase
from .interfaces import IFacetedCollection
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
