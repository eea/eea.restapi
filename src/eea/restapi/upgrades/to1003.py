''' upgrade to 1003 '''
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


def transform_links(context, value, transformer):
    """Convert absolute links to resolveuid
    http://localhost:55001/plone/link-target
    ->
    ../resolveuid/023c61b44e194652804d05a15dc126f4"""


class SlateBlockTransformer:
    """SlateBlockTransformer."""

    def __init__(self, context):
        self.context = self.context

    def handle_a(self, child):
        data = child.get("data", {})
        if data.get("link", {}).get("internal", {}).get("internal_link"):
            internal_link = data["link"]["internal"]["internal_link"]
            for link in internal_link:
                link["@id"] = path2uid(self.context, link["@id"])

    def handle_link(self, child):
        if child.get("data", {}).get("url"):
            if 'resolveuid' not in child["data"]["url"]:
                logger.info("fixing type:'link' in %s",
                            self.context.absolute_url())
                child["data"]["url"] = path2uid(
                    self.context, child["data"]["url"])
                return True

    def handle_dataentity(self, child):
        if child.get('data', {}).get('provider_url'):
            if 'resolveuid' not in child['data']['provider_url']:
                child['data']['provider_url'] = path2uid(
                    self.context,
                    child['data']['provider_url'])
                return True

    def __call__(self, block):
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
    order = blocks_layout.get('items', [])
    blocks = getattr(obj, 'blocks', {})

    out = []
    for id in order:
        out.append((id, blocks[id]))

    return out


class BlocksTraverser:
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

                self.handle_subblocks(block_value, visitor)

        if "blocks" in block_value:
            for block_value in block_value['blocks'].values():
                if visitor(block_value):
                    self.context._p_changed = True

                self.handle_subblocks(block_value, visitor)


def migrate_provider_url(obj):
    """ Fixes the 'provider_url' to make it a resolveuid-based link
    """

    pass


def run_upgrade(setup_context):
    """ run upgrade to 1003
    """

    # fixes = [migrate_slate_elements, migrate_provider_url]

    site = setup_context.getSite()
    brains = site.portal_catalog.unrestrictedSearchResults(_nonsense=True)

    for i, brain in enumerate(brains):
        obj = brain.getObject()

        if hasattr(obj, 'blocks') and hasattr(obj, 'blocks_layout'):
            traverser = BlocksTraverser(obj)

            slate_fixer = SlateBlockTransformer(obj)
            traverser(slate_fixer)

        if i % 200 == 0:
            transaction.savepoint()
