import urllib.request
import json
import sys

# Configure UTF-8 stdout for Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def post_json(url, data, headers=None):
    if headers is None: headers = {}
    headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method='POST')
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def get_json(url, headers=None):
    if headers is None: headers = {}
    req = urllib.request.Request(url, headers=headers, method='GET')
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def put_json(url, data, headers=None):
    if headers is None: headers = {}
    headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method='PUT')
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

print("=== 1. Testing Request OTP ===")
r_otp = post_json('http://127.0.0.1:8000/api/auth/request-otp', {'email': 'sunita.devi@gmail.com'})
print("OTP result:", r_otp.get('success'), "Dev OTP:", r_otp.get('dev_otp'))
dev_otp = r_otp.get('dev_otp')

print("=== 2. Testing Verify OTP ===")
r_auth = post_json('http://127.0.0.1:8000/api/auth/verify-otp', {'email': 'sunita.devi@gmail.com', 'code': dev_otp})
token = r_auth.get('token')
print("Auth result:", r_auth.get('success'), "Token exists:", bool(token))

auth_headers = {'Authorization': f'Bearer {token}'}

print("=== 3. Testing Get Me ===")
r_me = get_json('http://127.0.0.1:8000/api/me', auth_headers)
print("Current User email:", r_me['user']['email'])

print("=== 4. Testing Update Profile (Sunita Devi: Farmer, Women, Low-Income) ===")
profile_data = {
    'name': 'Sunita Devi',
    'age': 32,
    'gender': 'Female',
    'state': 'Bihar',
    'area': 'Rural',
    'income': 120000,
    'land': 'Small/Marginal (< 5 Acres)',
    'bpl': True,
    'categories': ['Farmer', 'Women', 'Low-Income/Economically Weaker', 'Rural Household'],
    'subCategories': ['Small/Marginal Farmer', 'Women Farmer', 'General Woman', 'BPL Family', 'Rural Woman'],
    'occupation': 'Farmer',
    'interest': 'LPG connection and crop support'
}
r_upd = put_json('http://127.0.0.1:8000/api/me/profile', {'profile': profile_data}, auth_headers)
print("Profile updated:", r_upd.get('success'), "Saved categories:", r_upd['user']['profile']['categories'])

print("=== 5. Testing Schemes Evaluation ===")
r_schemes = get_json('http://127.0.0.1:8000/api/schemes', auth_headers)
print("Total schemes:", r_schemes['total'])
print("Eligible count:", r_schemes['eligible_count'])
print("Criteria mismatch count:", r_schemes['criteria_mismatch_count'])
print("Overall match rate:", r_schemes['overall_match_rate'], "%")

for s in r_schemes['schemes'][:4]:
    el = s.get('eligibility', {})
    print(f"\n[Scheme] {s['name']}")
    print(f"Status: {el.get('status')} | Match Score: {el.get('match_percentage')}%")
    print(f"Official Portal: {s.get('portal')}")
    for cond in el.get('conditions', []):
        mark = "PASS" if cond['passed'] else "FAIL"
        print(f"   [{mark}] {cond['label']}: {cond['detail']}")

print("\n=== 6. Testing Bookmark Toggle ===")
r_bm = post_json('http://127.0.0.1:8000/api/me/saved/pm-ujjwala-yojana', {}, auth_headers)
print("Bookmark PM Ujjwala:", r_bm.get('success'), "Is saved:", r_bm.get('is_saved'))
