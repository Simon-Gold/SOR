from flask import Blueprint, jsonify, request, abort
from apifairy import authenticate, body, response, other_responses
from apifairy.exceptions import ValidationError
from mongoengine.queryset.visitor import Q
#internals
from api.offender.schemas import OffenderSchema
from api.auth import token_auth
from .models import Offender, OffenderCase

# blue print
offenders = Blueprint("offenders", __name__)

offender_schema = OffenderSchema()
offenders_schema = OffenderSchema(many=True)


@offenders.route("/search/", methods=["GET"])
# @authenticate(token_auth)
@response(offenders_schema,)
@other_responses({400: "Bad Request!"})
def search_offenders():
    lastname = request.args.get("last")
    if not lastname:
        raise ValueError("Lastname is required!")
    q_lastname = Q(names__last_name__istartswith=lastname)

    # firstname optional
    firstname = request.args.get("first")
    q_firstname = Q()
    if firstname:
        q_firstname = Q(names__first_name__istartswith=firstname)

    # date of birth optional
    dob = request.args.get("dob")
    q_dob = Q()
    if dob:
        month,day,year = dob.split("/")
        q_dob = (Q(dob__year=int(year)) &
                Q(dob__month=int(month)) &
                Q(dob__day=int(day)))
    # filter all
    results = Offender.objects.filter(
        q_lastname &
        q_firstname &
        q_dob
    )

    return results

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