""" search module """

from plone.app.portlets.portlets.search import Renderer
from . import PortletSerializer


class SearchPortletSerializer(PortletSerializer):
    """ Portlet serializer for search portlet
    """

    def __call__(self):
        res = super(SearchPortletSerializer, self).__call__()
        renderer = SearchPortletRenderer(
            self.context,
            self.request,
            None,
            None,
            self.assignment
        )

        res['classicportlet'] = renderer.render()

        return res


class SearchPortletRenderer(Renderer):
    """ search portlet renderer """
    def render(self):
        """ render """
        res = {
            'enable_livesearch': self.enable_livesearch()
        }
        return res
