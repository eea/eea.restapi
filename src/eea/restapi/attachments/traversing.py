from zope.traversing.namespace import SimpleHandler

from plone.rest.traverse import RESTWrapper
from six.moves import urllib
from zExceptions import NotFound

from .interfaces import IAttachmentStorage


class AttachmentTraversing(SimpleHandler):
    name = None

    def __init__(self, context, request=None):
        self.context = context

    def traverse(self, name, remaining):

        # Note: also fixes possible unicode problems
        attach_name = urllib.parse.quote(name)

        storage = IAttachmentStorage(self.context)

        if attach_name not in storage:
            raise NotFound

        return storage[attach_name]


class RestAttachmentTraversing(SimpleHandler):
    name = None

    def __init__(self, context, request=None):
        self.context = context

    def traverse(self, name, remaining):

        # Note: also fixes possible unicode problems
        attach_name = urllib.parse.quote(name)

        storage = IAttachmentStorage(self.context.context)

        if attach_name not in storage:
            raise NotFound

        # self.context is a RESTWrapper
        storage = storage.__of__(self.context.context)

        return RESTWrapper(storage[attach_name], self.context.request)
