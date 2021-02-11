# -*- coding: utf-8 -*-
''' local navigation '''
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from OFS.interfaces import IApplication
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.registry.interfaces import IRegistry
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from Products.CMFPlone.browser.interfaces import INavigationTabs
from Products.CMFPlone.browser.navtree import NavtreeQueryBuilder
from Products.CMFPlone.browser.navtree import SitemapNavtreeStrategy
from Products.CMFPlone.interfaces import INavigationSchema
from Products.Five import BrowserView
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.interface import Interface
from ..interfaces import ILocalSectionMarker


class NavigationTreeQueryBuilder(NavtreeQueryBuilder):
    """Build a folder tree query
    """

    def __init__(self, context, depth):
        NavtreeQueryBuilder.__init__(self, context)
        self.query["path"] = {
            "query": "/".join(context.getPhysicalPath()),
            "navtree_start": 1,
            "depth": depth - 1,
        }


def getNavigationRoot(context):
    ''' get navigation root '''
    return "/".join(context.getPhysicalPath())


class CustomNavtreeStrategy(SitemapNavtreeStrategy):
    ''' nothing is customized here, just this getNavigationRoot method '''

    def __init__(self, context):
        SitemapNavtreeStrategy.__init__(self, context, None)
        self.context = context
        self.bottomLevel = 0
        self.rootPath = self.getRootPath()

    def subtreeFilter(self, node):
        ''' subtree filter '''
        sitemapDecision = SitemapNavtreeStrategy.subtreeFilter(self, node)

        if sitemapDecision is False:
            return False
        depth = node.get("depth", 0)

        if depth > 0 and self.bottomLevel > 0 and depth >= self.bottomLevel:
            return False
        return True

    def getRootPath(self, topLevel=1):
        ''' get root path '''
        rootPath = getNavigationRoot(self.context)

        rootPath = contextPath = "/".join(self.context.getPhysicalPath())

        if not contextPath.startswith(rootPath):
            return None
        contextSubPathElements = contextPath[len(rootPath) + 1:]

        if contextSubPathElements:
            contextSubPathElements = contextSubPathElements.split("/")

            if len(contextSubPathElements) < topLevel:
                return None
            rootPath = (
                rootPath + "/" + "/".join(contextSubPathElements[:topLevel])
            )  # noqa
        else:
            return None

        return rootPath


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class LocalNavigation(object):
    ''' local navigation '''
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.portal = getSite()

    def get_section_root(self, context):
        ''' get section root '''
        original = context

        while not IApplication.providedBy(context):
            if ILocalSectionMarker.providedBy(context):
                return context
            context = aq_parent(context)

        return original

    def __call__(self, expand=False):
        if self.request.form.get("expand.localnavigation.depth", False):
            self.depth = int(self.request.form["expand.localnavigation.depth"])
        else:
            self.depth = 1

        result = {
            "localnavigation": {"@id": "{}/@localnavigation".format(
                self.context.absolute_url())}
        }

        if not expand:
            return result

        context = self.get_section_root(self.context)
        tabs = getMultiAdapter((context, self.request),
                               name="localtabs_view")
        items = []

        for tab in tabs.topLevelTabs():
            if self.depth > 1:
                subitems = self.getTabSubTree(
                    tabUrl=tab["url"], tabPath=tab.get("path")
                )
                items.append(
                    {
                        "title": tab.get("title", tab.get("name")),
                        "@id": tab["url"] + "",
                        "description": tab.get("description", ""),
                        "items": subitems,
                    }
                )
            else:
                items.append(
                    {
                        "title": tab.get("title", tab.get("name")),
                        "@id": tab["url"] + "",
                        "description": tab.get("description", ""),
                    }
                )
        result["localnavigation"]["items"] = items

        return result

    def getTabSubTree(self, tabUrl="", tabPath=None):
        ''' get tab subtree '''
        if tabPath is None:
            # get path for current tab's object
            tabPath = tabUrl.split(self.portal.absolute_url())[-1]

            if tabPath == "" or "/view" in tabPath:
                return ""

            if tabPath.startswith("/"):
                tabPath = tabPath[1:]
            elif tabPath.endswith("/"):
                # we need a real path, without a slash that might appear
                # at the end of the path occasionally
                tabPath = str(tabPath.split("/")[0])

            if "%20" in tabPath:
                # we have the space in object's ID that has to be
                # converted to the real spaces
                tabPath = tabPath.replace("%20", " ").strip()

        tabObj = self.portal.restrictedTraverse(tabPath, None)

        if tabObj is None:
            return ""

        strategy = CustomNavtreeStrategy(tabObj)
        queryBuilder = NavigationTreeQueryBuilder(tabObj, self.depth)
        query = queryBuilder()
        data = buildFolderTree(
            tabObj, obj=tabObj, query=query, strategy=strategy)

        return self.recurse(children=data.get("children", []), level=1)

    def recurse(self, children=None, level=0, bottomLevel=0):
        ''' recurse '''
        li = []

        for node in children:
            item = {"title": node["Title"], "description": node["Description"]}
            item["@id"] = node["getURL"]

            if bottomLevel <= 0 or level <= bottomLevel:
                nc = node["children"]
                nc = self.recurse(nc, level + 1, bottomLevel)

                if nc:
                    item["items"] = nc
            li.append(item)

        return li


