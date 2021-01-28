""" indexers module """
from plone import api
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.indexer.decorator import indexer
from plone.restapi.behaviors import IBlocks
from plone.restapi.interfaces import IBlockSearchableText
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest

import logging
import six


logger = logging.getLogger("eea.restapi")


@indexer(ILeadImage)
def lead_image(obj):
    """ lead image """
    return obj.image and obj.image.filename


def get_bytestring(text):
    """ get bytestring """
    if six.PY2:
        if isinstance(text, six.text_type):
            text = text.encode("utf-8", "replace")

    return text


def transform_text(text, portal_transforms=None):
    """ transform text """
    if not text:
        return ""

    if not portal_transforms:
        portal_transforms = api.portal.get_tool(name="portal_transforms")

    # Output here is a single <p> which contains <br /> for newline
    data = portal_transforms.convertTo(
        "text/plain", text, mimetype="text/html")
    converted = data.getData()

    return converted or ""


def _extract_text(block):
    """_extract_text.

    :param block:
    """
    result = ""

    for paragraph in block.get("text", {}).get("blocks", []):
        text = paragraph["text"]

        if six.PY2:
            if isinstance(text, six.text_type):
                text = text.encode("utf-8", "replace")

            if text:
                result = " ".join((result, text))
        else:
            result = " ".join((result, text))

    return result


@implementer(IBlockSearchableText)
@adapter(IBlocks, IBrowserRequest)
class CKTextIndexer(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, block):
        raw = block.get("cktext", None)
        portal_transforms = api.portal.get_tool(name="portal_transforms")
        if raw:
            text = transform_text(raw, portal_transforms)
            return six.safe_text(text)
