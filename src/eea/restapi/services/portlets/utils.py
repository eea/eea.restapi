# -*- coding: utf-8 -*-
""" utils module """
from plone.app.portlets.interfaces import IPortletTypeInterface
from plone.portlets.interfaces import IPortletManager
from zope.component import getUtilitiesFor
from zope.component import getUtility


def get_portlet_types():
    """ get portlet types """
    return getUtilitiesFor(IPortletTypeInterface)


def get_portletmanagers():
    """ get portlet managers """
    return getUtilitiesFor(IPortletManager)


def manager_by_name(context, name):
    """ get manager by name """
    return getUtility(IPortletManager,
                      name=name,
                      context=context)