class LocalNavigationGet(Service):
    ''' local navigation - get '''
    def reply(self):
        ''' reply '''
        navigation = LocalNavigation(self.context, self.request)

        return navigation(expand=True)["localnavigation"]


def get_url(item):
    ''' get url '''
    if not item:
        return None

    if hasattr(aq_base(item), 'getURL'):
        # Looks like a brain

        return item.getURL()

    return item.absolute_url()


def get_id(item):
    ''' get id '''
    if not item:
        return None
    getId = getattr(item, 'getId')

    if not utils.safe_callable(getId):
        # Looks like a brain
        return getId

    return getId()


def get_view_url(context):
    ''' get view url '''
    registry = getUtility(IRegistry)
    view_action_types = registry.get(
        'plone.types_use_view_action_in_listings', [])
    item_url = get_url(context)
    name = get_id(context)

    if getattr(context, 'portal_type', {}) in view_action_types:
        item_url += '/view'
        name += '/view'

    return name, item_url


@implementer(INavigationTabs)
class CatalogNavigationTabs(BrowserView):
    ''' catalog navigation tabs '''

    def _getNavQuery(self):
        ''' check whether we only want actions '''
        registry = getUtility(IRegistry)
        navigation_settings = registry.forInterface(
            INavigationSchema,
            prefix="plone",
            check=False
        )
        customQuery = getattr(self.context, 'getCustomNavQuery', False)

        if customQuery is not None and utils.safe_callable(customQuery):
            query = customQuery()
        else:
            query = {}

        query['path'] = {
            'query': getNavigationRoot(self.context),
            'depth': 1
        }
        query['portal_type'] = [t for t in navigation_settings.displayed_types]
        query['sort_on'] = navigation_settings.sort_tabs_on

        if navigation_settings.sort_tabs_reversed:
            query['sort_order'] = 'reverse'
        else:
            query['sort_order'] = 'ascending'

        if navigation_settings.filter_on_workflow:
            query['review_state'] = navigation_settings.workflow_states_to_show

        query['is_default_page'] = False

        if not navigation_settings.nonfolderish_tabs:
            query['is_folderish'] = True

        return query

    # pylint: disable=too-many-locals
    def topLevelTabs(self, actions=None, category='portal_tabs'):
        ''' top level tabs '''
        context = aq_inner(self.context)
        registry = getUtility(IRegistry)
        navigation_settings = registry.forInterface(
            INavigationSchema,
            prefix="plone",
            check=False
        )
        mtool = getToolByName(context, 'portal_membership')
        member = mtool.getAuthenticatedMember().id
        catalog = getToolByName(context, 'portal_catalog')

        if actions is None:
            context_state = getMultiAdapter(
                (context, self.request),
                name=u'plone_context_state'
            )
            actions = context_state.actions(category)

        # Build result dict
        result = []
        # first the actions

        for actionInfo in actions:
            data = actionInfo.copy()
            data['name'] = data['title']
            result.append(data)

        # check whether we only want actions

        if not navigation_settings.generate_tabs:
            return result

        query = self._getNavQuery()

        rawresult = catalog.searchResults(query)

        def _get_url(item):
            """_get_url.

            :param item:
            """
            if item.getRemoteUrl and not member == item.Creator:
                return (get_id(item), item.getRemoteUrl)

            return get_view_url(item)

        # now add the content to results

        # pylint: disable=unused-variable
        for item in rawresult:
            # if item.exclude_from_nav:
            #     continue
            cid, item_url = _get_url(item)
            data = {
                'name': utils.pretty_title_or_id(context, item),
                'id': item.getId,
                'url': item_url,
                'description': item.Description,
                'review_state': item.review_state
            }
            result.append(data)

        return result
