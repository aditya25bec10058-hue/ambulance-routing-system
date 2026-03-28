"""
booking.py - Handles bed reservation and case logging
Saves all cases to a CSV file for record keeping
"""

import csv
import os
import datetime


LOG_FILE = "case_log.csv"

CSV_HEADERS = [
    "Case ID", "Timestamp", "Patient Name", "Age", "Gender", "Blood Group",
    "Severity", "ICU Required", "Incident Description", "Symptoms",
    "Specialist Needed", "Medical History", "Pickup Location",
    "Pickup Lat", "Pickup Lon", "Contact",
    "Assigned Hospital", "Hospital Address", "Hospital Contact",
    "Distance (km)", "ETA (min)", "Bed Type Booked", "Booking Status"
]


def initialize_log():
    """Create the CSV log file with headers if it doesn't exist."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)
        print(f"  📁 Case log initialized: {LOG_FILE}")


def confirm_booking(patient, ranked_hospitals, hospitals_module):
    """
    Ask ambulance crew to confirm which hospital to book.
    Updates bed availability and logs the case.
    """
    if not ranked_hospitals:
        print("\n  ❌ No hospitals available to book.\n")
        return None

    print("\n" + "=" * 65)
    print("     ✅  CONFIRM HOSPITAL BOOKING")
    print("=" * 65)
    print(f"  Enter hospital number to book (1–{len(ranked_hospitals)})")
    print("  Or press 'S' to skip booking and just log the case.")
    print("  Or press 'Q' to quit without logging.\n")

    choice = input("  Your choice: ").strip().upper()

    if choice == "Q":
        print("\n  🚫 Booking cancelled. Case not logged.")
        return None

    if choice == "S":
        _log_case(patient, None, None, "SKIPPED")
        print("\n  📝 Case logged without hospital assignment.")
        return None

    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(ranked_hospitals):
            raise ValueError
    except ValueError:
        print("\n  ❌ Invalid choice. Case not booked.")
        return None

    selected = ranked_hospitals[idx]
    hdata = selected["data"]
    hid = selected["id"]

    # Choose bed type
    print(f"\n  Booking at: {hdata['name']}")
    if patient.get("icu_required") and hdata["icu_beds_available"] > 0:
        bed_input = input("  Book ICU bed (I) or General bed (G)? ").strip().upper()
        bed_type = "icu" if bed_input == "I" else "general"
    else:
        bed_type = "general"
        if patient.get("icu_required") and hdata["icu_beds_available"] == 0:
            print("  ⚠️  ICU unavailable here. Booking general bed instead.")

    # Update availability
    success, message = hospitals_module.update_bed_availability(hid, bed_type)

    if success:
        print(f"\n  ✅ {message}")
        print(f"  📞 Hospital notified. Contact: {hdata['contact']}")
        print(f"  ⏱️  ETA: ~{selected['travel_time_min']} minutes")

        # Log to CSV
        _log_case(patient, selected, bed_type, "CONFIRMED")

        print(f"\n  📝 Case logged to {LOG_FILE}")
        return selected
    else:
        print(f"\n  ❌ Booking failed: {message}")
        return None


def _log_case(patient, selected_hospital, bed_type, status):
    """Write case details to the CSV log."""
    initialize_log()

    if selected_hospital:
        hdata = selected_hospital["data"]
        h_name = hdata["name"]
        h_address = hdata["address"]
        h_contact = hdata["contact"]
        distance = selected_hospital["distance_km"]
        eta = selected_hospital["travel_time_min"]
    else:
        h_name = h_address = h_contact = "N/A"
        distance = eta = "N/A"

    row = [
        patient.get("case_id", ""),
        patient.get("timestamp", ""),
        patient.get("name", ""),
        patient.get("age", ""),
        patient.get("gender", ""),
        patient.get("blood_group", ""),
        patient.get("severity_label", ""),
        "Yes" if patient.get("icu_required") else "No",
        patient.get("incident_description", ""),
        "; ".join(patient.get("symptoms", [])),
        patient.get("specialist_needed", ""),
        patient.get("medical_history", ""),
        patient.get("pickup_location", ""),
        patient.get("pickup_lat", ""),
        patient.get("pickup_lon", ""),
        patient.get("contact_number", ""),
        h_name,
        h_address,
        h_contact,
        distance,
        eta,
        bed_type.upper() if bed_type else "N/A",
        status,
    ]

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)


def view_case_history():
    """Display all past cases from the CSV log."""
    if not os.path.exists(LOG_FILE):
        print("\n  📭 No case history found. No cases logged yet.")
        return

    print("\n" + "=" * 65)
    print("         📚  PAST CASE HISTORY")
    print("=" * 65)

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("  No records found.")
        return

    print(f"  Total cases logged: {len(rows)}\n")
    for i, row in enumerate(rows, 1):
        status_icon = "✅" if row["Booking Status"] == "CONFIRMED" else "📝"
        print(f"  {status_icon} [{i}] {row['Case ID']} | {row['Timestamp']}")
        print(f"       Patient : {row['Patient Name']}, {row['Age']}, {row['Gender']}")
        print(f"       Severity: {row['Severity']} | ICU: {row['ICU Required']}")
        print(f"       Incident: {row['Incident Description'][:50]}...")
        print(f"       Hospital: {row['Assigned Hospital']}")
        print(f"       Status  : {row['Booking Status']}")
        print()


def view_hospital_stats(all_hospitals):
    """Display current bed availability across all hospitals."""
    print("\n" + "=" * 65)
    print("         🏥  LIVE HOSPITAL BED AVAILABILITY")
    print("=" * 65)

    for hid, hdata in all_hospitals.items():
        status = "🟢 OPEN" if hdata["emergency_available"] and hdata["available_beds"] > 0 else "🔴 FULL/CLOSED"
        print(f"\n  {status} — {hdata['name']}")
        print(f"    General Beds : {hdata['available_beds']} / {hdata['total_beds']} available")
        print(f"    ICU Beds     : {hdata['icu_beds_available']} / {hdata['icu_beds_total']} available")
        print(f"    Doctors      : {hdata['doctors_on_duty']} on duty")

        specialists_avail = [s for s, c in hdata["specialists"].items() if c > 0]
        print(f"    Specialists  : {', '.join(specialists_avail) if specialists_avail else 'None'}")
