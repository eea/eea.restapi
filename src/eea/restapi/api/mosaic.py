''' mosaic module '''
from eea.restapi.interfaces import IMosaicSettings
from plone.registry.interfaces import IRegistry
from plone.restapi.services import Service
from zope.component import getUtility  # adapter, getMultiAdapter


class MosaicSettingsGet(Service):
    """ Get the mosaic settings
    """

    def reply(self):
        ''' reply '''
        proxy = getUtility(IRegistry).forInterface(IMosaicSettings)

        return {
            'styles': list(proxy.styles)
        }
