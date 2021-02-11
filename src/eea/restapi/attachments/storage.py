""" storage """
from persistent.mapping import PersistentMapping
from plone.folder.ordered import CMFOrderedBTreeFolderBase
from zope.annotation.factory import factory
from zope.component import adapter
from zope.interface import implementer
from .interfaces import IAttachmentStorage
from .interfaces import IHasAttachments
from .interfaces import IHasSliderImages
from .interfaces import ISliderImagesStorage

# from Acquisition import Implicit
# from OFS.Folder import Folder
# from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2


ATTACHMENTS_KEY = "restapi.attachments"
SLIDER_KEY = "slider.images.storage"


@adapter(IHasSliderImages)
@implementer(ISliderImagesStorage)
class SliderImages(PersistentMapping):
    """Slider images stored in a persistent mapping"""


slides_annotation_storage = factory(SliderImages, key=SLIDER_KEY)


@adapter(IHasAttachments)
@implementer(IAttachmentStorage)
class AttachmentStorage(CMFOrderedBTreeFolderBase):  # BTreeFolder2,
    # Implicit
    """Slider images stored in a persistent mapping"""


attachments_annotation_storage = factory(
    AttachmentStorage, key=ATTACHMENTS_KEY)
