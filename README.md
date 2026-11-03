# Yojana Mitra (योजना मित्र)
### Government Scheme Eligibility Identifier for Indian Citizens

> **Yojana Mitra** is a civic-tech full-stack web application designed to help Indian citizens navigate central and state welfare programs. By profiling socio-economic factors and matching them against an authentic 25-group identity taxonomy, Yojana Mitra provides personalized scheme recommendations, transparent pass/fail diagnostic checklists, and direct links to official government portals.

---

## 🏛️ Key Highlights & Features

1. **Classic AngularJS 1.8.3 Frontend (Zero Build Step)**:
   - Pure, dependency-free frontend loaded directly via CDN `<script>` tag.
   - Single-Page Application (SPA) architecture with 5 interactive screens (`Welcome/Login`, `Eligibility Profiler Wizard`, `Dashboard`, `Scheme Detail Diagnostic`, `Profile & Saved Schemes`).
   - Saffron & Civic Navy design system with dark mode toggle, animated SVG match score gauge, and mobile responsiveness.

2. **Django 5 Backend & MongoDB via MongoEngine ODM**:
   - Clean, lightweight Django views returning `JsonResponse` (no DRF needed).
   - Document-based models using `mongoengine` with embedded user profiles and TTL index OTPs.
   - Seamless live MongoDB connection with an automatic in-memory `mongomock` fallback for local evaluation.

3. **Passwordless Gmail-Only OTP Authentication**:
   - Accepts only `@gmail.com` accounts verified via regex.
   - Issues 6-digit numeric OTP with 10-minute validity and SHA-256 hash storage.
   - Sends real emails via Gmail SMTP if configured; provides seamless developer auto-fill in development mode.
   - Issues stateless JWT session tokens signed with PyJWT.

4. **Exact 25 Citizen Categories & Sub-Categories Taxonomy**:
   - Supports multi-group identity (e.g. *Farmer* + *Women* + *Low-Income*).
   - Dynamic sub-category accordion that reveals tailored sub-groups upon selecting parent categories.

5. **Diagnostic Eligibility Engine**:
   - Evaluates categories, sub-categories, income ceilings, land ownership, BPL status, gender, and age limits.
   - Provides transparent line-by-line checklists explaining why a scheme passed or failed.
   - Includes official step-by-step application instructions and direct `.gov.in` / `.nic.in` portal links.

---

## 📂 Project Architecture

```
web tech/
├── backend/
│   ├── manage.py                          # Django management script
│   ├── yojana_mitra_backend/
│   │   ├── settings.py                    # Django configuration, CORS, JWT, MongoEngine
│   │   ├── urls.py                        # API routes & static frontend server
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── api/
│   │   ├── models.py                      # MongoEngine Documents: User, UserProfile, Scheme, Otp
│   │   ├── taxonomy.py                    # Official 25 categories & sub-categories dictionary
│   │   ├── eligibility.py                 # Diagnostic eligibility rule matching engine
│   │   ├── auth.py                        # Gmail regex validation, OTP generation, JWT auth
│   │   ├── views.py                       # JsonResponse API endpoints
│   │   ├── urls.py                        # API route mappings
│   │   ├── seed_data.py                   # 12 authentic Indian government schemes
│   │   ├── db.py                          # MongoEngine connection with mongomock fallback
│   │   ├── tests.py                       # Automated test suite
│   │   └── management/commands/
│   │       └── seed_schemes.py            # CLI database seeding command
│   ├── requirements.txt                   # Backend dependencies
│   ├── .env.example                       # Environment variables template
│   └── .env                               # Active configuration
├── frontend/
│   ├── index.html                          # AngularJS 1.8.3 SPA (5 distinct views)
│   ├── app.js                              # AngularJS module, Api factory, MainCtrl controller
│   ├── style.css                           # Civic trust design, CSS variables, Dark Mode
│   ├── login-lab.html                      # Standalone AngularJS login form for the lab
│   ├── login-lab.js                        # Login module, controller, and AuthService
│   └── login-lab.css                       # Responsive login form styles
└── README.md
```

---

## 🛠️ Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Frontend** | AngularJS | `1.8.3` | Classic declarative MVC frontend (via CDN) |
| **Styling** | Vanilla CSS3 | Custom | Civic Trust Palette, Dark Mode, SVG Rings |
| **Backend** | Django | `5.1.4` | Python web framework, views returning `JsonResponse` |
| **Database** | MongoDB | MongoEngine `0.29.3` | Document-based ODM with embedded documents |
| **Authentication** | PyJWT | `2.15.1` | Stateless Bearer token sessions |
| **CORS** | django-cors-headers | `4.9.0` | Cross-origin access for standalone frontend |
| **Fallback DB** | mongomock | `4.3.0` | In-memory MongoDB mock for instant zero-dependency testing |

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.14)
- (Optional) MongoDB 6.0+ running locally or a MongoDB Atlas URI. *(Note: If MongoDB is not running, the application automatically uses in-memory `mongomock` so it runs immediately out of the box).*

