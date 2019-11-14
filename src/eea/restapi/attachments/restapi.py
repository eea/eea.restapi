from random import randint

from zope.component import queryMultiAdapter
from zope.interface import alsoProvides

import plone.protect.interfaces
from DateTime import DateTime
from plone.restapi.deserializer import json_body
from plone.restapi.exceptions import DeserializationError
from plone.restapi.interfaces import IDeserializeFromJson, ISerializeToJson
from plone.restapi.services import Service
from plone.restapi.services.content.get import ContentGet

from .content import AttachedFile, AttachedImage, AttachmentFolder
from .interfaces import IAttachmentStorage


class AttachmentsPOST(Service):
    """ Creates a new content object.
    """

    def reply(self):
        data = json_body(self.request)
        container = str(data['@container'])

        storage = IAttachmentStorage(self.context)
        storage = storage.__of__(self.context)

        if container not in storage.keys():
            folder = AttachmentFolder()
            folder.__name__ = folder.id = container
            # folder.__parent__ = self.context
            storage[container] = folder
        else:
            folder = storage[container]

        folder = folder.__of__(storage)

        # Disable CSRF protection

        if "IDisableCSRFProtection" in dir(plone.protect.interfaces):
            alsoProvides(
                self.request, plone.protect.interfaces.IDisableCSRFProtection)

        if 'image' in data['file']['content-type']:
            obj = AttachedImage()
        else:
            obj = AttachedFile()

        obj = obj.__of__(folder)

        now = DateTime()

        # # Update fields
        deserializer = queryMultiAdapter((obj, self.request),
                                         IDeserializeFromJson)

        if deserializer is None:
            self.request.response.setStatus(501)

            return dict(
                error={'message': "Cannot deserialize type Attachment"}
            )
        try:
            deserializer(validate_all=True, create=True)
        except DeserializationError as e:
            self.request.response.setStatus(400)

            return dict(error=dict(type="DeserializationError",
                                   message=str(e)))

        _id = "f.{}.{}{:04d}".format(
            now.strftime("%Y-%m-%d"),
            str(now.millis())[7:],
            randint(0, 9999),
        )
        # obj.__parent__ = folder
        obj.__name__ = _id
        obj.id = _id
        folder[_id] = obj

        self.request.response.setStatus(201)
        self.request.response.setHeader("Location", obj.absolute_url())

        serializer = queryMultiAdapter((obj, self.request), ISerializeToJson)

        if not serializer:
            self.request.response.setStatus(400)

            return dict(error=dict(type="SerializationError",
                                   message=u'No serializer found'))

        serialized_obj = serializer()

        return serialized_obj


class AttachmentsGET(Service):
    """ Get the available transactions
    """

    def reply(self):
        storage = IAttachmentStorage(self.context)
        storage = storage.__of__(self.context)

        service = ContentGet()

        service.context = storage
        service.request = self.request

        return service.reply()
