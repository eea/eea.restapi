from eea.restapi.interfaces import IClonedBlocks
from eea.restapi.interfaces import IEEARestapiLayer
from plone import api
from plone.dexterity.fti import DexterityFTI
from plone.registry import field
from plone.registry.record import Record
from plone.restapi.deserializer import json_body
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.dxcontent import SerializeToJson
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import alsoProvides
from zope.interface import implementer

import plone.protect.interfaces
import six


@implementer(ISerializeToJson)
@adapter(IClonedBlocks, IEEARestapiLayer)
class SerializeClonedBlocksToJson(SerializeToJson):
    def __call__(self, version=None, include_items=True):
        res = super(SerializeClonedBlocksToJson, self).__call__(version,
                                                                include_items)
        res['cloned_blocks'] = {}
        res['cloned_blocks_layout'] = []

        portal_type = self.context.portal_type
        uid = api.portal.get_registry_record(
            'eea.clonedblocks.' + portal_type, default=None)

        if uid:
            source = api.content.get(UID=uid)
            res['cloned_blocks'] = source.blocks
            res['cloned_blocks_layout'] = source.blocks_layout

        return res


class CreateCloneTemplate(Service):
    """ Saves a content as a template
    """

    def reply(self):
        # Disable CSRF protection

        if "IDisableCSRFProtection" in dir(plone.protect.interfaces):
            alsoProvides(
                self.request, plone.protect.interfaces.IDisableCSRFProtection)

        type_title = json_body(self.request)['typeName'].strip().capitalize()
        type_id = str(type_title.lower().strip().replace(' ', '_'))
        types_tool = api.portal.get_tool('portal_types')
        base = 'clonable_type'
        base_fti = types_tool._getOb(base)

        props = dict(base_fti.propertyItems())
        # make sure we don't share the factory

        if props['factory'] == base_fti.getId():
            del props['factory']

        props['title'] = type_title
        props['global_allow'] = True
        props['add_view_expr'] = props['add_view_expr'].replace(
            base,
            str(type_id)
        )
        fti = DexterityFTI(type_id, **props)
        types_tool._setObject(fti.id, fti)

        id = '{}/@types/{}'.format(api.portal.get().portal_url(), fti.id)

        uid = self.context.UID()

        registry = api.portal.get_tool('portal_registry')
        record = Record(field.TextLine(title=u"UID"), uid)
        registry.records['eea.clonedblocks.' + fti.id] = record

        return {'name': type_title, '@id': id}
