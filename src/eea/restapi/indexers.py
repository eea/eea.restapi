from plone import api
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.app.contenttypes.indexers import SearchableText
from plone.indexer.decorator import indexer
from plone.restapi.behaviors import IBlocks
from plone.restapi.indexers import SearchableText_blocks

import logging
import six


logger = logging.getLogger('eea.restapi')


@indexer(ILeadImage)
def lead_image(obj):
    return obj.image and obj.image.filename


def get_bytestring(text):
    if six.PY2:
        if isinstance(text, six.text_type):
            text = text.encode("utf-8", "replace")

    return text


def transform_text(text, portal_transforms=None):
    if not text:
        return ''

    if not portal_transforms:
        portal_transforms = api.portal.get_tool(name='portal_transforms')

    # Output here is a single <p> which contains <br /> for newline
    data = portal_transforms.convertTo('text/plain', text,
                                       mimetype='text/html')
    converted = data.getData()

    return converted or ''


@indexer(IBlocks)
def custom_SearchableText_blocks(obj):
    blocks = [b for b in obj.blocks.values() if b.get('@type') == u'cktext']
    portal_transforms = api.portal.get_tool(name='portal_transforms')

    try:
        searchable_text = SearchableText_blocks(obj)()
    except:
        searchable_text = ''

    blocks_text = [searchable_text] + [
        transform_text(b.get('cktext', ''), portal_transforms)

        for b in blocks
    ]

    text = " ".join([get_bytestring(t) for t in blocks_text])

    return text
