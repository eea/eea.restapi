""" behavior module """
from collections import defaultdict
from io import StringIO
import csv
import logging
import requests
from eea.restapi.utils import timing
from moz_sql_parser import format as sql_format
from moz_sql_parser import parse
from plone.app.dexterity.behaviors.metadata import DCFieldProperty
from plone.app.dexterity.behaviors.metadata import MetadataBase
from plone.dexterity.interfaces import IDexterityContent
from plone.memoize import ram
from plone.rfc822.interfaces import IPrimaryFieldInfo
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from .interfaces import IConnectorDataParameters
from .interfaces import IConnectorDataProvider
from .interfaces import IDataConnector
from .interfaces import IDataProvider
from .interfaces import IDataVisualization
from .interfaces import IFacetedCollection
from .interfaces import IFileDataProvider
from .interfaces import IHTMLEmbed
from .interfaces import ISimpleFacetedCollection

logger = logging.getLogger(__name__)


def build_where_statement(wheres, operator="and"):
    """make where statement for moz_sql_parser"""
    if wheres:
        if len(wheres) == 1:
            return wheres[0]
        return {operator: wheres}
    return False

def has_required_parameters(request, context):
    """Check if required_parameters exists in form"""
    if not context.required_parameters:
        return True
    for param in context.required_parameters:
        value = None
        if context.namespace:
            value = request.form.get(
                "{}.{}".format(
                    context.namespace, param))
        if not value:
            value = request.form.get(param)
        if not value:
            return False
    return True


@implementer(IDataConnector)
@adapter(IDexterityContent)
class DataConnector(MetadataBase):
    """Allow data connectivity to discodata

    See http://discomap.eea.europa.eu/App/SqlEndpoint/Browser.aspx
    """

    endpoint_url = DCFieldProperty(IDataConnector["endpoint_url"])
    sql_query = DCFieldProperty(IDataConnector["sql_query"])
    parameters = DCFieldProperty(IDataConnector["parameters"])
    required_parameters = DCFieldProperty(IDataConnector["required_parameters"])
    namespace = DCFieldProperty(IDataConnector["namespace"])


@adapter(IConnectorDataProvider, IBrowserRequest)
@implementer(IDataProvider)
class DataProviderForConnectors(object):
    """ data provider for connectors """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @timing
    def _get_data(self):
        """_get_data."""
        # query = urllib.parse.quote_plus(self.query)

        form = self.request.form
        query = parse(self.context.sql_query)
        wheres_list = []
        data = {}

        if self.context.parameters:
            for param in self.context.parameters:
                value = None

                if self.context.namespace:
                    value = form.get(
                        "{}.{}".format(
                            self.context.namespace, param))

                if not value:
                    value = form.get(param)

                if isinstance(value, list):
                    or_wheres_list = [
                        {"eq": [param, {"literal": str(item)}]} for item in
                        value]
                    or_wheres = build_where_statement(or_wheres_list, "or")
                    if or_wheres:
                        wheres_list.append(or_wheres)
                elif value:
                    wheres_list.append(
                        {"eq": [param, {"literal": str(value)}]})

        wheres = build_where_statement(wheres_list, "and")

        if "where" in query and wheres:
            query["where"] = {"and": [query["where"], wheres]}
        elif "where" not in query and wheres:
            query["where"] = wheres

        data["query"] = sql_format(query)

        if form.get("p"):
            data["p"] = form.get("p")

        if form.get("nrOfHits"):
            data["nrOfHits"] = form.get("nrOfHits")

        try:
            req = requests.post(self.context.endpoint_url, data)
            res = req.json()
        except Exception:
            logger.exception("Error in requestion data")
            res = {"results": []}

        if "errors" in res:
            return {"results": []}

        return res

    def change_orientation(self, data):
        """ change orientation """
        res = {}

        if not data:
            return res

        keys = data[0].keys()

        # TO DO: in-memory built, should optimize

        for k in keys:
            res[k] = [row[k] for row in data]

        return res

    # TO DO: persistent caching, periodical refresh, etc
    @ram.cache(lambda func, self: (self.context.modified(), self.request.form))
    def _provided_data(self):
        """ provided data """
        if not self.context.sql_query:
            return []

        if not has_required_parameters(self.request, self.context):
            return []

        data = self._get_data()

        return self.change_orientation(data["results"])

    @property
    def provided_data(self):
        """ provided data """
        return self._provided_data()


@implementer(IDataProvider)
@adapter(IFileDataProvider, IBrowserRequest)
class DataProviderForFiles(object):
    """Behavior implementation for content types with a File primary field"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def provided_data(self):
        """ provided data """
        field = IPrimaryFieldInfo(self.context)

        if not field.value:
            return []

        text = field.value.data
        f = StringIO(text.decode("utf-8"))
        try:
            reader = csv.reader(f)
        except Exception:
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
    """Standard Fise Metadata adaptor"""

    visualization = DCFieldProperty(IDataVisualization["visualization"])


class FacetedCollection(MetadataBase):
    """Facetes based on indexes for collections"""

    facets = DCFieldProperty(IFacetedCollection["facets"])


class SimpleFacetedCollection(MetadataBase):
    """Simple Faceted Collection"""

    filter = DCFieldProperty(ISimpleFacetedCollection["filter"])


class HTMLEmbed(MetadataBase):
    """HTML Embed"""

    embed_code = DCFieldProperty(IHTMLEmbed["embed_code"])


class ConnectorDataParameters(MetadataBase):
    """Provide predefined connector data for parameters"""

    # data_parameters = DCFieldProperty(
    #     IConnectorDataParameters['data_parameters'])
    data_query = DCFieldProperty(IConnectorDataParameters["data_query"])
