"""
Seed data of 12 real Indian Government Schemes with official portal URLs and criteria.
"""

SCHEMES_SEED = [
    {
        "slug": "pm-kisan",
        "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "cat": "Farmer & Agriculture",
        "color": "#15803d",
        "tagline": "Direct income support of \u20b96,000/year for landholding farmer families across India",
        "about": "PM-KISAN provides income support to all landholding farmer families across the country to cultivate crops and purchase agricultural inputs, transferred in 3 equal installments of \u20b92,000.",
        "benefit": "\u20b96,000 per year transferred directly to bank accounts via Direct Benefit Transfer (DBT) in three equal installments every 4 months.",
        "beneficiaries": "Small, marginal, and cultivating landholding farmer families.",
        "deadline": "Open / Ongoing registration throughout the year",
        "portal": "https://pmkisan.gov.in",
        "target_categories": ["Farmer", "Rural Household"],
        "target_subcategories": ["Small/Marginal Farmer", "Land Owner", "Women Farmer", "Agricultural Labourer"],
        "rules": {
            "land": "Required",
            "incomeMax": 350000
        },
        "steps": [
            ["Step 1: Aadhaar Authentication", "Visit pmkisan.gov.in and select 'New Farmer Registration'. Enter Aadhaar and complete OTP verification."],
            ["Step 2: Land Records Entry", "Enter your state, district, sub-district, village, land Khata/Khasra number, and bank account IFSC code."],
            ["Step 3: State Verification & DBT", "Revenue officers verify land ownership records. Approved farmers start receiving \u20b92,000 installments via DBT."]
        ]
    },
    {
        "slug": "nsp-central-scholarship",
        "name": "National Scholarship Scheme (Central Sector Higher Education)",
        "cat": "Education & Students",
        "color": "#1d4ed8",
        "tagline": "Financial scholarship of up to \u20b920,000/year for meritorious students in college and universities",
        "about": "Implemented by the Ministry of Education to support meritorious students from low-income families pursuing regular graduate and post-graduate studies in colleges and universities.",
        "benefit": "\u20b912,000 per annum for the first 3 years of Undergraduate study and \u20b920,000 per annum for Postgraduate courses.",
        "beneficiaries": "Students with 80th percentile in Class 12 pursuing regular higher education degrees.",
        "deadline": "Annual portal window typically July to December",
        "portal": "https://scholarships.gov.in",
        "target_categories": ["Student", "Youth", "Low-Income/Economically Weaker"],
        "target_subcategories": ["College Student", "Higher Education Student", "Girl Student", "SC/ST Student", "Minority Student"],
        "rules": {
            "incomeMax": 450000,
            "ageMax": 26
        },
        "steps": [
            ["Step 1: OTR Portal Registration", "Register on the National Scholarship Portal (NSP) with One-Time Registration (OTR) and Aadhaar."],
            ["Step 2: Choose Scheme & Submit Marks", "Select 'Central Sector Scheme of Scholarships for College and University Students' and upload marks sheet and fee receipt."],
            ["Step 3: Verification & Credit", "College/University verifies admission online, followed by State Nodal Officer approval. Funds transfer directly to bank."]
        ]
    },
    {
        "slug": "pmay-housing",
        "name": "Pradhan Mantri Awas Yojana (PMAY - Housing for All)",
        "cat": "Housing & Homeless",
        "color": "#b45309",
        "tagline": "Financial assistance up to \u20b91.30 Lakh to \u20b92.67 Lakh for building pucca houses with amenities",
        "about": "PMAY aims to ensure every poor Indian household has a pucca house equipped with clean cooking, electricity, and sanitation facilities.",
        "benefit": "Direct construction grant of \u20b91.20 Lakh (plains) / \u20b91.30 Lakh (hilly areas) for PMAY-G; up to \u20b92.67 Lakh interest subsidy under PMAY-U.",
        "beneficiaries": "Homeless families, kutcha house dwellers, low-income and BPL households.",
        "deadline": "Ongoing Gram Panchayat / Urban Local Body survey cycle",
        "portal": "https://pmaymis.gov.in",
        "target_categories": ["Housing/Homeless", "Rural Household", "Urban Household", "Low-Income/Economically Weaker", "Socially Vulnerable"],
        "target_subcategories": ["Homeless Person", "Homeless Family", "Rural Housing Beneficiary", "Urban Housing Beneficiary", "BPL Family", "Landless Family"],
        "rules": {
            "bpl": True,
            "incomeMax": 300000
        },
        "steps": [
            ["Step 1: Check SECC Priority List", "Check your family name on AwaasSoft SECC priority list or submit details to Gram Panchayat / Municipal Ward."],
            ["Step 2: Geo-tagging of Site", "Authorized inspector visits the kutcha house, takes geo-tagged photos, and verifies Aadhaar & bank details."],
            ["Step 3: Staged Construction Installments", "Disbursements are credited in 3 stages linked to construction milestones: plinth level, lintel level, and completion."]
        ]
    },
    {
        "slug": "ayushman-bharat-pmjay",
        "name": "Ayushman Bharat - PM-JAY (Jan Arogya Yojana)",
        "cat": "Health & Medical",
        "color": "#047857",
        "tagline": "Cashless health insurance coverage of \u20b95,00,000 per family/year for secondary & tertiary care",
        "about": "The world's largest government-funded healthcare scheme, providing free secondary and tertiary care hospitalization coverage across 27,000+ empaneled hospitals nationwide.",
        "benefit": "\u20b95,00,000 health cover per family per year, 100% cashless and paperless at public and private empaneled hospitals.",
        "beneficiaries": "Bottom 40% vulnerable and low-income population, plus all senior citizens 70+ years.",
        "deadline": "Open 24/7 / Ongoing card issuance",
        "portal": "https://pmjay.gov.in",
        "target_categories": ["Health/Medical", "Low-Income/Economically Weaker", "Senior Citizen", "Differently Abled / Persons with Disabilities", "Socially Vulnerable"],
        "target_subcategories": ["Low-Income Family", "BPL Family", "Serious Disease Patient", "Low-Income Patient", "60+ Years", "80+ Years"],
        "rules": {
            "incomeMax": 300000
        },
        "steps": [
            ["Step 1: Check Eligibility Online", "Visit pmjay.gov.in or Ayushman App and search by mobile number, Aadhaar number, or Ration Card."],
            ["Step 2: Biometric e-KYC", "Complete Aadhaar biometric verification or OTP at any CSC (Common Service Center) or hospital Ayushman Mitra desk."],
            ["Step 3: Download Ayushman Card", "Instant generation of the digital Ayushman Card containing unique PM-JAY ID for cashless treatments."]
        ]
    },
    {
        "slug": "pm-ujjwala-yojana",
        "name": "Pradhan Mantri Ujjwala Yojana 2.0 (PMUY)",
        "cat": "Women Welfare",
        "color": "#be185d",
        "tagline": "Deposit-free LPG connection, first refill and stove for women from low-income households",
        "about": "Provides clean cooking fuel to rural and deprived women to eliminate indoor smoke pollution and improve respiratory health.",
        "benefit": "Free LPG connection with zero deposit fee, free first 14.2 kg LPG cylinder refill, free gas stove, and continuing \u20b9300 targeted subsidy per refill.",
        "beneficiaries": "Adult women belonging to BPL households, SC/ST families, forest dwellers, and poor rural families.",
        "deadline": "Continuous open enrollment",
        "portal": "https://pmuy.gov.in",
        "target_categories": ["Women", "Low-Income/Economically Weaker", "Rural Household", "SC \u2013 Scheduled Caste", "ST \u2013 Scheduled Tribe"],
        "target_subcategories": ["General Woman", "Widow", "Single Mother", "BPL Family", "SC Woman", "ST Woman", "Rural Woman"],
        "rules": {
            "gender": "Female",
            "incomeMax": 250000
        },
        "steps": [
            ["Step 1: Obtain Application Form", "Apply online at pmuy.gov.in or collect the form from nearest Indane, Bharat Gas, or HP Gas distributor."],
            ["Step 2: Submit KYC Documents", "Provide applicant woman's Aadhaar card, ration card/BPL certificate, and bank account passbook."],
            ["Step 3: Delivery and Installation", "Gas distributor inspects kitchen, delivers cylinder, regulator, and safety stove with safety demonstration."]
        ]
    },
    {
        "slug": "pmkvy-skill-development",
        "name": "Pradhan Mantri Kaushal Vikas Yojana 4.0 (PMKVY)",
        "cat": "Youth & Employment",
        "color": "#7c3aed",
        "tagline": "Free industry-aligned skill training, government certification, and job placement support",
        "about": "Flagship scheme of the Ministry of Skill Development and Entrepreneurship (MSDE) enabling Indian youth to take up industry-relevant skill training.",
        "benefit": "100% free skill certification training, toolkits, daily stipend during training, and direct placement opportunities.",
        "beneficiaries": "School/college dropouts, unemployed youth, and job seekers aged 15-45.",
        "deadline": "Continuous training batches year-round",
        "portal": "https://www.pmkvyofficial.org",
        "target_categories": ["Youth", "Unemployed Person", "Student"],
        "target_subcategories": ["Unemployed Youth", "Job Seeker", "Skill Training Seeker", "Educated Unemployed", "Unskilled Unemployed"],
        "rules": {
            "ageMin": 15,
            "ageMax": 45
        },
        "steps": [
            ["Step 1: Skill India Digital Registration", "Visit skillindiadigital.gov.in and register with your mobile number."],
            ["Step 2: Choose Course & Training Center", "Browse modern skill courses (AI, Drone Technology, IT, Solar, Healthcare) and pick a nearby certified centre."],
            ["Step 3: Certification & Job Fair", "Complete course, pass NSQF assessment, receive verified DigiLocker certificate, and attend job fairs."]
        ]
    },
    {
        "slug": "national-senior-pension",
        "name": "Indira Gandhi National Old Age Pension Scheme (IGNOAPS)",
        "cat": "Senior Citizens",
        "color": "#0369a1",
        "tagline": "Monthly direct social security pension and welfare support for elderly citizens",
        "about": "National social security scheme providing monthly financial pensions and medical support to elderly citizens from economically vulnerable backgrounds.",
        "benefit": "Monthly financial pension (varying from \u20b91,000 to \u20b93,000 depending on state additions), free geriatric assistive devices, and dedicated 14567 helpline.",
        "beneficiaries": "Senior citizens aged 60 years and above from low-income or BPL households.",
        "deadline": "Open application cycle throughout the year",
        "portal": "https://socialjustice.gov.in",
        "target_categories": ["Senior Citizen", "Low-Income/Economically Weaker", "Socially Vulnerable"],
        "target_subcategories": ["60+ Years", "80+ Years", "Senior Citizen with Disability", "Low-Income Senior Citizen", "Destitute Person"],
        "rules": {
            "ageMin": 60,
            "incomeMax": 200000
        },
        "steps": [
            ["Step 1: Apply at Panchayat or Portal", "Submit application at nsap.nic.in or at the Block Development Office (BDO) / District Social Welfare Office."],
            ["Step 2: Age and Income Verification", "Submit Aadhaar card or voter ID for proof of age (60+) and BPL/income certificate issued by revenue authorities."],
            ["Step 3: Monthly Direct Bank Deposit", "Upon sanction, pension is credited every month directly to the senior citizen's bank or postal savings account."]
        ]
    },
    {
        "slug": "adip-divyangjan-aids",
        "name": "ADIP Scheme (Aids & Assistive Devices for Persons with Disabilities)",
        "cat": "Differently Abled",
        "color": "#4338ca",
        "tagline": "Free motorized tricycles, wheelchairs, smart canes, and hearing aids for Divyangjan",
        "about": "Implemented by the Department of Empowerment of Persons with Disabilities (DEPwD) to bring modern assistive equipment within reach of persons with disabilities.",
        "benefit": "100% free motorized tricycles, smart canes, braille slates, digital hearing aids, artificial limbs, prosthetics, and cochlear implant surgeries (up to \u20b96 Lakh for kids).",
        "beneficiaries": "Persons with benchmark disabilities (40% or more) holding a UDID card with family income up to \u20b930,000 per month.",
        "deadline": "Ongoing distribution camps and online applications",
        "portal": "https://adip.depwd.gov.in",
        "target_categories": ["Differently Abled / Persons with Disabilities", "Children", "Low-Income/Economically Weaker"],
        "target_subcategories": ["Visual Impairment", "Hearing Impairment", "Locomotor Disability", "Intellectual Disability", "Child with Disability", "Multiple Disability"],
        "rules": {
            "incomeMax": 360000
        },
        "steps": [
            ["Step 1: Obtain UDID Card", "Apply for Unique Disability ID at swavlambancard.gov.in and undergo medical assessment at District Hospital."],
            ["Step 2: Register on ADIP Portal", "Log in to adip.depwd.gov.in, select required assistive device according to disability specification."],
            ["Step 3: Camp Fitment & Handover", "Attend the ALIMCO distribution camp in your district for personalized fitment, training, and free handover of equipment."]
        ]
    },
    {
        "slug": "stand-up-india",
        "name": "Stand-Up India Scheme for SC/ST & Women Entrepreneurs",
        "cat": "Entrepreneurship & Business",
        "color": "#c2410c",
        "tagline": "Bank loans between \u20b910 Lakh and \u20b91 Crore for setting up greenfield business enterprises",
        "about": "Facilitates bank loans between \u20b910 lakh and \u20b91 crore to at least one SC or ST borrower and at least one woman borrower per bank branch for setting up greenfield enterprises.",
        "benefit": "Composite term loan & working capital from \u20b910 Lakh to \u20b9100 Lakh at concessional interest rates, margin money support, and handholding mentorship.",
        "beneficiaries": "SC / ST individuals and Women entrepreneurs aged 18 and above creating a new enterprise.",
        "deadline": "Continuous credit window across all Scheduled Commercial Banks",
        "portal": "https://www.standupmitra.in",
        "target_categories": ["Entrepreneur/Business Owner", "SC \u2013 Scheduled Caste", "ST \u2013 Scheduled Tribe", "Women"],
        "target_subcategories": ["SC Entrepreneur", "ST Entrepreneur", "Women Entrepreneur", "New Entrepreneur", "MSME Owner", "Startup Founder"],
        "rules": {
            "ageMin": 18
        },
        "steps": [
            ["Step 1: Portal Profiling", "Register on standupmitra.in as a 'Trainee Borrower' or 'Ready Borrower'."],
            ["Step 2: Project Report & Business Plan", "Prepare detailed project report (DPR) with financial projections with assistance from SIDBI handholding agencies."],
            ["Step 3: Bank Sanction & Disbursement", "Lead bank processes application without collateral requirement under Credit Guarantee Scheme for Stand-Up India (CGFSI)."]
        ]
    },
    {
        "slug": "pm-svanidhi-street-vendors",
        "name": "PM SVANidhi (Micro-Credit Scheme for Street Vendors)",
        "cat": "Urban Livelihoods",
        "color": "#0d9488",
        "tagline": "Collateral-free working capital micro-loans of \u20b910,000, \u20b920,000, and \u20b950,000 with 7% interest subsidy",
        "about": "Launched by Ministry of Housing and Urban Affairs to empower street vendors, hawkers, thelawalas, and urban workers to restart and scale their micro-businesses.",
        "benefit": "Initial \u20b910,000 collateral-free loan, upgraded to \u20b920,000 and \u20b950,000 upon timely repayment. 7% interest subsidy and up to \u20b91,200 annual cash back for UPI transactions.",
        "beneficiaries": "Urban street vendors, hawkers, food stalls, fruit/vegetable sellers with Certificate of Vending or Urban Local Body recommendation.",
        "deadline": "Active across all municipal corporations and urban local bodies",
        "portal": "https://pmsvanidhi.mohua.gov.in",
        "target_categories": ["Urban Household", "Low-Income/Economically Weaker", "Private Employee/Worker"],
        "target_subcategories": ["Street Vendor", "Urban Worker", "Urban Poor", "Slum Household", "Unorganised Worker"],
        "rules": {
            "incomeMax": 200000
        },
        "steps": [
            ["Step 1: Check Vending Survey Status", "Verify your street vendor survey ID or obtain Letter of Recommendation (LoR) from ULB on pmsvanidhi.mohua.gov.in."],
            ["Step 2: Aadhaar Mobile Authentication", "Log in using Aadhaar-linked mobile number and select preferred lending bank / NBFC / MFI."],
            ["Step 3: Direct Disbursal to Bank Account", "Loan amount is disbursed in 48 hours without any paperwork or physical security."]
        ]
    },
    {
        "slug": "pm-vishwakarma",
        "name": "PM Vishwakarma Scheme (Support for Traditional Artisans)",
        "cat": "Artisans & Crafts",
        "color": "#9333ea",
        "tagline": "Official certificate, ID card, \u20b915,000 modern toolkit grant, and 5% interest loans up to \u20b93 Lakh",
        "about": "Holistic scheme to support traditional artisans and craftspeople working with their hands and traditional tools across 18 artisan trades.",
        "benefit": "Official recognition, 5-7 days basic skill training with \u20b9500/day stipend, \u20b915,000 grant for modern toolkits, and collateral-free enterprise credit up to \u20b93 Lakh at 5% interest.",
        "beneficiaries": "Traditional artisans (carpenters, blacksmiths, potters, weavers, cobblers, sculptors, goldsmiths, tailors, etc.) aged 18+.",
        "deadline": "Continuous nationwide enrollment",
        "portal": "https://pmvishwakarma.gov.in",
        "target_categories": ["Traditional Artisan", "Low-Income/Economically Weaker", "Entrepreneur/Business Owner"],
        "target_subcategories": ["Weaver", "Potter", "Carpenter", "Blacksmith", "Handicraft Worker", "Traditional Artisan"],
        "rules": {
            "ageMin": 18,
            "incomeMax": 300000
        },
        "steps": [
            ["Step 1: CSC Center Biometric Registration", "Visit nearest Common Service Center (CSC) with Aadhaar and bank details for biometric registration."],
            ["Step 2: Gram Panchayat & ULB Verification", "Three-tier verification: Gram Panchayat / Urban Local Body check followed by District Implementation Committee."],
            ["Step 3: Toolkit Grant & Credit Access", "Receive PM Vishwakarma ID, basic training stipend, \u20b915,000 digital toolkit voucher, and low-interest loan."]
        ]
    },
    {
        "slug": "pmmsy-fisheries",
        "name": "Pradhan Mantri Matsya Sampada Yojana (PMMSY)",
        "cat": "Fisheries & Marine",
        "color": "#0284c7",
        "tagline": "Up to 60% government subsidy for motorized fishing boats, biofloc units, and safety equipment",
        "about": "Implemented by the Department of Fisheries to modernize the fisheries sector, enhance fishers' safety at sea, and double fishermen's income.",
        "benefit": "40% capital subsidy for General category and 60% capital subsidy for Women, SC, and ST fishers for boats, communication transponders, nets, and fish farming.",
        "beneficiaries": "Traditional fishers, fish farmers, fisherwomen cooperatives, and self-help groups.",
        "deadline": "Annual state fisheries department project approvals",
        "portal": "https://pmmsy.dof.gov.in",
        "target_categories": ["Fisherman", "Rural Household"],
        "target_subcategories": ["Fisherman", "Fisherwoman", "Fishing Family", "Fisher Youth"],
        "rules": {
            "incomeMax": 400000
        },
        "steps": [
            ["Step 1: Online Project Submission", "Register at pmmsy.dof.gov.in and submit project proposal with cost estimate."],
            ["Step 2: District Fisheries Officer Inspection", "District Level Committee (DLC) reviews and sanctions the proposed fisheries or equipment project."],
            ["Step 3: Subsidy Release via DBT", "Subsidy is directly released into the beneficiary's bank account upon purchase verification and geo-tagging."]
        ]
    }
]


def seed_schemes_in_db():
    from .models import Scheme
    inserted_count = 0
    for data in SCHEMES_SEED:
        scheme = Scheme.objects(slug=data["slug"]).first()
        if not scheme:
            scheme = Scheme(**data)
            scheme.save()
            inserted_count += 1
        else:
            # Update fields in case schema was enriched
            for key, val in data.items():
                setattr(scheme, key, val)
            scheme.save()
    return inserted_count
