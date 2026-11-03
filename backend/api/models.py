import datetime
from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    EmailField,
    IntField,
    FloatField,
    BooleanField,
    ListField,
    DictField,
    DateTimeField,
    EmbeddedDocumentField,
)

class UserProfile(EmbeddedDocument):
    name = StringField(default="")
    age = IntField(default=0)
    gender = StringField(default="")  # "Female", "Male", "Transgender", "Other"
    state = StringField(default="")
    area = StringField(default="Rural")  # "Rural" or "Urban"
    income = FloatField(default=0.0)  # Annual household income in INR
    land = StringField(default="None")  # "None", "Landless", "Small/Marginal (< 5 Acres)", "Medium/Large (> 5 Acres)"
    bpl = BooleanField(default=False)  # BPL card holder
    categories = ListField(StringField(), default=list)  # Main categories chosen from 25
    subCategories = ListField(StringField(), default=list)  # Sub-categories
    occupation = StringField(default="")
    interest = StringField(default="")

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "state": self.state,
            "area": self.area,
            "income": self.income,
            "land": self.land,
            "bpl": self.bpl,
            "categories": list(self.categories or []),
            "subCategories": list(self.subCategories or []),
            "occupation": self.occupation,
            "interest": self.interest,
        }


class User(Document):
    meta = {
        "collection": "users",
        "indexes": ["email"]
    }
    email = EmailField(unique=True, required=True)
    profile = EmbeddedDocumentField(UserProfile, default=UserProfile)
    saved_schemes = ListField(StringField(), default=list)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "profile": self.profile.to_dict() if self.profile else UserProfile().to_dict(),
            "saved_schemes": list(self.saved_schemes or []),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Scheme(Document):
    meta = {
        "collection": "schemes",
        "indexes": ["slug", "cat"]
    }
    slug = StringField(unique=True, required=True)
    name = StringField(required=True)
    cat = StringField(default="General")
    color = StringField(default="#1a237e")
    tagline = StringField(default="")
    about = StringField(default="")
    benefit = StringField(default="")
    beneficiaries = StringField(default="")
    deadline = StringField(default="Ongoing / Open")
    portal = StringField(required=True)  # REAL official government website URL
    target_categories = ListField(StringField(), default=list)  # Target from 25 main categories
    target_subcategories = ListField(StringField(), default=list)  # Optional narrower targeting
    rules = DictField(default=dict)  # optional: incomeMax, land, bpl, gender, ageMin, ageMax, area
    steps = ListField(ListField(StringField()), default=list)  # [[step_title, step_desc], ...]

    def to_dict(self):
        return {
            "id": str(self.id),
            "slug": self.slug,
            "name": self.name,
            "cat": self.cat,
            "color": self.color,
            "tagline": self.tagline,
            "about": self.about,
            "benefit": self.benefit,
            "beneficiaries": self.beneficiaries,
            "deadline": self.deadline,
            "portal": self.portal,
            "target_categories": list(self.target_categories or []),
            "target_subcategories": list(self.target_subcategories or []),
            "rules": dict(self.rules or {}),
            "steps": list(self.steps or []),
        }


class Otp(Document):
    meta = {
        "collection": "otps",
        "indexes": [
            "email",
            {"fields": ["expires_at"], "expireAfterSeconds": 0}
        ]
    }
    email = StringField(required=True)
    code_hash = StringField(required=True)
    attempts = IntField(default=0)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    expires_at = DateTimeField(required=True)
