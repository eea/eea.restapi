from plone.restapi.types.adapters import DefaultJsonSchemaProvider
from plone.restapi.types.interfaces import IJsonSchemaProvider
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@adapter(Interface, Interface, Interface)
@implementer(IJsonSchemaProvider)
class GenericSchemaValueAdapter(DefaultJsonSchemaProvider):
    def __init__(self, field, context, request):
        self.field = field
        self.context = context
        self.request = request

    def get_schema(self):
        return {}
