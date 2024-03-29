# -*- coding: utf-8 -*-
""" get module """
from plone.restapi.interfaces import IJsonCompatible
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.services import Service
from eea.restapi.services.portlets.utils import get_portletmanagers
from eea.restapi.services.portlets.utils import manager_by_name
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class PortletsGet(Service):
    """ Portlets Get service """
    portletmanager_id = None

    def publishTraverse(self, request, name):  # noqa
        """ publish traverse """
        if name:
            self.portletmanager_id = name

        return self

    def reply(self):
        """ reply """
        if self.portletmanager_id:
            return self.reply_portletmanager()

        def serialize(portletmanagers):
            """ serialize """
            for manager in portletmanagers:
                serializer = queryMultiAdapter(
                    (manager[1], self.context, self.request),
                    ISerializeToJsonSummary)
                yield serializer()

        portletmanagers = get_portletmanagers()

        return IJsonCompatible(list(serialize(portletmanagers)))

    def reply_portletmanager(self):
        """ reply portletmanager """
        manager = manager_by_name(self.context, self.portletmanager_id)

        if manager is None:
            self.request.response.setStatus(404)
            return None
        serializer = queryMultiAdapter((manager, self.context, self.request),
                                       ISerializeToJson)

        if serializer is None:
            self.request.response.setStatus(501)
            return dict(error=dict(message='No serializer available.'))

        return serializer()
