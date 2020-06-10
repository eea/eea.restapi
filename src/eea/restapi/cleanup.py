''' cleanup module '''
from plone import api


class HTMLBlockCleanup(object):
    ''' HTML Block cleanup '''
    def __init__(self, context):
        self.context = context

    def clean(self, block_value):
        ''' clean '''
        portal_transforms = api.portal.get_tool(name='portal_transforms')
        raw_html = block_value.get('html', '')
        data = portal_transforms.convertTo('text/x-html-safe', raw_html,
                                           mimetype="text/html")
        html = data.getData()
        block_value['html'] = html

        return block_value
