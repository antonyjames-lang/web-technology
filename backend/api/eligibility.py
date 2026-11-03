"""
Eligibility Engine for Yojana Mitra
Evaluates scheme criteria against user profile and produces detailed checklists.
"""

def evaluate_scheme_eligibility(scheme, profile):
    """
    Evaluates a single scheme against a user's profile dict or UserProfile object.
    Returns:
    {
        "is_eligible": bool,
        "status": "ELIGIBLE" | "CRITERIA_MISMATCH" | "NOT_ELIGIBLE",
        "badge": "Eligible" | "Criteria Mismatch" | "Not Eligible",
        "match_percentage": int (0-100),
        "conditions": [
            {
                "id": str,
                "label": str,
                "passed": bool,
                "detail": str
            },
            ...
        ]
    }
    """
    if hasattr(profile, "to_dict"):
        p = profile.to_dict()
    elif isinstance(profile, dict):
        p = profile
    else:
        p = {}

    user_categories = set(p.get("categories") or [])
    user_subcategories = set(p.get("subCategories") or [])
    user_income = float(p.get("income") or 0.0)
    user_land = str(p.get("land") or "None").strip()
    user_bpl = bool(p.get("bpl", False))
    user_gender = str(p.get("gender") or "").strip().lower()
    user_age = int(p.get("age") or 0)

    target_cats = set(scheme.get("target_categories") if isinstance(scheme, dict) else (scheme.target_categories or []))
    target_subcats = set(scheme.get("target_subcategories") if isinstance(scheme, dict) else (scheme.target_subcategories or []))
    rules = scheme.get("rules") if isinstance(scheme, dict) else (scheme.rules or {})
    if not isinstance(rules, dict):
        rules = {}

    conditions = []

    # 1. Category / Subcategory Overlap
    matched_cats = user_categories.intersection(target_cats)
    matched_subcats = user_subcategories.intersection(target_subcats)
    has_category_match = bool(matched_cats or matched_subcats)

    if has_category_match:
        matched_items = list(matched_cats) + list(matched_subcats)
        conditions.append({
            "id": "category_match",
            "label": "Category & Persona Match",
            "passed": True,
            "detail": f"Matched category/group: {', '.join(matched_items[:3])}"
        })
    else:
        target_display = ", ".join(list(target_cats)[:2]) if target_cats else "Specific target groups"
        conditions.append({
            "id": "category_match",
            "label": "Category & Persona Match",
            "passed": False,
            "detail": f"Scheme targets: {target_display}. You selected: {', '.join(list(user_categories)[:2]) or 'None'}"
        })

    # 2. Income Max Rule
    if "incomeMax" in rules and rules["incomeMax"] is not None:
        max_income = float(rules["incomeMax"])
        if user_income <= max_income:
            conditions.append({
                "id": "income_rule",
                "label": "Income Ceiling",
                "passed": True,
                "detail": f"Annual income (\u20b9{int(user_income):,}) is within limit (\u20b9{int(max_income):,})"
            })
        else:
            conditions.append({
                "id": "income_rule",
                "label": "Income Ceiling",
                "passed": False,
                "detail": f"Annual income (\u20b9{int(user_income):,}) exceeds limit of \u20b9{int(max_income):,}"
            })

    # 3. Land Ownership Rule
    if "land" in rules and rules["land"]:
        req_land = rules["land"]
        if req_land in ["Required", "Owner"]:
            has_land = user_land not in ["None", "Landless", ""]
            conditions.append({
                "id": "land_rule",
                "label": "Agricultural Land",
                "passed": has_land,
                "detail": "Cultivable land ownership verified" if has_land else "Scheme requires land ownership (profile indicates Landless / None)"
            })
        elif req_land in ["None", "Landless"]:
            is_landless = user_land in ["None", "Landless", ""]
            conditions.append({
                "id": "land_rule",
                "label": "Landless Status",
                "passed": is_landless,
                "detail": "Landless criteria met" if is_landless else "Scheme is intended exclusively for landless households"
            })

    # 4. BPL Status Rule
    if "bpl" in rules and rules["bpl"] is True:
        conditions.append({
            "id": "bpl_rule",
            "label": "BPL Card Status",
            "passed": user_bpl,
            "detail": "BPL cardholder status confirmed" if user_bpl else "Requires active BPL (Below Poverty Line) card"
        })

    # 5. Gender Rule
    if "gender" in rules and rules["gender"]:
        req_gender = str(rules["gender"]).strip().lower()
        gender_match = (user_gender == req_gender)
        conditions.append({
            "id": "gender_rule",
            "label": "Gender Eligibility",
            "passed": gender_match,
            "detail": f"Exclusively for {rules['gender']} applicants" if gender_match else f"Requires {rules['gender']} applicant (Profile is {p.get('gender') or 'Unspecified'})"
        })

    # 6. Age Minimum Rule
    if "ageMin" in rules and rules["ageMin"] is not None:
        min_age = int(rules["ageMin"])
        age_pass = user_age >= min_age
        conditions.append({
            "id": "age_min_rule",
            "label": "Minimum Age",
            "passed": age_pass,
            "detail": f"Applicant age ({user_age} yrs) meets minimum requirement ({min_age} yrs)" if age_pass else f"Applicant age ({user_age} yrs) is below minimum required age of {min_age} yrs"
        })

    # 7. Age Maximum Rule
    if "ageMax" in rules and rules["ageMax"] is not None:
        max_age = int(rules["ageMax"])
        age_pass = (user_age > 0 and user_age <= max_age)
        conditions.append({
            "id": "age_max_rule",
            "label": "Maximum Age",
            "passed": age_pass,
            "detail": f"Applicant age ({user_age} yrs) is within maximum age limit of {max_age} yrs" if age_pass else f"Applicant age ({user_age} yrs) exceeds maximum limit of {max_age} yrs"
        })

    # Overall calculation
    total_conditions = len(conditions)
    passed_conditions = sum(1 for c in conditions if c["passed"])
    match_percentage = int((passed_conditions / total_conditions) * 100) if total_conditions > 0 else 0

    all_rules_passed = all(c["passed"] for c in conditions if c["id"] != "category_match")
    category_passed = any(c["passed"] for c in conditions if c["id"] == "category_match")

    is_eligible = (category_passed and all_rules_passed)

    if is_eligible:
        status = "ELIGIBLE"
        badge = "Eligible"
    elif category_passed and not all_rules_passed:
        status = "CRITERIA_MISMATCH"
        badge = "Criteria Mismatch"
    else:
        status = "NOT_ELIGIBLE"
        badge = "Not Eligible"

    return {
        "is_eligible": is_eligible,
        "status": status,
        "badge": badge,
        "match_percentage": match_percentage,
        "passed_count": passed_conditions,
        "total_count": total_conditions,
        "conditions": conditions
    }
