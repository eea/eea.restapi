from eea.restapi.interfaces import IEEARestapiLayer
from plone.app.contenttypes.interfaces import ICollection
from plone.restapi.batching import HypermediaBatch
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.dxcontent import SerializeToJson
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer


@implementer(ISerializeToJson)
@adapter(ICollection, IEEARestapiLayer)
class SerializeCollectionToJson(SerializeToJson):
    """ Override the default serializer to include custom query
    """

    def __call__(self, version=None, include_items=True):
        # {u'i': u'portal_type',
        #         u'o': u'plone.app.querystring.operation.selection.any',
        #         u'v': [u'Document']
        collection_metadata = super(SerializeCollectionToJson, self).__call__(
            version=version
        )
        custom_query = {}       # TODO: needs to read custom query from body
        results = self.context.results(batch=False, custom_query=custom_query)
        batch = HypermediaBatch(self.request, results)

        results = collection_metadata

        if not self.request.form.get("fullobjects"):
            results["@id"] = batch.canonical_url
        results["items_total"] = batch.items_total

        if batch.links:
            results["batching"] = batch.links

        results["items"] = [
            getMultiAdapter((brain, self.request), ISerializeToJsonSummary)()

            for brain in batch
        ]

        return results
