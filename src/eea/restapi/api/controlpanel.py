""" An extension to list all the configlets that are not supported by
plone.restapi, with a link to their fallback API implementation
"""

from plone.restapi.controlpanels import IControlpanel
from plone.restapi.interfaces import IJsonCompatible
from plone.restapi.services import Service
from Products.CMFCore.utils import getToolByName
from zope.component import getAdapters


class ControlpanelFallbackGet(Service):

    def get_controlpanel_adapters(self):
        adapters = getAdapters(
            (self.context, self.request), provided=IControlpanel)

        for name, panel in adapters:
            panel.__name__ = name
            yield name, panel

    def available_controlpanels(self):
        panels = dict(self.get_controlpanel_adapters())
        panels_by_configlet = dict(
            [(p.configlet_id, name) for name, p in panels.items()]
        )

        pctool = getToolByName(self.context, "portal_controlpanel")

        for group in pctool.getGroups():
            for action_data in pctool.enumConfiglets(group=group["id"]):
                if action_data['id'] not in panels_by_configlet:
                    yield {
                        '@id': action_data['url'],
                        'title': action_data['title'],
                        'group': group['title'],
                    }

    def reply(self):
        panels = self.available_controlpanels()

        return IJsonCompatible(list(panels))
