# -*- coding: utf-8 -*-
''' searc module '''
from plone.restapi.services.search.get import SearchGet as BaseSearchGet


class SearchGet(BaseSearchGet):
    ''' search - get '''
    def reply(self):
        ''' reply '''
        # this instructs the SummarySerializer to include breadcrumb
        # information
        self.request.set('is_search', True)
        self.request.form.update({
            'metadata_fields': '_all',
        })

        return super(SearchGet, self).reply()
