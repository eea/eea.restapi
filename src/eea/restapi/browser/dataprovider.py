from eea.restapi.interfaces import IDataProvider
from Products.Five.browser import BrowserView


class DataProviderView(BrowserView):
    """ Basic view for the DataConnector
    """

    def data(self):
        dataprovider = IDataProvider(self.context)

        return dataprovider.provided_data
