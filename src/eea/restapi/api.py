from .interfaces import IEEARestapiLayer
from plone.dexterity.interfaces import IDexterityContainer
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.batching import HypermediaBatch
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.dxcontent import SerializeFolderToJson
from plone.restapi.serializer.dxcontent import SerializeToJson
from plone.restapi.serializer.expansion import expandable_elements
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import providedBy

import json


@implementer(ISerializeToJson)
@adapter(IPloneSiteRoot, IEEARestapiLayer)
class SerializeSiteRootToJson(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _build_query(self):
        path = "/".join(self.context.getPhysicalPath())
        query = {
            "path": {"depth": 1, "query": path},
            "sort_on": "getObjPositionInParent",
        }

        return query

    def __call__(self, version=None):
        version = "current" if version is None else version

        if version != "current":
            return {}

        query = self._build_query()

        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog(query)

        batch = HypermediaBatch(self.request, brains)

        result = {
            # '@context': 'http://www.w3.org/ns/hydra/context.jsonld',
            "@id": batch.canonical_url,
            "id": self.context.id,
            "@type": "Plone Site",
            "title": self.context.Title(),
            "parent": {},
            "is_folderish": True,
            "description": self.context.description,
            "tiles": json.loads(getattr(self.context, "tiles", "{}")),
            "tiles_layout": json.loads(
                getattr(self.context, "tiles_layout", "{}")
            ),  # noqa
        }

        # this is the place where the code is change from the original.
        # We want to expose the layout property
        # The override might not be needed, I think (Interface) in the
        # descriminator is the browser layer.
        layout = getattr(self.context, 'layout', None)

        if layout:
            result["layout"] = layout

        # Insert expandable elements
        result.update(expandable_elements(self.context, self.request))

        result["items_total"] = batch.items_total

        if batch.links:
            result["batching"] = batch.links

        result["items"] = [
            getMultiAdapter((brain, self.request), ISerializeToJsonSummary)()

            for brain in batch
        ]
        result['@provides'] = ['{}.{}'.format(I.__module__, I.__name__)
                               for I in providedBy(self.context)]

        return result


@adapter(IDexterityContent, IEEARestapiLayer)
class DexterityContentSerializer(SerializeToJson):
    def __call__(self, version=None, include_items=True):
        res = super(DexterityContentSerializer, self).__call__(version,
                                                               include_items)
        res['@provides'] = ['{}.{}'.format(I.__module__, I.__name__)
                            for I in providedBy(self.context)]

        return res


@adapter(IDexterityContainer, IEEARestapiLayer)
class DexterityContainerSerializer(SerializeFolderToJson):
    def __call__(self, version=None, include_items=True):
        res = super(DexterityContainerSerializer, self).__call__(version,
                                                                 include_items)
        res['@provides'] = ['{}.{}'.format(I.__module__, I.__name__)
                            for I in providedBy(self.context)]

        return res
