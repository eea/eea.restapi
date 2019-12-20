from plone.restapi.interfaces import IExpandableElement
from plone.restapi.interfaces import ISerializeToJson
from Products.CMFDynamicViewFTI.interfaces import ISelectableBrowserDefault
from zope.component import getMultiAdapter
from zope.interface import implementer


@implementer(IExpandableElement)
class DefaultPageExpansion(object):
    """ A data expansion for default page information
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        defaultpage = ISelectableBrowserDefault(self.context).getDefaultPage()

        if not defaultpage:
            return {}

        res = {
            'defaultpage': {
                '@id': self.context.absolute_url() + '/@defaultpage',
                'name': defaultpage,
            }
        }

        if expand or 'fullobjects' in self.request.form:
            obj = self.context.restrictedTraverse(defaultpage)
            adapter = getMultiAdapter((obj, self.request), ISerializeToJson)
            res['defaultpage']['content'] = adapter()

        return res
