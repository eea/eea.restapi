from eea.restapi.interfaces import IClonedBlocks
from eea.restapi.interfaces import IEEARestapiLayer
from plone import api
from plone.dexterity.fti import DexterityFTI
from plone.restapi.deserializer import json_body
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.dxcontent import SerializeToJson
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import implementer


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

        print(uid)
        # if uid is not None:
        #
        #     import pdb
        #     pdb.set_trace()

        return res


class CreateCloneTemplate(Service):
    """ Saves a content as a template
    """

    def reply(self):
        type_title = json_body(self.request)['typeName'].strip()
        type_id = type_title.lower().strip().replace(' ', '-')
        types_tool = api.portal.get_tool('portal_types')
        base = 'clonable_type'
        base_fti = types_tool._getOb(base)

        props = dict(base_fti.propertyItems())
        # make sure we don't share the factory

        if props['factory'] == self.context.fti.getId():
            del props['factory']

        props['title'] = type_title
        props['add_view_expr'] = props['add_view_expr'].replace(
            base,
            type_id
        )
        fti = DexterityFTI(type_id, **props)
        types_tool._setObject(fti.id, fti)

        return {}
