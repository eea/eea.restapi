''' traversing '''
from six.moves import urllib
from plone.rest.traverse import RESTWrapper
from zExceptions import NotFound
from zope.traversing.namespace import SimpleHandler
from .interfaces import IAttachmentStorage


class AttachmentTraversing(SimpleHandler):
    ''' attachment traversing '''

    name = None

    def __init__(self, context, request=None):
        self.context = context

    def traverse(self, name, remaining):
        ''' traverse '''

        # Note: also fixes possible unicode problems
        attach_name = urllib.parse.quote(name)

        storage = IAttachmentStorage(self.context)

        if attach_name not in storage:
            raise NotFound

        return storage[attach_name]


class RestAttachmentTraversing(SimpleHandler):
    ''' rest attachment traversing '''

    name = None

    def __init__(self, context, request=None):
        self.context = context

    def traverse(self, name, remaining):
        ''' traverse '''

        # Note: also fixes possible unicode problems
        attach_name = urllib.parse.quote(name)

        storage = IAttachmentStorage(self.context.context)

        if attach_name not in storage:
            raise NotFound

        # self.context is a RESTWrapper
        storage = storage.__of__(self.context.context)

        return RESTWrapper(storage[attach_name], self.context.request)
