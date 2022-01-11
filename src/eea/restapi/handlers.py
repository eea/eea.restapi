''' handlers module '''

# from plone.app.linkintegrity.utils import referencedRelationship
import json
import logging
from Acquisition import aq_base
from plone import api
from plone.api.exc import CannotGetPortalError
from plone.app.linkintegrity.handlers import updateReferences
from plone.app.linkintegrity.utils import ensure_intid
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.component import queryAdapter
from zope.intid.interfaces import IIntIds
from .interfaces import IBlockValidator


logger = logging.getLogger('eea.restapi')


def handle_clonedblock_content_added(obj, event):
    ''' handle clonedblock content added '''

    portal_type = obj.portal_type
    uid = api.portal.get_registry_record(
        'eea.clonedblocks.' + portal_type, default=None
    )
    source = api.content.get(UID=uid)
    intids = getUtility(IIntIds)

    source_id = ensure_intid(source, intids)
    relation = RelationValue(source_id)

    updateReferences(obj, [relation])

    logger.info("Added clone relationship for %r ", obj)


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
