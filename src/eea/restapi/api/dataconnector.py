# -*- coding: utf-8 -*-


from eea.restapi.interfaces import IBasicDataProvider
from eea.restapi.interfaces import IDataProvider
from plone.restapi.deserializer import json_body
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


def filter_data(data, filters):
    return data


@implementer(IExpandableElement)
@adapter(IBasicDataProvider, Interface)
class ConnectorData(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {
            "connector-data": {
                "@id": "{}/@connector-data".format(self.context.absolute_url())
            }
        }

        if not expand:
            return result

        connector = IDataProvider(self.context)
        result['connector-data']["data"] = connector.provided_data

        return result


class ConnectorDataGet(Service):
    def reply(self):
        data = ConnectorData(self.context, self.request)

        return data(expand=True)["connector-data"]


class ConnectorDataPost(Service):
    def reply(self):
        cd = ConnectorData(self.context, self.request)
        qs = json_body(self.request)['query']

        raw_data = cd(expand=True)

        data = filter_data(raw_data["connector-data"]['data'], qs)
        cd['connector-data']['data'] = data

        return cd
