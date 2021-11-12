''' upgrade to 1003 '''
import transaction
from plone.restapi.deserializer.blocks import ResolveUIDSerializerBase


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
        if "data" in block_value and isinstance(block_value["data"], dict):
            if "blocks" in block_value["data"]:
                for block in block_value["data"]["blocks"].values():
                    if visitor(block):
                        self.context._p_changed = True

                    self.handle_subblocks(block_value, visitor)

        if "blocks" in block_value:
            for block_value in block_value['blocks'].values():
                if visitor(block_value):
                    self.context._p_changed = True

                self.handle_subblocks(block_value, visitor)


def migrate_slate_dataentities(obj):
    pass


def migrate_provider_url(obj):
    """ Fixes the 'provider_url' to make it a resolveuid-based link
    """

    pass


def run_upgrade(setup_context):
    """ run upgrade to 1003
    """

    fixes = [migrate_slate_dataentities, migrate_provider_url]

    site = setup_context.getSite()
    brains = site.portal_catalog.unrestrictedSearchResults(_nonsense=True)

    for i, brain in enumerate(brains):
        obj = brain.getObject()

        if hasattr(obj, 'blocks') and hasattr(obj, 'blocks_layout'):
            for fixer in fixes:
                fixer(obj)

        if i % 200 == 0:
            transaction.savepoint()
