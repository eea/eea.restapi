''' content module '''
from Acquisition import Implicit
from OFS.OrderedFolder import OrderedFolder
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.interfaces import IContentish
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty
from .interfaces import IAttachedFile
from .interfaces import IAttachedImage
from .interfaces import IAttachment
from .interfaces import IAttachmentFolder


@implementer(IAttachment, IContentish)
class Attachment(SimpleItem):
    """ Attachment implementation
    """

    file = FieldProperty(IAttachment['file'])
    text = FieldProperty(IAttachment['text'])


@implementer(IAttachedFile)
class AttachedFile(Attachment):
    """ Attachment implementation
    """

    file = FieldProperty(IAttachedFile['file'])


@implementer(IAttachedImage)
class AttachedImage(Attachment):
    """ Attachment implementation
    """

    file = FieldProperty(IAttachedImage['file'])


@implementer(IAttachmentFolder)
class AttachmentFolder(OrderedFolder, Implicit):
    """ Attachment folder
    """

    def getPhysicalPath(self):
        ''' return physical path
        override, to be able to provide a fake name for the physical path
        should probably set this as folder id
        '''
        path = super(AttachmentFolder, self).getPhysicalPath()

        res = tuple([''] + [bit for bit in path[1:] if bit])
        path = () + res[:-1] + ('++attachment++' + path[-1], )

        return path
