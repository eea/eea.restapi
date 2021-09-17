''' collection module '''
from eea.restapi.interfaces import IEEARestapiLayer
from plone.app.contenttypes.interfaces import ICollection
from plone.restapi.batching import HypermediaBatch
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.deserializer import boolean_value
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
        result = super(SerializeCollectionToJson,
                       self).__call__(version=version)

        include_items = self.request.form.get("include_items", include_items)
        include_items = boolean_value(include_items)
        # {u'i': u'portal_type',
        #         u'o': u'plone.app.querystring.operation.selection.any',
        #         u'v': [u'Document']
        custom_query = {}       # TO DO: needs to read custom query from body
        if include_items:
            results = self.context.results(batch=False,
                                           custom_query=custom_query)
            batch = HypermediaBatch(self.request, results)

            result["items_total"] = batch.items_total
            if batch.links:
                result["batching"] = batch.links

            if "fullobjects" in list(self.request.form):
                result["items"] = [
                    getMultiAdapter(
                        (brain.getObject(), self.request), ISerializeToJson
                    )()
                    for brain in batch
                ]
            else:
                result["items"] = [
                    getMultiAdapter(
                        (brain, self.request), ISerializeToJsonSummary)()
                    for brain in batch
                ]
        return result
