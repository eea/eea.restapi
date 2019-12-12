""" Overrides for the default Plone serialization
"""

from eea.restapi.interfaces import IEEARestapiLayer
from plone.dexterity.interfaces import IDexterityContainer
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer import dxcontent
from zope.component import adapter
from zope.interface import implementer
from zope.interface import providedBy


@implementer(ISerializeToJson)
@adapter(IDexterityContent, IEEARestapiLayer)
class SerializeToJson(dxcontent.SerializeToJson):
    def __call__(self, version=None, include_items=True):
        res = super(SerializeToJson, self).__call__(version, include_items)

        if "fullobjects" in self.request.form:
            res['@provides'] = ['{}.{}'.format(I.__module__, I.__name__)
                                for I in providedBy(self.context)]

        if self.context.getLayout() != 'compositepage_view':
            if 'blocks' in res:
                del res['blocks']

            if 'blocks_layout' in res:
                del res['blocks_layout']

        return res


@implementer(ISerializeToJson)
@adapter(IDexterityContainer, IEEARestapiLayer)
class SerializeFolderToJson(dxcontent.SerializeFolderToJson):
    def __call__(self, version=None, include_items=True):
        res = super(SerializeFolderToJson, self).__call__(
            version, include_items)

        if "fullobjects" in self.request.form:
            res['@provides'] = ['{}.{}'.format(I.__module__, I.__name__)
                                for I in providedBy(self.context)]

        if self.context.getLayout() != 'compositepage_view':
            if 'blocks' in res:
                del res['blocks']

            if 'blocks_layout' in res:
                del res['blocks_layout']

        return res
