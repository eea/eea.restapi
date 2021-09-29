""" news module """

from DateTime import DateTime
from plone.app.portlets.portlets.news import Renderer
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.converters import json_compatible
from zope.component import getMultiAdapter
from . import PortletSerializer


class NewsPortletSerializer(PortletSerializer):
    """ Portlet serializer for news portlet
    """

    def __call__(self):
        res = super(NewsPortletSerializer, self).__call__()
        renderer = NewsPortletRenderer(
            self.context,
            self.request,
            None,
            None,
            self.assignment
        )
        res['newsportlet'] = renderer.render()

        return res


class NewsPortletRenderer(Renderer):
    """ News Portlet Renderer """
    def as_date(self, value):
        """ return value as date time """
        if value:
            if isinstance(value, DateTime):
                value = value.asdatetime()

            return json_compatible(value)
        return None

    def render(self):
        """ render """
        items = []
        brains = self.published_news_items()

        for brain in brains:
            item = getMultiAdapter(
                (brain, self.request), ISerializeToJsonSummary)()

            item['created'] = self.as_date(brain.created)
            item['effective'] = self.as_date(brain.effective)
            item['thumb'] = ''

            if self.thumb_scale and brain.getIcon:
                item['thumb'] = '{}/@@images/image/{}'.format(
                    brain.getURL(), self.thumb_scale())

            items.append(item)

        res = {
            'items': items,
            'all_news_link': self.all_news_link(),
        }

        return res
