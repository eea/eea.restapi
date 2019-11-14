from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

from Acquisition import Implicit
from OFS.OrderedFolder import OrderedFolder
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.interfaces import IContentish

from .interfaces import (IAttachedFile, IAttachedImage, IAttachment,
                         IAttachmentFolder)


class Attachment(SimpleItem):
    """ Attachment implementation
    """
    implements(IAttachment, IContentish)

    file = FieldProperty(IAttachment['file'])
    text = FieldProperty(IAttachment['text'])


class AttachedFile(Attachment):
    """ Attachment implementation
    """
    implements(IAttachedFile)

    file = FieldProperty(IAttachedFile['file'])


class AttachedImage(Attachment):
    """ Attachment implementation
    """
    implements(IAttachedImage)

    file = FieldProperty(IAttachedImage['file'])


class AttachmentFolder(OrderedFolder, Implicit):
    """
    """
    implements(IAttachmentFolder)

    def getPhysicalPath(self):
        # override, to be able to provide a fake name for the physical path
        # should probably set this as folder id
        path = super(AttachmentFolder, self).getPhysicalPath()

        res = tuple([''] + [bit for bit in path[1:] if bit])
        path = () + res[:-1] + ('++attachment++' + path[-1], )

        return path
