"""
AI Health Assistant Routes.
"""

from flask import (
    Blueprint,
    render_template,
    request,
)

from rapidfuzz import process, fuzz

from flask import send_file
from reportlab.pdfgen import canvas
import io

bp = Blueprint("ai", __name__)


# ---------------------------------------
# Symptom Database
# ---------------------------------------

SYMPTOMS = {

    "fever": {
        "keywords": [
            "fever",
            "fevr",
            "temperature",
            "high temperature",
            "body hot"
        ],
        "condition": "Possible Viral Fever / Flu",
        "advice": [
            "Drink plenty of water.",
            "Take adequate rest.",
            "Monitor your temperature."
        ],
        "severity": "Medium"
    },

    "cough": {
        "keywords": [
            "cough",
            "cof",
            "coughing",
            "dry cough",
            "wet cough"
        ],
        "condition": "Possible Respiratory Infection",
        "advice": [
            "Drink warm fluids.",
            "Avoid cold drinks."
        ],
        "severity": "Low"
    },

    "headache": {
        "keywords": [
            "headache",
            "head ache",
            "head pain",
            "migraine"
        ],
        "condition": "Possible Migraine / Stress Headache",
        "advice": [
            "Stay hydrated.",
            "Reduce screen time.",
            "Take proper rest."
        ],
        "severity": "Low"
    },

    "cold": {
        "keywords": [
            "cold",
            "running nose",
            "runny nose",
            "blocked nose",
            "sneezing"
        ],
        "condition": "Possible Common Cold",
        "advice": [
            "Drink warm water.",
            "Get enough sleep."
        ],
        "severity": "Low"
    },

    "sore throat": {
        "keywords": [
            "sore throat",
            "throat pain",
            "pain while swallowing"
        ],
        "condition": "Possible Throat Infection",
        "advice": [
            "Gargle with warm salt water.",
            "Drink warm liquids."
        ],
        "severity": "Low"
    },

    "stomach pain": {
        "keywords": [
            "stomach pain",
            "stomach ache",
            "gas pain"
        ],
        "condition": "Possible Gastric Problem",
        "advice": [
            "Avoid oily food.",
            "Drink enough water."
        ],
        "severity": "Medium"
    },

    "vomiting": {
        "keywords": [
            "vomiting",
            "vomit",
            "throwing up",
            "nausea"
        ],
        "condition": "Possible Food Poisoning",
        "advice": [
            "Drink ORS.",
            "Stay hydrated."
        ],
        "severity": "High"
    },

    "diarrhea": {
        "keywords": [
            "diarrhea",
            "loose motion",
            "loose stools"
        ],
        "condition": "Possible Digestive Infection",
        "advice": [
            "Drink ORS.",
            "Avoid spicy food."
        ],
        "severity": "Medium"
    },

    "body pain": {
        "keywords": [
            "body pain",
            "body ache",
            "muscle pain",
            "joint pain"
        ],
        "condition": "Possible Viral Infection",
        "advice": [
            "Take proper rest.",
            "Drink enough fluids."
        ],
        "severity": "Medium"
    },

    "fatigue": {
        "keywords": [
            "fatigue",
            "weakness",
            "low energy",
            "tired"
        ],
        "condition": "Possible General Weakness",
        "advice": [
            "Eat nutritious food.",
            "Sleep 7–8 hours."
        ],
        "severity": "Low"
    }

}

# ---------------------------------------
# Emergency Symptoms
# ---------------------------------------

EMERGENCY_KEYWORDS = [

    "chest pain",
    "heart pain",
    "difficulty breathing",
    "breathing problem",
    "can't breathe",
    "cannot breathe",
    "shortness of breath",
    "unconscious",
    "passed out",
    "severe bleeding",
    "heavy bleeding",
    "blood loss",
    "heart attack",
    "stroke"

]

# ---------------------------------------
# Doctor Recommendation
# ---------------------------------------

DOCTOR_MAP = {

    "fever": "👨‍⚕️ General Physician",

    "cough": "🫁 Pulmonologist",

    "cold": "👨‍⚕️ General Physician",

    "headache": "🧠 Neurologist",

    "sore throat": "👂 ENT Specialist",

    "stomach pain": "🩺 Gastroenterologist",

    "vomiting": "🩺 Gastroenterologist",

    "diarrhea": "🩺 Gastroenterologist",

    "body pain": "🦴 Orthopedic",

    "fatigue": "👨‍⚕️ General Physician"

}

