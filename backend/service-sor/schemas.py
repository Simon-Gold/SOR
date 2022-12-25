from marshmallow import validate
# internals
from main import marsh as ma


class OffenderChargeSchema(ma.Schema):
    description = ma.String()
    offense_date = ma.String()


class OffenderCaseSchema(ma.Schema):
    case_number = ma.String()
    charges = ma.List(ma.Nested(OffenderChargeSchema))


class DateOfBirth(ma.Schema):
    class Meta:
        ordered = True

    year = ma.Integer(strict=True, required=True,
                      validate=[validate.Range(
                          min=1900, error="Year must be min 1900")]
                      )
    month = ma.Integer(strict=True, required=True,
                       validate=[validate.Range(
                           min=1, max=12, error="Month must be between 1,12")]
                       )
    day = ma.Integer(strict=True, required=False,
                     validate=[validate.Range(
                         min=1, max=31, error="Day must be between 1,31")]
                     )


class DemographicSchema(ma.Schema):
    height = ma.String()
    weight = ma.String()
    sex = ma.String()
    race = ma.String()


class OffenderNameSchema(ma.Schema):
    first_name = ma.String()
    middle = ma.String()
    last_name = ma.String()


class OffenderAddressSchema(ma.Schema):
    line = ma.String()


class OffenderSchema(ma.Schema):
    class Meta:
        ordered = True

    id = ma.String(unique=True, dump_only=True)
    state = ma.String()
    names = ma.List(ma.Nested(OffenderNameSchema), required=True)
    addresses = ma.List(ma.Nested(OffenderAddressSchema), required=True)
    dob = ma.Nested(DateOfBirth, required=True)
    demographic = ma.Nested(DemographicSchema, required=True)
    is_deleted = ma.Boolean()
    created_date = ma.DateTime(dump_only=True)
    updated_date = ma.DateTime(dump_only=True)
    age = ma.Integer(required=False)
    cases = ma.List(ma.Nested(OffenderCaseSchema), required=False)
