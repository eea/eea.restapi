''' summary module '''
from eea.restapi.interfaces import IEEARestapiLayer
from plone.app.contentlisting.interfaces import IContentListingObject
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer import summary
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ISerializeToJsonSummary)
@adapter(Interface, IEEARestapiLayer)
class DefaultJSONSummarySerializer(summary.DefaultJSONSummarySerializer):
    """ Override the default summary serializer to include breadcrumb info
    """

    def __call__(self):
        res = super(DefaultJSONSummarySerializer, self).__call__()

        if self.request.get('is_search') and \
                IContentListingObject.providedBy(self.context):
            breadcrumb_adapter = getMultiAdapter(
                (self.context.getObject(), self.request),
                IExpandableElement, name='breadcrumbs')

            if '@components' not in res:
                res['@components'] = {}

            res['@components'].update(breadcrumb_adapter(expand=True))

        return res
