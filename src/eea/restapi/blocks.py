""" Block serializers, deserializers and utilities
"""

from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.restapi.behaviors import IBlocks
from plone.restapi.deserializer.blocks import (
    SlateBlockTransformer, ResolveUIDDeserializerBase)
from plone.restapi.deserializer.utils import path2uid
from plone.restapi.interfaces import (
    IBlockFieldDeserializationTransformer, IBlockFieldSerializationTransformer)
from plone.restapi.serializer.blocks import ResolveUIDSerializerBase
from plone.restapi.serializer.utils import uid_to_url
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest

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
        """ """
        if child.get('data', {}).get('provider_url'):
            child['data']['provider_url'] = path2uid(
                self.context,
                child['data']['provider_url'])


@adapter(IPloneSiteRoot, IBrowserRequest)
@implementer(IBlockFieldDeserializationTransformer)
class SlatePloneRootBlockDeserializer(SlateBlockDeserializer):
    """" """
    pass


@adapter(IBlocks, IBrowserRequest)
@implementer(IBlockFieldDeserializationTransformer)
class SlateBlockSerializer(SlateBlockTransformer):
    """ Handle block transformer integration for slate elements
    """

    order = 200
    block_type = "slate"

    def handle_dataentity(self, child):
        """ """
        if child.get('data', {}).get('provider_url'):
            child['data']['provider_url'] = uid_to_url(
                child['data']['provider_url'])


@adapter(IPloneSiteRoot, IBrowserRequest)
@implementer(IBlockFieldDeserializationTransformer)
class SlatePloneRootBlockSerializer(SlateBlockSerializer):
    """ """
    pass


@adapter(IBlocks, IBrowserRequest)
@implementer(IBlockFieldDeserializationTransformer)
class PlotlyDeserializer(object):
    """ Handle block transformer integration for slate elements
    """

    order = 300
    block_type = "connected_plotly_chart"

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, block):
        uid_resolver = ResolveUIDDeserializerBase(self.context, self.request)
        block = uid_resolver(block)

        if 'chartData' in block:
            block['chartData'] = uid_resolver(block['chartData'])

        return block

# TO DO register the plotlycharts serializer/deserializers also for Plone root


@adapter(IBlocks, IBrowserRequest)
@implementer(IBlockFieldDeserializationTransformer)
class FilteredPlotlyDeserializer(PlotlyDeserializer):
    """ """
    order = 301
    block_type = "filteredConnectedPlotlyChart"


@adapter(IBlocks, IBrowserRequest)
@implementer(IBlockFieldSerializationTransformer)
class PlotlySerializer(object):
    """ Handle block transformer integration for chart blocks
    """

    order = 300
    block_type = "connected_plotly_chart"

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, block):
        uid_resolver = ResolveUIDSerializerBase(self.context, self.request)
        block = uid_resolver(block)

        if 'chartData' in block:
            block['chartData'] = uid_resolver(block['chartData'])

        return block


@adapter(IBlocks, IBrowserRequest)
@implementer(IBlockFieldDeserializationTransformer)
class FilteredPlotlySerializer(PlotlySerializer):
    """ """
    order = 301
    block_type = "filteredConnectedPlotlyChart"
