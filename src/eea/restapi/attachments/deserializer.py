''' deserializer module '''
from plone.restapi.deserializer import json_body
from plone.restapi.deserializer.mixins import OrderingMixin
from plone.restapi.interfaces import IDeserializeFromJson
from plone.restapi.interfaces import IFieldDeserializer
from z3c.form.interfaces import IDataManager
from z3c.form.interfaces import IManagerValidator
from zExceptions import BadRequest
from zope.component import adapter  # , queryUtility
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.interface import Interface
from zope.schema import getFields
from zope.schema.interfaces import ValidationError
from .interfaces import IAttachedFile
from .interfaces import IAttachedImage
from .interfaces import IAttachment


@implementer(IDeserializeFromJson)
@adapter(IAttachment, Interface)
class DeserializeFromJson(OrderingMixin, object):
    ''' deserialize from json '''
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(
        self, validate_all=False, data=None, create=False
    ):  # noqa: ignore=C901

        if data is None:
            data = json_body(self.request)

        schema_data, errors = self.get_schema_data(data, validate_all)

        for schema, field_data in schema_data.items():
            validator = queryMultiAdapter(
                (self.context, self.request, None, schema, None),
                IManagerValidator
            )

            for error in validator.validate(field_data):
                errors.append({"error": error, "message": str(error)})

        if errors:
            raise BadRequest(errors)

        # OrderingMixin
        self.handle_ordering(data)

        return self.context

    # pylint: disable=too-many-branches
    def get_schema_data(self, data, validate_all):
        ''' get_schema_data '''
        schema = IAttachment

        if IAttachedFile.providedBy(self.context):
            schema = IAttachedFile
        elif IAttachedImage.providedBy(self.context):
            schema = IAttachedImage

        schema_data = {}
        errors = []

        for name, field in getFields(schema).items():

            field_data = schema_data.setdefault(schema, {})

            if field.readonly:
                continue

            if name in data:
                dm = queryMultiAdapter((self.context, field), IDataManager)

                if not dm.canWrite():
                    continue

                if data[name] is None:
                    if not field.required:
                        dm.set(field.missing_value)
                    else:
                        errors.append(
                            {
                                "field": field.__name__,
                                "message": (
                                    "{} is a required field.".format(
                                        field.__name__
                                    ),
                                    "Setting it to null is not allowed.",
                                ),
                            }
                        )

                    continue

                # Deserialize to field value
                deserializer = queryMultiAdapter(
                    (field, self.context, self.request), IFieldDeserializer
                )

                if deserializer is None:
                    continue

                try:
                    value = deserializer(data[name])
                except ValueError as e:
                    errors.append(
                        {"message": str(e), "field": name, "error": e})
                except ValidationError as e:
                    errors.append(
                        {"message": e.doc(), "field": name, "error": e})
                else:
                    field_data[name] = value

                    if value != dm.get():
                        dm.set(value)
                        # self.mark_field_as_changed(schema, name)

            elif validate_all:
                # Never validate the changeNote of p.a.versioningbehavior
                # The Versionable adapter always returns an empty string
                # which is the wrong type. Should be unicode and should be
                # fixed in p.a.versioningbehavior

                if name == "changeNote":
                    continue
                dm = queryMultiAdapter((self.context, field), IDataManager)
                bound = field.bind(self.context)
                try:
                    bound.validate(dm.get())
                except ValidationError as e:
                    errors.append(
                        {"message": e.doc(), "field": name, "error": e})

        return schema_data, errors
