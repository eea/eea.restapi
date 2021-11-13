''' upgrade to 1003 '''
import json
from plone import api
import transaction
from plone.restapi.deserializer.utils import path2uid
from collections import deque
import logging

logger = logging.getLogger('eea.restapi.migration')

# from plone.restapi.deserializer.blocks import ResolveUIDSerializerBase


def iterate_children(value):
    """iterate_children.

    :param value:
    """
    queue = deque(value)

    while queue:
        child = queue.pop()
        yield child
        if child.get("children"):
            queue.extend(child["children"] or [])


class SlateBlockTransformer(object):
    """SlateBlockTransformer."""

    def __init__(self, context):
        self.context = context

    def handle_a(self, child):
        """Convert absolute links to resolveuid
        http://localhost:55001/plone/link-target
        ->
        ../resolveuid/023c61b44e194652804d05a15dc126f4"""

        dirty = False

        data = child.get("data", {})
        if data.get("link", {}).get("internal", {}).get("internal_link"):
            internal_link = data["link"]["internal"]["internal_link"]
            for link in internal_link:
                if 'resolveuid' not in link['@id']:
                    old = link['@id']
                    link["@id"] = path2uid(self.context, link["@id"])
                    logger.info(
                        "fixing type:'internal_link' in %s (%s) => (%s)",
                        self.context.absolute_url(), old, link["@id"]
                    )
                dirty = True

        return dirty

    def handle_link(self, child):
        if child.get("data", {}).get("url"):
            if 'resolveuid' not in child["data"]["url"]:
                old = child["data"]["url"]
                child["data"]["url"] = path2uid(
                    self.context, child["data"]["url"])
                logger.info("fixing type:'link' in %s (%s) => (%s)",
                            self.context.absolute_url(),
                            old, child["data"]["url"])
                return True

    def handle_dataentity(self, child):
        if child.get('data', {}).get('provider_url'):
            if 'resolveuid' not in child['data']['provider_url']:
                old = child['data']['provider_url']
                child['data']['provider_url'] = path2uid(
                    self.context,
                    child['data']['provider_url'])

                logger.info("fixing type:'dataentity' in %s (%s) => (%s)",
                            self.context.absolute_url(), old,
                            child['data']['provider_url'])
                return True

    def __call__(self, block):
        if (block or {}).get('@type') != 'slate':
            return
        if 'value' not in block:        # avoid empty blocks
            return
        value = block['value']
        children = iterate_children(value or [])
        status = []

        for child in children:
            node_type = child.get("type")
            if node_type:
                handler = getattr(self, f"handle_{node_type}", None)
                if handler:
                    status.append(handler(child))

        return any(status)


def get_blocks(obj):
    blocks_layout = getattr(obj, 'blocks_layout', {})

    if isinstance(blocks_layout, str):
        blocks_layout = json.loads(blocks_layout)
        obj.blocks_layout = blocks_layout
        obj._p_changed = True
        logger.info('Converted str blocks_layout for % s',
                    obj.absolute_url())

    order = blocks_layout.get('items', [])

    blocks = getattr(obj, 'blocks', {})
    if isinstance(blocks, str):
        blocks = json.loads(blocks)
        obj.blocks = blocks
        obj._p_changed = True
        logger.info('Converted str blocks for % s',
                    obj.absolute_url())

    out = []
    for id in order:
        out.append((id, blocks[id]))

    return out


class BlocksTraverser(object):
    def __init__(self, context):
        self.context = context

    def __call__(self, visitor):

        for (bid, block_value) in get_blocks(self.context):

            if visitor(block_value):
                self.context._p_changed = True

            self.handle_subblocks(block_value, visitor)

    def handle_subblocks(self, block_value, visitor):
        if "data" in block_value and isinstance(block_value["data"], dict) \
                and "blocks" in block_value["data"]:
            for block in block_value["data"]["blocks"].values():
                if visitor(block):
                    self.context._p_changed = True

                self.handle_subblocks(block, visitor)

        if "blocks" in block_value:
            for block in block_value['blocks'].values():
                if visitor(block):
                    self.context._p_changed = True

                self.handle_subblocks(block, visitor)


class ResolveUIDDeserializerBase(object):
    """The "url" smart block field.

    This is a generic handler. In all blocks, it converts any "url"
    field from using resolveuid to an "absolute" URL
    """

    order = 1
    block_type = None
    fields = ["url", "href", "provider_url"]

    def __init__(self, context):
        self.context = context

    def __call__(self, block):
        dirty = False
        # Convert absolute links to resolveuid
        for field in self.fields:
            link = block.get(field, "")
            if link and isinstance(link, str):
                if 'resolveuid' not in link:
                    block[field] = path2uid(context=self.context, link=link)
                    logger.info("fixing block field:'%s' in %s (%s) => (%s)",
                                field, self.context.absolute_url(), link,
                                block[field])
            elif link and isinstance(link, list):
                # Detect if it has an object inside with an
                # "@id" key (object_widget)
                if len(link) > 0 and isinstance(link[0], dict) \
                        and "@id" in link[0]:
                    for item in link:
                        if 'resolveuid' not in item['@id']:
                            old = item['@id']
                            item["@id"] = path2uid(
                                context=self.context, link=item["@id"]
                            )
                            dirty = True
                            logger.info(
                                "fixing block field:'%s' in %s (%s) => (%s)",
                                field, self.context.absolute_url(), old,
                                item['@id'])
                elif len(link) > 0 and isinstance(link[0], str):
                    dirty = any(
                        ['resolveuid' not in bit for bit in link]) or dirty
                    block[field] = [
                        path2uid(context=self.context, link=item)
                    ]

        return dirty


def run_upgrade(setup_context):
    """ run upgrade to 1003
    """

    # fixes = [migrate_slate_elements, migrate_provider_url]

    catalog = api.portal.get_tool("portal_catalog")

    brains = catalog(_nonsense=True)

    for i, brain in enumerate(brains):
        obj = brain.getObject()

        if hasattr(obj, 'blocks') and hasattr(obj, 'blocks_layout'):
            traverser = BlocksTraverser(obj)

            slate_fixer = SlateBlockTransformer(obj)
            traverser(slate_fixer)

            resolveuid_fixer = ResolveUIDDeserializerBase(obj)
            traverser(resolveuid_fixer)

        if i % 200 == 0:
            transaction.savepoint()
