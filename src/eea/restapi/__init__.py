# -*- coding: utf-8 -*-
"""Init and utils."""

from zope.i18nmessageid import MessageFactory

from plone.restapi.serializer.blocks import ResolveUIDSerializerBase

ResolveUIDSerializerBase.fields.append('provider_url')


_ = MessageFactory("eea.restapi")