MEDICINE_MAP = {

    "fever": [
        "Paracetamol (if suitable)",
        "ORS / Plenty of fluids"
    ],

    "cough": [
        "Cough syrup (OTC)",
        "Warm water"
    ],

    "cold": [
        "Steam inhalation",
        "Saline nasal spray"
    ],

    "headache": [
        "Paracetamol (if suitable)"
    ],

    "sore throat": [
        "Lozenges",
        "Warm salt-water gargle"
    ],

    "stomach pain": [
        "ORS",
        "Light meals"
    ],

    "vomiting": [
        "ORS"
    ],

    "diarrhea": [
        "ORS",
        "Probiotics (if advised)"
    ],

    "body pain": [
        "Paracetamol (if suitable)"
    ],

    "fatigue": [
        "Multivitamin (if advised)",
        "Balanced diet"
    ]

}


# ---------------------------------------
# AI Chatbot
# ---------------------------------------
@bp.route("/", methods=["GET", "POST"])
def chatbot():

    response = None

    if request.method == "POST":

        text = request.form.get(
            "symptoms",
            ""
        ).lower().strip()

        # ---------------------------------------
        # Build searchable phrases
        # ---------------------------------------

        words = text.split()

        phrases = words[:]

        # Two-word phrases
        for i in range(len(words) - 1):
            phrases.append(
                words[i] + " " + words[i + 1]
            )

        # Three-word phrases
        for i in range(len(words) - 2):
            phrases.append(
                words[i]
                + " "
                + words[i + 1]
                + " "
                + words[i + 2]
            )

        # ---------------------------------------
        # Emergency Detection
        # ---------------------------------------

        for emergency in EMERGENCY_KEYWORDS:

            # Exact match
            if emergency in text:

                response = {
                    "condition": "Possible Medical Emergency",
                    "advice": [
                        "Seek immediate medical attention.",
                        "Visit the nearest hospital immediately.",
                        "Do not rely only on AI advice."
                    ],
                    "medicines": [],
                    "detected": [
                        emergency.title()
                    ],
                    "severity": "🚨 EMERGENCY",
                    "doctor": "🚑 Emergency Department / Emergency Medicine",
                    "emergency": True
                }

                return render_template(
                    "ai/chatbot.html",
                    response=response
                )

            # Fuzzy match
            matched = process.extractOne(
                emergency,
                phrases,
                score_cutoff=75
            )

            if matched:

                response = {
                    "condition": "Possible Medical Emergency",
                    "advice": [
                        "Seek immediate medical attention.",
                        "Visit the nearest hospital immediately.",
                        "Do not rely only on AI advice."
                    ],
                    "medicines": [],
                    "detected": [
                        emergency.title()
                    ],
                    "severity": "🚨 EMERGENCY",
                    "doctor": "🚑 Emergency Department / Emergency Medicine",
                    "emergency": True
                }

                return render_template(
                    "ai/chatbot.html",
                    response=response
                )

        # ---------------------------------------
        # Normal Symptom Detection
        # ---------------------------------------

        # ---------------------------------------
        # Normal Symptom Detection
        # ---------------------------------------

        detected = []

        for symptom, data in SYMPTOMS.items():

            found = False

            for keyword in data["keywords"]:

                # Exact match
                if keyword in text:
                    found = True
                    break

                # Fuzzy match
                score = process.extractOne(
                    keyword,
                    phrases,
                    score_cutoff=80
                )

                if score:
                    found = True
                    break

            if found:
                detected.append(symptom)

        # ---------------------------------------
        # Build AI Response
        # ---------------------------------------

        if detected:

            conditions = []
            advice = set()
            doctors = set()
            medicines = set()

            severity_score = 0

            for symptom in detected:

                data = SYMPTOMS[symptom]

                conditions.append(data["condition"])

                doctors.add(
                    DOCTOR_MAP[symptom]
                )

                for item in data["advice"]:
                    advice.add(item)

                for medicine in MEDICINE_MAP[symptom]:
                    medicines.add(medicine)

                if data["severity"] == "Low":
                    severity_score += 1

                elif data["severity"] == "Medium":
                    severity_score += 2

                else:
                    severity_score += 3

            if severity_score <= 1:
                overall = "🟢 Low"

            elif severity_score <= 3:
                overall = "🟡 Medium"

            else:
                overall = "🔴 High"

            response = {

                "condition": ", ".join(
                    sorted(set(conditions))
                ),

                "advice": sorted(advice),

                "medicines": sorted(medicines),

                "detected": [
                    symptom.title()
                    for symptom in detected
                ],

                "severity": overall,

                "doctor": ", ".join(
                    sorted(doctors)
                ),

                "emergency": False

            }

        else:

            response = {

                "condition": "Unable to determine.",

                "advice": [
                    "Please consult a qualified doctor."
                ],

                "medicines": [],

                "detected": [],

                "severity": "Unknown",

                "doctor": "👨‍⚕️ General Physician",

                "emergency": False

            }

    return render_template(
        "ai/chatbot.html",
        response=response
    )