### 2. Backend Setup
From the project root:

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (if not already created)
python -m venv ../venv
..\venv\Scripts\activate    # On Windows
# source ../venv/bin/activate # On Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Run migrations and system checks
python manage.py check

# Seed authentic government schemes
python manage.py seed_schemes
```

### 3. Run the Application
Start the Django development server:

```bash
python manage.py runserver 8000
```

Open your web browser and navigate to:
👉 **`http://localhost:8000/`**

> **Note**: Django serves the frontend directly at `http://localhost:8000/`. Alternatively, you can open `frontend/index.html` directly in your browser or serve it on any static port (e.g. `python -m http.server 3000` from `frontend/`) because CORS is fully configured!

### AngularJS Login Form Lab

The standalone lab form is `frontend/login-lab.html`. It uses AngularJS 1.8.3 from Google's CDN and the existing Django Gmail OTP endpoints. From the project root, start the backend using the setup above, then serve the frontend in a second VS Code terminal:

```powershell
python -m http.server 3000
```

Open `http://localhost:3000/frontend/login-lab.html`. Enter a Gmail address, request the code, and verify it. In development mode, the returned OTP appears on the page; successful verification displays the signed-in email. The backend stores the session token in browser local storage.

---

## ⚙️ Environment Configuration (`.env`)

Create `backend/.env` from `backend/.env.example` if it does not already exist. Keep this file local; it contains credentials and is excluded by `.gitignore`.

```ini
# MongoDB Connection
# Set to your MongoDB instance or MongoDB Atlas URI:
MONGODB_URI=mongodb://localhost:27017/yojana_mitra
MONGODB_DB=yojana_mitra

# Security
DJANGO_SECRET_KEY=yojana-mitra-civic-django-super-secret-key-change-in-production
JWT_SECRET=yojana-mitra-jwt-civic-secret-key-minimum-32-chars-long
DEBUG=True

# Gmail SMTP Settings (Optional - for sending real emails)
# If left blank, the app runs in Development Mode and returns OTPs directly in the API response.
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=
```

### MongoDB Connection

The Django API uses MongoEngine models for users, OTPs, and schemes. On startup, `backend/api/db.py` pings the configured MongoDB server and connects to the `MONGODB_DB` database. The default configuration is local MongoDB:

```ini
MONGODB_URI=mongodb://localhost:27017/yojana_mitra
MONGODB_DB=yojana_mitra
```

For MongoDB Atlas, create a database user, allow the development machine's IP in Atlas Network Access, then put the Atlas connection string in `backend/.env`. Use a URL-encoded password if it contains reserved URL characters:

```ini
MONGODB_URI=mongodb+srv://<database-user>:<url-encoded-password>@<cluster-host>/yojana_mitra?retryWrites=true&w=majority
MONGODB_DB=yojana_mitra
```

Start Django from the `backend/` directory with `python manage.py runserver 8000`. A successful startup reports the database name, not the connection string. If MongoDB is unreachable, local development falls back to in-memory `mongomock`; its data is temporary and will not persist after the process exits. Install and run MongoDB locally or configure Atlas to persist login and application data.

---

## 📋 Comprehensive 25 Categories Taxonomy

Every user can select multiple personas from this exact civic taxonomy:

