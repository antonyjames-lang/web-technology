import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Scheme, User, UserProfile
from .taxonomy import TAXONOMY, CATEGORIES_LIST
from .seed_data import seed_schemes_in_db
from .auth import (
    is_valid_gmail,
    generate_and_save_otp,
    verify_otp_and_login,
    jwt_required,
    get_user_from_request,
)
from .eligibility import evaluate_scheme_eligibility
from .db import init_mongo

logger = logging.getLogger(__name__)

# Ensure DB is initialized
init_mongo()


def parse_json_body(request):
    try:
        if request.body:
            return json.loads(request.body.decode("utf-8"))
        return {}
    except Exception:
        return {}


@csrf_exempt
@require_http_methods(["GET"])
def get_taxonomy(request):
    """Returns the 25 official categories and their sub-categories."""
    return JsonResponse({
        "success": True,
        "taxonomy": TAXONOMY,
        "categories": CATEGORIES_LIST
    })


@csrf_exempt
@require_http_methods(["POST"])
def request_otp(request):
    """
    POST /api/auth/request-otp { email }
    Sends or returns 6-digit OTP (Gmail only).
    """
    data = parse_json_body(request)
    email = data.get("email", "").strip()

    if not email:
        return JsonResponse({"error": "Email is required."}, status=400)

    if not is_valid_gmail(email):
        return JsonResponse({
            "error": "Invalid email",
            "message": "Only @gmail.com addresses are permitted (e.g. yourname@gmail.com)."
        }, status=400)

    try:
        result = generate_and_save_otp(email)
        response_data = {
            "success": True,
            "message": f"Verification OTP generated for {email}." + (
                " Sent to your inbox." if result["email_sent"] else " (Dev Mode Active: Use the code below)"
            ),
            "email_sent": result["email_sent"],
            "expires_in_minutes": result["expires_in_minutes"]
        }

        # If SMTP not configured or failed, return OTP in response for dev testing
        if not result["email_sent"]:
            response_data["dev_otp"] = result["code"]
            response_data["dev_note"] = "SMTP unconfigured or dev mode: OTP provided directly."

        return JsonResponse(response_data)
    except Exception as e:
        logger.exception("Failed in request_otp")
        return JsonResponse({"error": "Server error", "message": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def verify_otp(request):
    """
    POST /api/auth/verify-otp { email, code }
    Returns JWT token and user object.
    """
    data = parse_json_body(request)
    email = data.get("email", "").strip()
    code = data.get("code", "").strip()

    if not email or not code:
        return JsonResponse({"error": "Both email and 6-digit OTP are required."}, status=400)

    if not is_valid_gmail(email):
        return JsonResponse({"error": "Only @gmail.com addresses are supported."}, status=400)

    auth_result, error_msg = verify_otp_and_login(email, code)
    if error_msg:
        return JsonResponse({"error": "Verification failed", "message": error_msg}, status=400)

    return JsonResponse({
        "success": True,
        "message": "Successfully authenticated with Yojana Mitra.",
        "token": auth_result["token"],
        "user": auth_result["user"]
    })


@csrf_exempt
@require_http_methods(["GET"])
@jwt_required
def get_current_user(request):
    """
    GET /api/me (Bearer token auth)
    Returns current user object.
    """
    user = request.current_user
    return JsonResponse({
        "success": True,
        "user": user.to_dict()
    })


@csrf_exempt
@require_http_methods(["PUT"])
@jwt_required
def update_profile(request):
    """
    PUT /api/me/profile (Bearer token auth) { profile }
    Saves user profile including categories[] and subCategories[].
    """
    user = request.current_user
    data = parse_json_body(request)
    profile_data = data.get("profile", {})

    if not isinstance(profile_data, dict):
        return JsonResponse({"error": "Invalid payload format. 'profile' object required."}, status=400)

    # Validate categories against taxonomy
    categories = profile_data.get("categories", [])
    if isinstance(categories, list):
        # Keep valid categories
        clean_categories = [str(c).strip() for c in categories if str(c).strip()]
    else:
        clean_categories = []

    sub_categories = profile_data.get("subCategories", [])
    if isinstance(sub_categories, list):
        clean_sub_categories = [str(sc).strip() for sc in sub_categories if str(sc).strip()]
    else:
        clean_sub_categories = []

    try:
        user.profile.name = str(profile_data.get("name", "")).strip()
        user.profile.age = int(profile_data.get("age", 0) or 0)
        user.profile.gender = str(profile_data.get("gender", "")).strip()
        user.profile.state = str(profile_data.get("state", "")).strip()
        user.profile.area = str(profile_data.get("area", "Rural")).strip()
        user.profile.income = float(profile_data.get("income", 0.0) or 0.0)
        user.profile.land = str(profile_data.get("land", "None")).strip()
        user.profile.bpl = bool(profile_data.get("bpl", False))
        user.profile.categories = clean_categories
        user.profile.subCategories = clean_sub_categories
        user.profile.occupation = str(profile_data.get("occupation", "")).strip()
        user.profile.interest = str(profile_data.get("interest", "")).strip()

        user.save()

        return JsonResponse({
            "success": True,
            "message": "Citizen profile successfully updated.",
            "user": user.to_dict()
        })
    except Exception as e:
        logger.exception("Failed to update profile")
        return JsonResponse({"error": "Failed to update profile", "message": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@jwt_required
def toggle_saved_scheme(request, slug):
    """
    POST /api/me/saved/<slug> (Bearer token auth)
    Toggles a scheme as saved for the user.
    """
    user = request.current_user
    slug = str(slug).strip()

    # Check if scheme exists
    scheme = Scheme.objects(slug=slug).first()
    if not scheme:
        return JsonResponse({"error": "Scheme not found with given slug."}, status=404)

    saved_list = list(user.saved_schemes or [])
    if slug in saved_list:
        saved_list.remove(slug)
        is_saved = False
        action_msg = "Scheme removed from your saved list."
    else:
        saved_list.append(slug)
        is_saved = True
        action_msg = "Scheme saved to your profile for quick reference."

    user.saved_schemes = saved_list
    user.save()

    return JsonResponse({
        "success": True,
        "slug": slug,
        "is_saved": is_saved,
        "saved_schemes": saved_list,
        "message": action_msg
    })


@csrf_exempt
@require_http_methods(["GET"])
def get_schemes(request):
    """
    GET /api/schemes
    Returns full scheme list.
    Auto-seeds the database on first call if empty.
    If authenticated via Bearer token, calculates eligibility checklist for each scheme.
    """
    # Auto-seed if database is empty
    count = Scheme.objects.count()
    if count == 0:
        seed_schemes_in_db()

    schemes_docs = Scheme.objects.all()
    user = get_user_from_request(request)

    schemes_list = []
    eligible_count = 0
    criteria_mismatch_count = 0

    for s in schemes_docs:
        s_dict = s.to_dict()
        # Check if saved by current user
        if user and s.slug in (user.saved_schemes or []):
            s_dict["is_saved"] = True
        else:
            s_dict["is_saved"] = False

        # Calculate eligibility if user has filled profile
        if user and user.profile:
            eval_res = evaluate_scheme_eligibility(s_dict, user.profile)
            s_dict["eligibility"] = eval_res
            if eval_res["is_eligible"]:
                eligible_count += 1
            elif eval_res["status"] == "CRITERIA_MISMATCH":
                criteria_mismatch_count += 1
        else:
            # Default unauthenticated placeholder eligibility
            s_dict["eligibility"] = None

        schemes_list.append(s_dict)

    # Sort: Eligible first, then criteria mismatch, then others
    if user and user.profile:
        def sort_priority(item):
            el = item.get("eligibility")
            if not el:
                return 3
            if el.get("is_eligible"):
                return 0
            if el.get("status") == "CRITERIA_MISMATCH":
                return 1
            return 2
        schemes_list.sort(key=sort_priority)

    total_count = len(schemes_list)
    overall_match_rate = int((eligible_count / total_count) * 100) if total_count > 0 else 0

    return JsonResponse({
        "success": True,
        "total": total_count,
        "eligible_count": eligible_count,
        "criteria_mismatch_count": criteria_mismatch_count,
        "overall_match_rate": overall_match_rate,
        "schemes": schemes_list
    })


@csrf_exempt
@require_http_methods(["GET"])
def get_scheme_detail(request, slug):
    """
    GET /api/schemes/<slug>
    Returns detailed scheme data and eligibility analysis.
    """
    scheme = Scheme.objects(slug=slug).first()
    if not scheme:
        return JsonResponse({"error": "Scheme not found."}, status=404)

    user = get_user_from_request(request)
    s_dict = scheme.to_dict()

    if user:
        s_dict["is_saved"] = scheme.slug in (user.saved_schemes or [])
        if user.profile:
            s_dict["eligibility"] = evaluate_scheme_eligibility(s_dict, user.profile)
    else:
        s_dict["is_saved"] = False
        s_dict["eligibility"] = None

    return JsonResponse({
        "success": True,
        "scheme": s_dict
    })
