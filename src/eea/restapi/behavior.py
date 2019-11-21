from .interfaces import IConnectorDataProvider
from .interfaces import IDataConnector
from .interfaces import IDataProvider
from .interfaces import IDataVisualization
from .interfaces import IFileDataProvider
from collections import defaultdict
from io import StringIO
from plone.app.dexterity.behaviors.metadata import DCFieldProperty
from plone.app.dexterity.behaviors.metadata import MetadataBase
from plone.dexterity.interfaces import IDexterityContent
from plone.rfc822.interfaces import IPrimaryFieldInfo
from zope.component import adapter
from zope.interface import implementer

import csv
import logging
import requests


logger = logging.getLogger(__name__)


@implementer(IDataConnector)
@adapter(IDexterityContent)
class DataConnector(MetadataBase):
    """ Allow data connectivity to discodata

    See http://discomap.eea.europa.eu/App/SqlEndpoint/Browser.aspx
    """

    endpoint_url = DCFieldProperty(IDataConnector['endpoint_url'])
    sql_query = DCFieldProperty(IDataConnector['sql_query'])


@adapter(IConnectorDataProvider)
@implementer(IDataProvider)
class DataProviderForConnectors(object):
    def __init__(self, context):
        self.context = context

    def _get_data(self):
        # query = urllib.parse.quote_plus(self.query)

        try:
            req = requests.post(self.context.endpoint_url,
                                data={'sql': self.context.sql_query})
            res = req.json()
        except Exception:
            logger.exception("Error in requestion data")
            res = {'results': []}

        if 'errors' in res:
            return {'results': []}

        return res

    def change_orientation(self, data):
        res = {}

        if not data:
            return res

        keys = data[0].keys()

        # in-memory built, should optimize

        for k in keys:
            res[k] = [row[k] for row in data]

        return res

    @property
    def provided_data(self):
        if not self.context.sql_query:
            return []

        data = self._get_data()

        return self.change_orientation(data['results'])


@implementer(IDataProvider)
@adapter(IFileDataProvider)
class DataProviderForFiles(object):
    """ Behavior implementation for content types with a File primary field
    """

    def __init__(self, context):
        self.context = context

    @property
    def provided_data(self):
        field = IPrimaryFieldInfo(self.context)

        if not field.value:
            return []

        text = field.value.data
        f = StringIO(text.decode('utf-8'))
        try:
            reader = csv.reader(f)
        except:
            return []

        rows = list(reader)

        if not rows:
            return []

        keys = rows[0]
        res = defaultdict(list)

        for (i, k) in enumerate(keys):
            for row in rows[1:]:
                res[k].append(row[i])

        return res


class DataVisualization(MetadataBase):
    """ Standard Fise Metadata adaptor
    """

    visualization = DCFieldProperty(IDataVisualization['visualization'])
