''' mosaic module '''
from Products.Five.browser import BrowserView

import json


class MosaicTilesView(BrowserView):
    """ A fallback view for mosaic pages
    """

    def blocks(self):
        ''' load blocks from json '''
        blocks = getattr(self.context.aq_inner.aq_self, 'blocks', '{}')

        return json.loads(blocks)
