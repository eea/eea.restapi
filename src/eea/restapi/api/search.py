# -*- coding: utf-8 -*-
from plone.restapi.services.search.get import SearchGet as BaseSearchGet


class SearchGet(BaseSearchGet):
    def reply(self):
        # this instructs the SummarySerializer to include breadcrumb
        # information
        self.request.set('is_search', True)
        self.request.form.update({
            'metadata_fields': '_all',
        })

        return super(SearchGet, self).reply()
