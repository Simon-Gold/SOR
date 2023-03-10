import datetime
from flask import Blueprint, jsonify, request, abort
from apifairy import authenticate, body, response, other_responses
from apifairy.exceptions import ValidationError
from mongoengine.queryset.visitor import Q
from werkzeug.exceptions import NotFound
# internals
from schemas import OffenderSchema, OffenderUpdateSchema
from handlers import token_auth
from models import Offender, OffenderCase
from decorators import auth_required

# blue print
bp_offenders = Blueprint("offenders", __name__)

offender_schema = OffenderSchema()
offenders_schema = OffenderSchema(many=True)
offender_update_schema = OffenderUpdateSchema(partial=True)


@bp_offenders.route("/search/", methods=["GET"])
@auth_required
@response(offenders_schema,)
@other_responses({400: "Bad Request!"})
def search_offenders():
    lastname = request.args.get("last")
    if not lastname:
        raise abort(code=400, description="Lastname is required!")
    q_lastname = Q(names__last_name__istartswith=lastname)

    # firstname optional
    firstname = request.args.get("first")
    q_firstname = Q()
    if firstname:
        q_firstname = Q(names__first_name__istartswith=firstname)

    #  state optional
    state = request.args.get("state")
    q_state = Q()
    if state:
        q_state = Q(state__iexact=state)
    # date of birth optional
    param_dob = request.args.get("dob")
    q_dob = Q()
    #  TODO move to service
    if param_dob:
        if param_dob.count("/") == 0:
            try:
                dob = datetime.datetime.strptime(param_dob, "%Y")
                q_dob = Q(dob__year=dob.year)
            except ValueError:
                return abort(code=400, description="Date Of Birth year format must be YYYY")
        if param_dob.count("/") == 1:
            try:
                dob = datetime.datetime.strptime(param_dob, "%m/%Y")
                q_dob = Q(dob__year=dob.year) & Q(dob__month=dob.month)
            except ValueError:
                return abort(code=400, description="Date Of Birth month/year format must be MM/YYYY")
        if param_dob.count("/") == 2:
            try:
                dob = datetime.datetime.strptime(param_dob, "%m/%d/%Y")
                q_dob = (Q(dob__year=dob.year) &
                         Q(dob__month=dob.month) &
                         Q(dob__day=dob.day))
            except ValueError:
                return abort(code=400, description="Date Of Birth month/day/year format must be MM/dd/YYYY")
    #  filter all
    results = Offender.objects.filter(
        q_lastname &
        q_state &
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


@bp_offenders.route("/offenders/<string:id>", methods=["PUT", "PATCH"])
@auth_required
@body(offender_update_schema)
@response(offender_schema,)
@other_responses({404: "Offender Not Found"})
def update_offender(data, id):
    """Update an offender by id"""
    try:
        offender = Offender.objects.get(pk=id)
        offender.update(**data)
    except Offender.DoesNotExist:
        return abort(404)
    else:
        offender.save()
        offender.reload()
        return offender


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
