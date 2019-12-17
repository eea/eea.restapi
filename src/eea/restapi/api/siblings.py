# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone import api
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from plone.restapi.services.navigation.get import CustomNavtreeStrategy
from plone.restapi.services.navigation.get import NavigationTreeQueryBuilder
from Products.CMFPlone.browser.navtree import NavtreeQueryBuilder
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface


# class NavigationTreeQueryBuilder(NavtreeQueryBuilder):
#     """Build a folder tree query
#     """
#
#     def __init__(self, context, depth):
#         NavtreeQueryBuilder.__init__(self, context)
#         self.query["path"] = {
#             "query": "/".join(context.getPhysicalPath()),
#             "navtree_start": 1,
#             "depth": depth - 1,
#         }


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class Siblings(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {
            "siblings": {
                "@id": "{}/@siblings".format(self.context.absolute_url())
            }
        }

        # unline other expandable elements, expand is always True here

        if ('fullobjects' not in self.request.form) and not expand:
            return result

        portal = api.portal.get()

        if self.context is portal:
            return result

        tabObj = self.context.aq_parent.aq_inner
        items = tabObj.restrictedTraverse(
            'localtabs_view').topLevelTabs(actions=())

        result["siblings"]["items"] = items

        return result


class SiblingsGet(Service):
    def reply(self):
        siblings = Siblings(self.context, self.request)

        return siblings(expand=True)["siblings"]
