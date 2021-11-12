""" Block serializers, deserializers and utilities
"""
from plone.restapi.behaviors import IBlocks
from plone.restapi.deserializer.blocks import SlateBlockTransformer
from plone.restapi.deserializer.utils import path2uid
from plone.restapi.interfaces import IBlockFieldDeserializationTransformer
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from plone.restapi.serializer.utils import uid_to_url
from Products.CMFPlone.interfaces import IPloneSiteRoot

# from plone.restapi.interfaces import IFieldDeserializer
# from plone.schema import IJSONField
# from collections import deque
# from copy import deepcopy
# from plone import api


@adapter(IBlocks, IBrowserRequest)
@implementer(IBlockFieldDeserializationTransformer)
class SlateBlockDeserializer(SlateBlockTransformer):
    """ Handle block transformer integration for slate elements
    """

    order = 200
    block_type = "slate"

    def handle_dataentity(self, child):
        if child.get('data', {}).get('provider_url'):
            child['data']['provider_url'] = path2uid(
                self.context,
                child['data']['provider_url'])


@adapter(IPloneSiteRoot, IBrowserRequest)
@implementer(IBlockFieldDeserializationTransformer)
class SlatePloneRootBlockDeserializer(SlateBlockDeserializer):
    pass


@adapter(IBlocks, IBrowserRequest)
@implementer(IBlockFieldDeserializationTransformer)
class SlateBlockSerializer(SlateBlockTransformer):
    """ Handle block transformer integration for slate elements
    """

    order = 200
    block_type = "slate"

    def handle_dataentity(self, child):
        if child.get('data', {}).get('provider_url'):
            child['data']['provider_url'] = uid_to_url(
                child['data']['provider_url'])


@adapter(IPloneSiteRoot, IBrowserRequest)
@implementer(IBlockFieldDeserializationTransformer)
class SlatePloneRootBlockSerializer(SlateBlockSerializer):
    pass
