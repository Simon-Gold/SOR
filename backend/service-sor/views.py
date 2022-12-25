from flask import Blueprint, jsonify, request, abort
from apifairy import authenticate, body, response, other_responses
from apifairy.exceptions import ValidationError
from mongoengine.queryset.visitor import Q
from werkzeug.exceptions import NotFound
# internals
from schemas import OffenderSchema
from handlers import token_auth
from models import Offender, OffenderCase
from decorators import auth_required

# blue print
bp_offenders = Blueprint("offenders", __name__)

offender_schema = OffenderSchema()
offenders_schema = OffenderSchema(many=True)


@bp_offenders.route("/search/", methods=["GET"])
@auth_required
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
        month, day, year = dob.split("/")
        q_dob = (Q(dob__year=int(year)) &
                 Q(dob__month=int(month)) |
                 Q(dob__day=int(day)))
    #  filter all
    results = Offender.objects.filter(
        q_lastname &
        q_firstname &
        q_dob
    )

    return results


@bp_offenders.route("/offenders/", methods=["GET"])
@auth_required
@other_responses({400: "Bad Request!"})
def get_offenders():
    """Get all offenders"""
    PAGE = 1
    PAGE_LIMIT = 10
    page = request.args.get("page") or PAGE
    limit = request.args.get("limit") or PAGE_LIMIT
    try:
        po = Offender.objects.paginate(page=int(page), per_page=int(limit))
        response = jsonify({
            "next": f"{request.base_url}?page={po.next_num}&limit={po.per_page}",
            "prev": f"{request.base_url}?page={po.prev_num}&limit={po.per_page}" if po.has_prev else None,
            "current_page": po.page,
            "limit": po.per_page,
            "total_items": po.total,
            "total_pages": po.pages,
            "items": offenders_schema.dump(po.items),
        })
        return response
    except NotFound:
        return abort(404)


@bp_offenders.route("/offenders/<string:id>", methods=["GET"])
@auth_required
@response(offender_schema,)
@other_responses({404: "Offender Not Found"})
def get_offender(id):
    """Retrieve an offender by id"""
    try:
        offender = Offender.objects.get(pk=id)
        return offender
    except Offender.DoesNotExist:
        return abort(404)


@bp_offenders.route("/offenders/", methods=["POST"])
@auth_required
@body(offender_schema)
@response(offender_schema, 201)
@other_responses({400: "Bad Request!"})
def create_offender(args):
    """Create an offender"""
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
