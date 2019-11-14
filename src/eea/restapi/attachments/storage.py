from persistent.mapping import PersistentMapping
from zope.annotation.factory import factory
from zope.component import adapter
from zope.interface import implements

from Acquisition import Implicit
from OFS.Folder import Folder

from .interfaces import (IAttachmentStorage, IHasAttachments, IHasSliderImages,
                         ISliderImagesStorage)

ATTACHMENTS_KEY = 'restapi.attachments'
SLIDER_KEY = 'slider.images.storage'


@adapter(IHasSliderImages)
class SliderImages(PersistentMapping):
    """ Slider images stored in a persistent mapping
    """
    implements(ISliderImagesStorage)


slides_annotation_storage = factory(SliderImages, key=SLIDER_KEY)


@adapter(IHasAttachments)
class AttachmentStorage(Folder, Implicit):
    """ Slider images stored in a persistent mapping
    """
    implements(IAttachmentStorage)


attachments_annotation_storage = factory(AttachmentStorage,
                                         key=ATTACHMENTS_KEY)
