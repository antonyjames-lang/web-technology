import re
import os
import random
import hashlib
import datetime
import logging
import jwt
from functools import wraps
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import Otp, User

logger = logging.getLogger(__name__)

GMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@gmail\.com$", re.IGNORECASE)
OTP_EXPIRY_MINUTES = 10
SECRET_KEY = getattr(settings, "JWT_SECRET", "yojana-mitra-jwt-civic-secret-key-2026")

def is_valid_gmail(email: str) -> bool:
    if not email:
        return False
    return bool(GMAIL_REGEX.match(email.strip()))


def hash_otp_code(email: str, code: str) -> str:
    salt = getattr(settings, "SECRET_KEY", "yojana_mitra_salt")
    payload = f"{email.lower().strip()}:{code.strip()}:{salt}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def generate_and_save_otp(email: str):
    email = email.lower().strip()
    code = f"{random.randint(100000, 999999)}"
    code_hash = hash_otp_code(email, code)
    now = datetime.datetime.utcnow()
    expires_at = now + datetime.timedelta(minutes=OTP_EXPIRY_MINUTES)

    # Invalidate previous OTPs for this email
    try:
        Otp.objects(email=email).delete()
    except Exception as e:
        logger.warning(f"Error clearing previous OTPs: {e}")

    otp_doc = Otp(
        email=email,
        code_hash=code_hash,
        attempts=0,
        created_at=now,
        expires_at=expires_at
    )
    otp_doc.save()

    # Attempt to send via Gmail SMTP
    smtp_user = getattr(settings, "EMAIL_HOST_USER", os.getenv("EMAIL_HOST_USER", ""))
    smtp_pass = getattr(settings, "EMAIL_HOST_PASSWORD", os.getenv("EMAIL_HOST_PASSWORD", ""))
    email_sent = False
    smtp_error = None

    if smtp_user and smtp_pass:
        try:
            subject = "Yojana Mitra - Your 6-Digit Verification Code"
            message = (
                f"Namaste,\n\n"
                f"Your 6-digit login verification OTP for Yojana Mitra is: {code}\n\n"
                f"This code will expire in {OTP_EXPIRY_MINUTES} minutes. "
                f"Please do not share this OTP with anyone.\n\n"
                f"Government Scheme Eligibility Identifier - Yojana Mitra Team"
            )
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", smtp_user)
            send_mail(
                subject,
                message,
                from_email,
                [email],
                fail_silently=False,
            )
            email_sent = True
        except Exception as e:
            logger.warning(f"Failed to send email via SMTP: {e}")
            smtp_error = str(e)

    return {
        "code": code,
        "email_sent": email_sent,
        "smtp_error": smtp_error,
        "expires_in_minutes": OTP_EXPIRY_MINUTES
    }


def verify_otp_and_login(email: str, code: str):
    email = email.lower().strip()
    code = str(code).strip()
    code_hash = hash_otp_code(email, code)
    now = datetime.datetime.utcnow()

    otp_doc = Otp.objects(email=email).first()
    if not otp_doc:
        return None, "No OTP found for this email. Please request a new OTP."

    if otp_doc.expires_at < now:
        otp_doc.delete()
        return None, "OTP has expired. Please request a new code."

    if otp_doc.attempts >= 5:
        otp_doc.delete()
        return None, "Too many failed attempts. Please request a new OTP."

    if otp_doc.code_hash != code_hash:
        otp_doc.attempts += 1
        otp_doc.save()
        return None, f"Incorrect OTP. {5 - otp_doc.attempts} attempts remaining."

    # OTP is valid! Delete used OTP
    otp_doc.delete()

    # Find or create User
    user = User.objects(email=email).first()
    if not user:
        user = User(email=email)
        user.save()

    # Generate JWT
    token_payload = {
        "user_id": str(user.id),
        "email": user.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        "iat": datetime.datetime.utcnow()
    }
    token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

    return {
        "token": token,
        "user": user.to_dict()
    }, None


def get_user_from_request(request):
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header[7:].strip()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        email = payload.get("email")
        if user_id:
            user = User.objects(id=user_id).first()
            if user:
                return user
        if email:
            return User.objects(email=email).first()
        return None
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception) as e:
        logger.debug(f"JWT decode error: {e}")
        return None


def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = get_user_from_request(request)
        if not user:
            return JsonResponse({
                "error": "Unauthorized",
                "message": "Valid Bearer authentication token is required."
            }, status=401)
        request.current_user = user
        return view_func(request, *args, **kwargs)
    return _wrapped_view
