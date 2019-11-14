from eea.restapi.interfaces import IEEARestapiLayer
from plone.dexterity.interfaces import IDexterityContainer
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.serializer.dxcontent import SerializeFolderToJson
from plone.restapi.serializer.dxcontent import SerializeToJson
from zope.component import adapter
from zope.interface import providedBy


@adapter(IDexterityContent, IEEARestapiLayer)
class DexterityContentSerializer(SerializeToJson):
    def __call__(self, version=None, include_items=True):
        res = super(DexterityContentSerializer, self).__call__(version,
                                                               include_items)
        res['@provides'] = ['{}.{}'.format(I.__module__, I.__name__)
                            for I in providedBy(self.context)]

        return res


@adapter(IDexterityContainer, IEEARestapiLayer)
class DexterityContainerSerializer(SerializeFolderToJson):
    def __call__(self, version=None, include_items=True):
        res = super(DexterityContainerSerializer, self).__call__(version,
                                                                 include_items)
        res['@provides'] = ['{}.{}'.format(I.__module__, I.__name__)
                            for I in providedBy(self.context)]

        return res
