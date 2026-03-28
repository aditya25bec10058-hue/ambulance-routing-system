"""
hospitals.py - Hospital database and availability management
Stores hospital data: location, beds, doctors, specialists
"""

import random

# Simulated hospital data (city-based with coordinates for distance calc)
HOSPITAL_DATABASE = {
    "H001": {
        "name": "City General Hospital",
        "location": (28.6139, 77.2090),  # lat, lon (Delhi example)
        "address": "12, Civil Lines, New Delhi",
        "total_beds": 200,
        "available_beds": 45,
        "icu_beds_total": 30,
        "icu_beds_available": 8,
        "doctors_on_duty": 12,
        "specialists": {
            "Cardiologist": 2,
            "Neurologist": 1,
            "Orthopedic": 2,
            "General Surgeon": 3,
            "Pediatrician": 1,
            "Trauma Specialist": 2,
            "Burns Specialist": 1,
        },
        "facilities": ["ICU", "Operation Theater", "Blood Bank", "MRI", "CT Scan"],
        "contact": "011-23456789",
        "emergency_available": True,
    },
    "H002": {
        "name": "Apollo Medical Center",
        "location": (28.6280, 77.2150),
        "address": "45, Connaught Place, New Delhi",
        "total_beds": 150,
        "available_beds": 12,
        "icu_beds_total": 20,
        "icu_beds_available": 2,
        "doctors_on_duty": 8,
        "specialists": {
            "Cardiologist": 3,
            "Neurologist": 2,
            "Orthopedic": 1,
            "General Surgeon": 2,
            "Pediatrician": 2,
            "Trauma Specialist": 1,
            "Burns Specialist": 0,
        },
        "facilities": ["ICU", "Operation Theater", "Blood Bank", "MRI"],
        "contact": "011-34567890",
        "emergency_available": True,
    },
    "H003": {
        "name": "Sunrise Community Hospital",
        "location": (28.6000, 77.1900),
        "address": "78, Rajouri Garden, New Delhi",
        "total_beds": 80,
        "available_beds": 30,
        "icu_beds_total": 10,
        "icu_beds_available": 5,
        "doctors_on_duty": 5,
        "specialists": {
            "Cardiologist": 1,
            "Neurologist": 0,
            "Orthopedic": 1,
            "General Surgeon": 2,
            "Pediatrician": 1,
            "Trauma Specialist": 1,
            "Burns Specialist": 0,
        },
        "facilities": ["ICU", "Operation Theater", "CT Scan"],
        "contact": "011-45678901",
        "emergency_available": True,
    },
    "H004": {
        "name": "National Trauma & Burns Centre",
        "location": (28.6400, 77.2300),
        "address": "99, Ring Road, New Delhi",
        "total_beds": 120,
        "available_beds": 55,
        "icu_beds_total": 25,
        "icu_beds_available": 15,
        "doctors_on_duty": 10,
        "specialists": {
            "Cardiologist": 1,
            "Neurologist": 1,
            "Orthopedic": 3,
            "General Surgeon": 4,
            "Pediatrician": 0,
            "Trauma Specialist": 5,
            "Burns Specialist": 4,
        },
        "facilities": ["ICU", "Operation Theater", "Blood Bank", "Burns Unit", "MRI", "CT Scan"],
        "contact": "011-56789012",
        "emergency_available": True,
    },
    "H005": {
        "name": "Green Valley Children Hospital",
        "location": (28.5900, 77.2200),
        "address": "23, Lajpat Nagar, New Delhi",
        "total_beds": 60,
        "available_beds": 20,
        "icu_beds_total": 15,
        "icu_beds_available": 7,
        "doctors_on_duty": 6,
        "specialists": {
            "Cardiologist": 0,
            "Neurologist": 1,
            "Orthopedic": 0,
            "General Surgeon": 1,
            "Pediatrician": 5,
            "Trauma Specialist": 0,
            "Burns Specialist": 1,
        },
        "facilities": ["ICU", "Neonatal Unit", "Operation Theater"],
        "contact": "011-67890123",
        "emergency_available": True,
    },
    "H006": {
        "name": "Heartcare Cardiac Institute",
        "location": (28.6500, 77.1800),
        "address": "5, Pitampura, New Delhi",
        "total_beds": 90,
        "available_beds": 0,
        "icu_beds_total": 20,
        "icu_beds_available": 0,
        "doctors_on_duty": 4,
        "specialists": {
            "Cardiologist": 6,
            "Neurologist": 1,
            "Orthopedic": 0,
            "General Surgeon": 2,
            "Pediatrician": 0,
            "Trauma Specialist": 0,
            "Burns Specialist": 0,
        },
        "facilities": ["ICU", "Cath Lab", "Operation Theater", "MRI"],
        "contact": "011-78901234",
        "emergency_available": False,  # Full!
    },
}


def get_all_hospitals():
    """Return full hospital database."""
    return HOSPITAL_DATABASE


def get_hospital_by_id(hospital_id):
    """Fetch a single hospital by its ID."""
    return HOSPITAL_DATABASE.get(hospital_id, None)


def update_bed_availability(hospital_id, bed_type="general"):
    """
    Mark a bed as booked once ambulance confirms.
    bed_type: 'general' or 'icu'
    """
    if hospital_id not in HOSPITAL_DATABASE:
        return False, "Hospital not found."

    hospital = HOSPITAL_DATABASE[hospital_id]

    if bed_type == "icu":
        if hospital["icu_beds_available"] > 0:
            hospital["icu_beds_available"] -= 1
            return True, f"ICU bed booked at {hospital['name']}."
        else:
            return False, "No ICU beds available."
    else:
        if hospital["available_beds"] > 0:
            hospital["available_beds"] -= 1
            return True, f"General bed booked at {hospital['name']}."
        else:
            return False, "No general beds available."


def get_specialist_hospitals(specialist_needed):
    """Return hospitals that have the required specialist available."""
    result = []
    for hid, hdata in HOSPITAL_DATABASE.items():
        count = hdata["specialists"].get(specialist_needed, 0)
        if count > 0 and hdata["available_beds"] > 0 and hdata["emergency_available"]:
            result.append((hid, hdata, count))
    return result
