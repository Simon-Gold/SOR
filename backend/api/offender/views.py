from flask import Blueprint, jsonify, request, abort
from apifairy import authenticate, body, response, other_responses
from apifairy.exceptions import ValidationError
#internals
from api.offender.schemas import OffenderSchema
from api.auth import token_auth
from .models import Offender, OffenderCase

# blue print
offenders = Blueprint("offenders", __name__)

offender_schema = OffenderSchema()
offenders_schema = OffenderSchema(many=True)


@offenders.route("/offenders/", methods=["GET"])
@authenticate(token_auth)
@response(offenders_schema,)
@other_responses({400: "Bad Request!"})
def get_offenders():
    return Offender.objects

@offenders.route("/offenders/", methods=["POST"])
@authenticate(token_auth)
@body(offender_schema)
@response(offender_schema, 201)
@other_responses({400: "Bad Request!"})
def create_offender(args):
    payload = request.get_json()
    cases_payload = payload.pop("cases", [])
    cases_objects = []
    for case_payload in cases_payload:
        o_case = OffenderCase(**case_payload)
        o_case.save()
        cases_objects.append(o_case)
    offender = Offender(**payload, cases=cases_objects)
    offender.save()
    return offender