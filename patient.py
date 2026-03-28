"""
patient.py - Patient intake form filled by ambulance crew
Records emergency case details and determines specialist needed
"""

import datetime
import uuid


# Maps symptoms/conditions to required specialists
CONDITION_SPECIALIST_MAP = {
    "chest pain": "Cardiologist",
    "heart attack": "Cardiologist",
    "cardiac arrest": "Cardiologist",
    "palpitations": "Cardiologist",
    "stroke": "Neurologist",
    "seizure": "Neurologist",
    "unconscious": "Neurologist",
    "head injury": "Neurologist",
    "fracture": "Orthopedic",
    "bone break": "Orthopedic",
    "spinal injury": "Orthopedic",
    "accident": "Trauma Specialist",
    "road accident": "Trauma Specialist",
    "multiple injuries": "Trauma Specialist",
    "trauma": "Trauma Specialist",
    "burns": "Burns Specialist",
    "fire": "Burns Specialist",
    "chemical burn": "Burns Specialist",
    "child": "Pediatrician",
    "infant": "Pediatrician",
    "newborn": "Pediatrician",
    "pediatric": "Pediatrician",
    "appendix": "General Surgeon",
    "surgery": "General Surgeon",
    "bleeding": "General Surgeon",
}

SEVERITY_LEVELS = {
    "1": ("Critical", "🔴", "Immediate life-threatening emergency"),
    "2": ("Serious", "🟠", "Urgent but stable"),
    "3": ("Moderate", "🟡", "Needs attention, not life-threatening"),
    "4": ("Minor", "🟢", "Non-urgent"),
}


def create_patient_record():
    """
    Interactive form for ambulance crew to fill patient details.
    Returns a patient dictionary.
    """
    print("\n" + "=" * 60)
    print("       🚑  PATIENT INTAKE FORM  🚑")
    print("       (Filled by Ambulance Crew)")
    print("=" * 60)

    patient = {}
    patient["case_id"] = "CASE-" + str(uuid.uuid4())[:8].upper()
    patient["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n📋 Case ID: {patient['case_id']}")
    print(f"🕐 Time: {patient['timestamp']}\n")

    # Basic patient info
    print("--- PATIENT INFORMATION ---")
    patient["name"] = input("Patient Name (or 'Unknown'): ").strip() or "Unknown"
    
    age_input = input("Approximate Age: ").strip()
    patient["age"] = int(age_input) if age_input.isdigit() else 0
    
    patient["gender"] = input("Gender (M/F/Unknown): ").strip().upper() or "Unknown"
    patient["contact_number"] = input("Contact / Family Number (if available): ").strip() or "Not Available"

    # Incident description
    print("\n--- INCIDENT DESCRIPTION ---")
    print("Describe what happened (e.g., 'road accident with head injury and fracture'):")
    patient["incident_description"] = input("> ").strip()

    # Symptoms
    print("\nKey Symptoms observed (comma separated):")
    print("Examples: chest pain, unconscious, burns, fracture, seizure, bleeding...")
    symptoms_input = input("> ").strip().lower()
    patient["symptoms"] = [s.strip() for s in symptoms_input.split(",") if s.strip()]

    # Severity
    print("\n--- SEVERITY LEVEL ---")
    for key, (level, icon, desc) in SEVERITY_LEVELS.items():
        print(f"  {key}. {icon} {level} — {desc}")
    severity_choice = input("Select severity (1-4): ").strip()
    if severity_choice not in SEVERITY_LEVELS:
        severity_choice = "2"
    level_name, icon, desc = SEVERITY_LEVELS[severity_choice]
    patient["severity"] = severity_choice
    patient["severity_label"] = level_name
    patient["severity_icon"] = icon

    # ICU needed?
    print("\nDoes patient require ICU? (y/n): ", end="")
    icu_input = input().strip().lower()
    patient["icu_required"] = icu_input == "y"

    # Blood group
    patient["blood_group"] = input("\nBlood Group (if known, else press Enter): ").strip() or "Unknown"

    # Known medical history
    patient["medical_history"] = input("Known Medical History (e.g., diabetes, hypertension, or 'None'): ").strip() or "None"

    # Pickup location
    print("\n--- PICKUP LOCATION ---")
    patient["pickup_location"] = input("Incident Location / Address: ").strip()
    
    print("\nAmbulance GPS Coordinates (press Enter to use default test coords):")
    lat_in = input("  Latitude (e.g. 28.6200): ").strip()
    lon_in = input("  Longitude (e.g. 77.2100): ").strip()
    
    try:
        patient["pickup_lat"] = float(lat_in) if lat_in else 28.6200
        patient["pickup_lon"] = float(lon_in) if lon_in else 77.2100
    except ValueError:
        patient["pickup_lat"] = 28.6200
        patient["pickup_lon"] = 77.2100

    # Detect required specialist from symptoms
    patient["specialist_needed"] = detect_specialist(patient["symptoms"], patient["incident_description"])

    return patient


def detect_specialist(symptoms, description):
    """Auto-detect required specialist from symptoms and description."""
    combined = " ".join(symptoms) + " " + description.lower()
    for keyword, specialist in CONDITION_SPECIALIST_MAP.items():
        if keyword in combined:
            return specialist
    return "General Surgeon"  # Default fallback


def display_patient_summary(patient):
    """Print a clean summary of recorded patient data."""
    print("\n" + "=" * 60)
    print("         📄 PATIENT CASE SUMMARY")
    print("=" * 60)
    print(f"  Case ID     : {patient['case_id']}")
    print(f"  Time        : {patient['timestamp']}")
    print(f"  Name        : {patient['name']}")
    print(f"  Age/Gender  : {patient['age']} / {patient['gender']}")
    print(f"  Blood Group : {patient['blood_group']}")
    print(f"  Contact     : {patient['contact_number']}")
    print(f"  Severity    : {patient['severity_icon']} {patient['severity_label']}")
    print(f"  ICU Needed  : {'Yes ⚠️' if patient['icu_required'] else 'No'}")
    print(f"  Location    : {patient['pickup_location']}")
    print(f"  Coordinates : ({patient['pickup_lat']}, {patient['pickup_lon']})")
    print(f"\n  📝 Incident : {patient['incident_description']}")
    print(f"  🩺 Symptoms : {', '.join(patient['symptoms']) if patient['symptoms'] else 'Not specified'}")
    print(f"  🔬 Specialist Needed : {patient['specialist_needed']}")
    print(f"  📜 History  : {patient['medical_history']}")
    print("=" * 60)
