''' serializer module '''
from zope.component import adapter, getMultiAdapter, queryMultiAdapter
from zope.interface import Interface, implementer
from zope.schema import getFields

from plone.namedfile.interfaces import INamedFileField
from plone.restapi.interfaces import IFieldSerializer, ISerializeToJson
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.dxcontent import SerializeToJson
from plone.restapi.serializer.dxfields import (DefaultFieldSerializer,
                                               FileFieldSerializer,
                                               ImageFieldSerializer)

from .interfaces import (IAttachedFile, IAttachedImage, IAttachment,
                         IAttachmentFolder, IAttachmentStorage)


@implementer(ISerializeToJson)
@adapter(IAttachmentStorage, Interface)
class SerializeStorageToJson(SerializeToJson):
    '''serialize storage to json '''

    def __call__(self, version=None, include_items=True):
        result = {}
        # parent = self.context.__parent__

        # ILocation provided by the adapter locate=true registration
        context = self.context.__of__(self.context.__parent__)
        result['@id'] = '{}/@attachments'.format(
            self.context.__parent__.absolute_url())
        result['items'] = []

        for folder in context.values():
            folder = folder.__of__(context)
            fs = getMultiAdapter((folder, self.request), ISerializeToJson)()
            result['items'].append(fs)

        return result


@implementer(ISerializeToJson)
@adapter(IAttachmentFolder, Interface)
class SerializeAttachmentFolderToJson(SerializeToJson):
    ''' serialize attachment folder to json '''

    def __call__(self, version=None, include_items=True):
        result = {}
        result['@id'] = self.context.__name__
        result['items'] = []

        for folder in self.context.values():
            fs = getMultiAdapter((folder, self.request), ISerializeToJson)()
            result['items'].append(fs)

        return result


@implementer(ISerializeToJson)
@adapter(IAttachment, Interface)
class SerializeAttachmentToJson(object):
    ''' serialize attachment to json '''
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, version=None, include_items=True):
        obj = self.context
        result = {
            # '@context': 'http://www.w3.org/ns/hydra/context.jsonld',
            "@id": self.request.physicalPathToURL(obj.getPhysicalPath()),
            "id": obj.id,
        }

        iface = IAttachment

        if IAttachedFile.providedBy(obj):
            iface = IAttachedFile
        elif IAttachedImage.providedBy(obj):
            iface = IAttachedImage

        for name, field in getFields(iface).items():

            serializer = queryMultiAdapter(
                (field, obj, self.request), IFieldSerializer
            )

            assert serializer
            value = serializer()
            result[json_compatible(name)] = value

        return result


@adapter(INamedFileField, IAttachment, Interface)
@implementer(IFieldSerializer)
class AttachmentFieldSerializer(DefaultFieldSerializer):
    ''' attachment field serializer '''

    def __call__(self):
        namedfile = self.field.get(self.context)

        if namedfile is None:
            return None

        ctype = namedfile.contentType
        obj = self.context

        if 'image' in ctype:
            try:
                res = ImageFieldSerializer(self.field, obj, self.request)()
            except AttributeError:      # has been uploaded as file, not image
                res = FileFieldSerializer(self.field, obj, self.request)()
        else:
            res = FileFieldSerializer(self.field, self.context,
                                      self.request)()
        # rewrite urls, they're not generated properly
        path = obj.getPhysicalPath()
        res['@id'] = '{}'.format(self.request.physicalPathToURL(path))

        return res
