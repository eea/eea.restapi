from plone import api
from plone.app.linkintegrity.handlers import updateReferences
from plone.app.linkintegrity.utils import ensure_intid
from plone.app.linkintegrity.utils import referencedRelationship
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import logging


logger = logging.getLogger('eea.restapi')


def handle_clonedblock_content_added(obj, event):

    import pdb
    pdb.set_trace()
    portal_type = obj.portal_type
    uid = api.portal.get_registry_record(
        'eea.clonedblocks.' + portal_type, default=None)
    source = api.content.get(uid=uid)
    intids = getUtility(IIntIds)

    source_id = ensure_intid(source, intids)
    relation = RelationValue(source_id)

    updateReferences(obj, [relation])

    logger.info("Added clone relationship for %r ", obj)