1. **Farmer**: Small/Marginal Farmer, Land Owner, Tenant Farmer, Agricultural Labourer, Women Farmer, Farmer with Disability
2. **Student**: School Student, College Student, Higher Education Student, Girl Student, SC/ST Student, Minority Student, Student with Disability
3. **Women**: General Woman, Widow, Divorced Woman, Abandoned Woman, Single Mother, Pregnant/Lactating Woman, Women Entrepreneur
4. **Differently Abled / Persons with Disabilities**: Visual Impairment, Hearing Impairment, Locomotor Disability, Intellectual Disability, Autism, Cerebral Palsy, Multiple Disability
5. **Senior Citizen**: 60+ Years, 80+ Years, Senior Citizen with Disability, Low-Income Senior Citizen
6. **Children**: Girl Child, Boy Child, Orphan Child, Child from Low-Income Family, Child with Disability
7. **Youth**: Unemployed Youth, Job Seeker, Skill Training Seeker, Young Entrepreneur
8. **Unemployed Person**: Educated Unemployed, Unskilled Unemployed, Differently Abled Unemployed, Youth Seeking Employment
9. **SC – Scheduled Caste**: SC Student, SC Farmer, SC Entrepreneur, SC Woman, SC Unemployed Person
10. **ST – Scheduled Tribe**: ST Student, ST Farmer, ST Entrepreneur, ST Woman, Tribal Family
11. **BC/MBC/OBC**: BC, MBC, OBC, BC/MBC Student, BC/MBC Entrepreneur
12. **Minority**: Muslim, Christian, Sikh, Buddhist, Jain, Parsi, Minority Student, Minority Entrepreneur
13. **Government Employee**: Central Government Employee, State Government Employee, Government Pensioner, Government Employee Family
14. **Private Employee/Worker**: Private Employee, Industrial Worker, Construction Worker, Domestic Worker, Unorganised Worker
15. **Entrepreneur/Business Owner**: New Entrepreneur, MSME Owner, Women Entrepreneur, Youth Entrepreneur, SC/ST Entrepreneur, Startup Founder
16. **Low-Income/Economically Weaker**: BPL Family, EWS, Low-Income Family, Economically Vulnerable Family
17. **Rural Household**: Rural Poor, Landless Family, Rural Woman, Rural Youth, Rural Worker
18. **Urban Household**: Urban Poor, Slum Household, Urban Worker, Street Vendor
19. **Fisherman**: Fisherman, Fisherwoman, Fishing Family, Fisher Youth
20. **Traditional Artisan**: Weaver, Potter, Carpenter, Blacksmith, Handicraft Worker, Traditional Artisan
21. **Construction Worker**: Registered Construction Worker, Construction Worker Family, Construction Worker with Disability
22. **Ex-Serviceman**: Ex-Serviceman, Ex-Serviceman Family, War Widow
23. **Housing/Homeless**: Homeless Person, Homeless Family, Rural Housing Beneficiary, Urban Housing Beneficiary, Landless Family
24. **Health/Medical**: Pregnant Woman, Mother & Child, Person with Disability, Serious Disease Patient, Low-Income Patient
25. **Socially Vulnerable**: Orphan, Destitute Person, Homeless Person, Released Bonded Labourer, Manual Scavenger

---

## 📦 Seeded Government Schemes & Portals

The application includes 12 real Indian welfare programs with authentic `.gov.in` portals:

1. **PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)** — [https://pmkisan.gov.in](https://pmkisan.gov.in)
2. **National Scholarship Scheme (Central Sector Higher Education)** — [https://scholarships.gov.in](https://scholarships.gov.in)
3. **Pradhan Mantri Awas Yojana (PMAY - Housing for All)** — [https://pmaymis.gov.in](https://pmaymis.gov.in)
4. **Ayushman Bharat - PM-JAY (Jan Arogya Yojana)** — [https://pmjay.gov.in](https://pmjay.gov.in)
5. **Pradhan Mantri Ujjwala Yojana 2.0 (PMUY)** — [https://pmuy.gov.in](https://pmuy.gov.in)
6. **Pradhan Mantri Kaushal Vikas Yojana (PMKVY 4.0)** — [https://www.pmkvyofficial.org](https://www.pmkvyofficial.org)
7. **Indira Gandhi National Old Age Pension Scheme (IGNOAPS)** — [https://socialjustice.gov.in](https://socialjustice.gov.in)
8. **ADIP Scheme (Aids for Persons with Disabilities)** — [https://adip.depwd.gov.in](https://adip.depwd.gov.in)
9. **Stand-Up India Scheme (Loans for SC/ST/Women)** — [https://www.standupmitra.in](https://www.standupmitra.in)
10. **PM SVANidhi (Micro-Credit for Street Vendors)** — [https://pmsvanidhi.mohua.gov.in](https://pmsvanidhi.mohua.gov.in)
11. **PM Vishwakarma Scheme (Traditional Artisans)** — [https://pmvishwakarma.gov.in](https://pmvishwakarma.gov.in)
12. **Pradhan Mantri Matsya Sampada Yojana (PMMSY)** — [https://pmmsy.dof.gov.in](https://pmmsy.dof.gov.in)

---

## 📡 REST API Reference

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/taxonomy` | No | Returns the 25 official categories and sub-categories dictionary |
| `POST` | `/api/auth/request-otp` | No | Validates Gmail regex and dispatches 6-digit OTP |
| `POST` | `/api/auth/verify-otp` | No | Verifies OTP and returns JWT token and user profile |
| `GET` | `/api/me` | Bearer JWT | Returns current authenticated citizen profile |
| `PUT` | `/api/me/profile` | Bearer JWT | Updates citizen demographics, income, land, and categories |
| `POST` | `/api/me/saved/<slug>` | Bearer JWT | Toggles a scheme as bookmarked/saved |
| `GET` | `/api/schemes` | Optional | Returns schemes list with diagnostic eligibility checklists |
| `GET` | `/api/schemes/<slug>` | Optional | Returns detailed scheme criteria, roadmap, and portal |

---

## 🧪 Automated Testing

Run the Django automated test suite:

```bash
cd backend
python manage.py test api
```

Run the end-to-end integration test verifying the full login, profile update, eligibility matching, and bookmarking lifecycle:

```bash
python test_e2e_live.py
```
