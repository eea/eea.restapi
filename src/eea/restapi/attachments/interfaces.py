from zope.interface import Interface

from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobFile, NamedBlobImage
from plone.supermodel import model

# class ISliderImagesBehavior(Interface):
#     """ Behavior for slider images
#     """


class IHasSliderImages(Interface):
    """ Marker interface for objects that provide slider images
    """


class ISliderImagesStorage(Interface):
    """ Annotation based storage for slider images
    """


class IHasAttachments(Interface):
    """ Marker interface for objects that provide file attachments
    """


class IAttachmentStorage(Interface):
    """ Annotation based storage for attachments
    """


class IAttachmentFolder(Interface):
    """
    """


class IAttachment(model.Schema):
    """
    """

    file = NamedBlobFile(title=u'Attached file',
                         description=u'', required=True)
    text = RichText(title=u"Text", description=u'', required=False)


class IAttachedImage(IAttachment):
    """
    """
    file = NamedBlobImage(title=u'Attached file',
                          description=u'', required=True)


class IAttachedFile(IAttachment):
    """
    """
