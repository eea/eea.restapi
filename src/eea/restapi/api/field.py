from plone.restapi.deserializer import json_body
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service
from zope.component import queryMultiAdapter


class FieldGet(Service):
    """ Given a field name in the request, returns its serialized value
    """

    def reply(self):
        data = json_body(self.request)

        name = data.get('name') or self.request.form.get('name')

        if name is None:
            raise Exception("No field name provided")

        res = {
            '@id': self.context.absolute_url() + '#' + name,
        }

        serializer = queryMultiAdapter(
            (self.context, self.request), ISerializeToJson)

        if serializer is None:
            self.request.response.setStatus(501)

            return dict(error=dict(message="No serializer available."))

        ser = serializer(version=self.request.get("version"))
        res[name] = ser[name]

        return res
