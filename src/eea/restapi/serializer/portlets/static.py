""" static module """

from plone.portlet.static.static import Renderer
from . import PortletSerializer


class StaticTextPortletSerializer(PortletSerializer):
    """ Portlet serializer for static portlet
    """

    def __call__(self):
        res = super(StaticTextPortletSerializer, self).__call__()
        renderer = StaticTextPortletRenderer(
            self.context,
            self.request,
            None,
            None,
            self.assignment
        )

        res['statictextportlet'] = renderer.render()

        return res


class StaticTextPortletRenderer(Renderer):
    """ Static text portlet renderer """
    def render(self):
        """ render """
        res = {
            'text': self.transformed(),
        }

        return res
