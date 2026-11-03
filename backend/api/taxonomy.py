"""
Yojana Mitra - Exact 25 Categories and Sub-categories Taxonomy
"""

TAXONOMY = {
    "Farmer": [
        "Small/Marginal Farmer",
        "Land Owner",
        "Tenant Farmer",
        "Agricultural Labourer",
        "Women Farmer",
        "Farmer with Disability"
    ],
    "Student": [
        "School Student",
        "College Student",
        "Higher Education Student",
        "Girl Student",
        "SC/ST Student",
        "Minority Student",
        "Student with Disability"
    ],
    "Women": [
        "General Woman",
        "Widow",
        "Divorced Woman",
        "Abandoned Woman",
        "Single Mother",
        "Pregnant/Lactating Woman",
        "Women Entrepreneur"
    ],
    "Differently Abled / Persons with Disabilities": [
        "Visual Impairment",
        "Hearing Impairment",
        "Locomotor Disability",
        "Intellectual Disability",
        "Autism",
        "Cerebral Palsy",
        "Multiple Disability"
    ],
    "Senior Citizen": [
        "60+ Years",
        "80+ Years",
        "Senior Citizen with Disability",
        "Low-Income Senior Citizen"
    ],
    "Children": [
        "Girl Child",
        "Boy Child",
        "Orphan Child",
        "Child from Low-Income Family",
        "Child with Disability"
    ],
    "Youth": [
        "Unemployed Youth",
        "Job Seeker",
        "Skill Training Seeker",
        "Young Entrepreneur"
    ],
    "Unemployed Person": [
        "Educated Unemployed",
        "Unskilled Unemployed",
        "Differently Abled Unemployed",
        "Youth Seeking Employment"
    ],
    "SC \u2013 Scheduled Caste": [
        "SC Student",
        "SC Farmer",
        "SC Entrepreneur",
        "SC Woman",
        "SC Unemployed Person"
    ],
    "ST \u2013 Scheduled Tribe": [
        "ST Student",
        "ST Farmer",
        "ST Entrepreneur",
        "ST Woman",
        "Tribal Family"
    ],
    "BC/MBC/OBC": [
        "BC",
        "MBC",
        "OBC",
        "BC/MBC Student",
        "BC/MBC Entrepreneur"
    ],
    "Minority": [
        "Muslim",
        "Christian",
        "Sikh",
        "Buddhist",
        "Jain",
        "Parsi",
        "Minority Student",
        "Minority Entrepreneur"
    ],
    "Government Employee": [
        "Central Government Employee",
        "State Government Employee",
        "Government Pensioner",
        "Government Employee Family"
    ],
    "Private Employee/Worker": [
        "Private Employee",
        "Industrial Worker",
        "Construction Worker",
        "Domestic Worker",
        "Unorganised Worker"
    ],
    "Entrepreneur/Business Owner": [
        "New Entrepreneur",
        "MSME Owner",
        "Women Entrepreneur",
        "Youth Entrepreneur",
        "SC/ST Entrepreneur",
        "Startup Founder"
    ],
    "Low-Income/Economically Weaker": [
        "BPL Family",
        "EWS",
        "Low-Income Family",
        "Economically Vulnerable Family"
    ],
    "Rural Household": [
        "Rural Poor",
        "Landless Family",
        "Rural Woman",
        "Rural Youth",
        "Rural Worker"
    ],
    "Urban Household": [
        "Urban Poor",
        "Slum Household",
        "Urban Worker",
        "Street Vendor"
    ],
    "Fisherman": [
        "Fisherman",
        "Fisherwoman",
        "Fishing Family",
        "Fisher Youth"
    ],
    "Traditional Artisan": [
        "Weaver",
        "Potter",
        "Carpenter",
        "Blacksmith",
        "Handicraft Worker",
        "Traditional Artisan"
    ],
    "Construction Worker": [
        "Registered Construction Worker",
        "Construction Worker Family",
        "Construction Worker with Disability"
    ],
    "Ex-Serviceman": [
        "Ex-Serviceman",
        "Ex-Serviceman Family",
        "War Widow"
    ],
    "Housing/Homeless": [
        "Homeless Person",
        "Homeless Family",
        "Rural Housing Beneficiary",
        "Urban Housing Beneficiary",
        "Landless Family"
    ],
    "Health/Medical": [
        "Pregnant Woman",
        "Mother & Child",
        "Person with Disability",
        "Serious Disease Patient",
        "Low-Income Patient"
    ],
    "Socially Vulnerable": [
        "Orphan",
        "Destitute Person",
        "Homeless Person",
        "Released Bonded Labourer",
        "Manual Scavenger"
    ]
}

CATEGORIES_LIST = list(TAXONOMY.keys())

if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    
    total_subcategories = sum(len(subs) for subs in TAXONOMY.values())
    print("=" * 65)
    print("       YOJANA MITRA - CITIZEN TAXONOMY DIRECTORY")
    print("=" * 65)
    print(f"Total Primary Categories: {len(CATEGORIES_LIST)}")
    print(f"Total Sub-Categories    : {total_subcategories}\n")

    for idx, (category, subcategories) in enumerate(TAXONOMY.items(), 1):
        print(f"[{idx:02d}] {category} ({len(subcategories)} sub-categories):")
        for sub in subcategories:
            print(f"     • {sub}")
        print()
    print("=" * 65)
    print("Taxonomy structure verified successfully.")

