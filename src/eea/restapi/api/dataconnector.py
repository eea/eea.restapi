# -*- coding: utf-8 -*-


from eea.restapi.interfaces import IBasicDataProvider
from eea.restapi.interfaces import IDataProvider
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
        result['connector-data']["data"] = filter_data(connector.provided_data,
                                                       self.request.form)

        return result


class ConnectorDataGet(Service):
    def reply(self):
        import pdb
        pdb.set_trace()
        data = ConnectorData(self.context, self.request)

        return data(expand=True)["connector-data"]
