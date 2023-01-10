''' handlers module '''

# from plone.app.linkintegrity.utils import referencedRelationship
import json
import logging
from Acquisition import aq_base
from plone.api.exc import CannotGetPortalError
from zope.component import queryAdapter
from .interfaces import IBlockValidator


logger = logging.getLogger('eea.restapi')

_marker = object()


def validate_blocks(obj, event):
    ''' validate blocks '''

    base = aq_base(obj)
    blocks = getattr(base, 'blocks', _marker)

    if blocks in (_marker, None):
        return

    res = {}

    try:
        # blocks is *sometimes* a json encoded string
        blocks = json.loads(blocks)
    except Exception:
        pass
    for k, v in blocks.items():
        validator = queryAdapter(obj, IBlockValidator, name=v.get('@type', ''))

        if validator is not None:
            try:
                res[k] = validator.clean(v)
            except CannotGetPortalError:
                res[k] = v
        else:
            res[k] = v

    obj.blocks = res
