# -*- coding: utf-8 -*-
''' siblings module '''

from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class Siblings(object):
    ''' siblings object '''
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
    ''' siblings - get '''
    def reply(self):
        ''' reply '''
        siblings = Siblings(self.context, self.request)

        return siblings(expand=True)["siblings"]
