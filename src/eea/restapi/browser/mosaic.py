from Products.Five.browser import BrowserView

import json


class MosaicTilesView(BrowserView):
    """ A fallback view for mosaic pages
    """

    def blocks(self):
        return json.loads(getattr(self.context, 'blocks', '{}'))
