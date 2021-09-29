""" recent module """

from zope.component import getMultiAdapter
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.app.portlets.portlets.recent import Renderer
from . import PortletSerializer


class RecentPortletSerializer(PortletSerializer):
    """ Portlet serializer for news portlet
    """

    def __call__(self):
        res = super(RecentPortletSerializer, self).__call__()
        renderer = RecentPortletRenderer(
            self.context,
            self.request,
            None,
            None,
            self.assignment
        )
        res['recentportlet'] = renderer.render()

        return res


class RecentPortletRenderer(Renderer):
    """ Recent Portlet Renderer """
    def render(self):
        """ render  """
        items = []
        news = self.recent_items()
        for new in news:
            itemList = getMultiAdapter((new, self.request),
                                       ISerializeToJsonSummary)()
            itemList['date'] = new.ModificationDate
            items.append(itemList)
        res = {
            'items': items,
            'recently_modified_link': self.recently_modified_link()
        }
        return res
