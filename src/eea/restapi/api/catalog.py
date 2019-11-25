from plone.api import portal
from plone.restapi.deserializer import json_body
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service
from zope.component import getMultiAdapter


class IndexValues(Service):
    """Returns the querystring search results given a p.a.querystring data.
    """

    def reply(self):
        data = json_body(self.request)

        name = data.get('name')

        if name is None:
            raise Exception("No index name provided")

        catalog = portal.get_tool(name='portal_catalog')
        values = list(catalog.uniqueValuesFor(name))

        return sorted(values)
