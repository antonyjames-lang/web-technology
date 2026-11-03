import json
from django.test import TestCase, Client
from .models import Scheme, User, Otp
from .taxonomy import TAXONOMY, CATEGORIES_LIST
from .seed_data import seed_schemes_in_db

class YojanaMitraApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        seed_schemes_in_db()

    def test_taxonomy_endpoint(self):
        response = self.client.get('/api/taxonomy')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success"))
        self.assertEqual(len(data.get("categories", [])), 25)
        self.assertIn("Farmer", data.get("taxonomy", {}))
        self.assertIn("Small/Marginal Farmer", data["taxonomy"]["Farmer"])

    def test_request_otp_rejects_non_gmail(self):
        response = self.client.post(
            '/api/auth/request-otp',
            data=json.dumps({"email": "citizen@yahoo.com"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("Only @gmail.com", data.get("message", ""))

    def test_request_otp_valid_gmail_and_login(self):
        email = "citizen.india@gmail.com"
        # 1. Request OTP
        req_res = self.client.post(
            '/api/auth/request-otp',
            data=json.dumps({"email": email}),
            content_type="application/json"
        )
        self.assertEqual(req_res.status_code, 200)
        req_data = req_res.json()
        self.assertTrue(req_data.get("success"))
        otp_code = req_data.get("dev_otp")
        self.assertIsNotNone(otp_code)
        self.assertEqual(len(otp_code), 6)

        # 2. Try bad OTP
        bad_res = self.client.post(
            '/api/auth/verify-otp',
            data=json.dumps({"email": email, "code": "000000"}),
            content_type="application/json"
        )
        self.assertEqual(bad_res.status_code, 400)

        # 3. Verify OTP correctly
        verify_res = self.client.post(
            '/api/auth/verify-otp',
            data=json.dumps({"email": email, "code": otp_code}),
            content_type="application/json"
        )
        self.assertEqual(verify_res.status_code, 200)
        verify_data = verify_res.json()
        self.assertTrue(verify_data.get("success"))
        token = verify_data.get("token")
        self.assertIsNotNone(token)
        self.assertEqual(verify_data["user"]["email"], email)

        headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"}

        # 4. Check /api/me
        me_res = self.client.get('/api/me', **headers)
        self.assertEqual(me_res.status_code, 200)
        self.assertEqual(me_res.json()["user"]["email"], email)

        # 5. Update profile
        profile_payload = {
            "profile": {
                "name": "Ramesh Kumar",
                "age": 35,
                "gender": "Male",
                "state": "Uttar Pradesh",
                "area": "Rural",
                "income": 120000,
                "land": "Small/Marginal (< 5 Acres)",
                "bpl": True,
                "categories": ["Farmer", "Rural Household"],
                "subCategories": ["Small/Marginal Farmer", "Land Owner", "Rural Poor"],
                "occupation": "Agriculture",
                "interest": "Crop Subsidies & Solar Pump"
            }
        }
        update_res = self.client.put(
            '/api/me/profile',
            data=json.dumps(profile_payload),
            content_type="application/json",
            **headers
        )
        self.assertEqual(update_res.status_code, 200)
        updated_user = update_res.json()["user"]
        self.assertEqual(updated_user["profile"]["name"], "Ramesh Kumar")
        self.assertIn("Farmer", updated_user["profile"]["categories"])

        # 6. Fetch schemes with eligibility evaluation
        schemes_res = self.client.get('/api/schemes', **headers)
        self.assertEqual(schemes_res.status_code, 200)
        schemes_data = schemes_res.json()
        self.assertGreater(schemes_data["total"], 0)
        self.assertGreater(schemes_data["eligible_count"], 0)

        # PM-KISAN should be eligible for Ramesh (Farmer + Small/Marginal Land + Income <= 3.5L)
        pm_kisan = next((s for s in schemes_data["schemes"] if s["slug"] == "pm-kisan"), None)
        self.assertIsNotNone(pm_kisan)
        self.assertTrue(pm_kisan["eligibility"]["is_eligible"])
        self.assertEqual(pm_kisan["eligibility"]["status"], "ELIGIBLE")

        # 7. Toggle saved scheme
        save_res = self.client.post('/api/me/saved/pm-kisan', **headers)
        self.assertEqual(save_res.status_code, 200)
        self.assertTrue(save_res.json()["is_saved"])
        self.assertIn("pm-kisan", save_res.json()["saved_schemes"])

        # Toggle again to remove
        unsave_res = self.client.post('/api/me/saved/pm-kisan', **headers)
        self.assertEqual(unsave_res.status_code, 200)
        self.assertFalse(unsave_res.json()["is_saved"])
        self.assertNotIn("pm-kisan", unsave_res.json()["saved_schemes"])
