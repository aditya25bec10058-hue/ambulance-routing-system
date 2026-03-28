"""
main.py - SMART AMBULANCE DISPATCH & HOSPITAL ROUTING SYSTEM
=============================================================
A Python-based emergency medical routing system that:
1. Records patient case details (filled by ambulance crew)
2. Calculates nearest suitable hospitals using GPS + Haversine formula
3. Matches required specialist and bed availability
4. Books a bed and logs the case to CSV

Author: Aditya Srivastav (25BEC10058)
Course Project — Python Essentials
"""

import sys
import time
from hospitals import get_all_hospitals
from patient import create_patient_record, display_patient_summary
from routing import find_best_hospitals, display_hospital_options
from booking import confirm_booking, view_case_history, view_hospital_stats, initialize_log


def print_banner():
    """Display the welcome banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         🚑  SMART AMBULANCE DISPATCH SYSTEM  🚑              ║
║                                                              ║
║   Emergency Hospital Routing with Specialist Matching        ║
║   Real-time Bed Availability | GPS-based Distance Calc       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def main_menu():
    """Display main menu and return user choice."""
    print("\n" + "─" * 50)
    print("  MAIN MENU")
    print("─" * 50)
    print("  1. 🚨 New Emergency — Record Patient & Find Hospital")
    print("  2. 🏥 View All Hospital Availability")
    print("  3. 📋 View Past Case History")
    print("  4. ❌ Exit")
    print("─" * 50)
    return input("  Enter choice (1-4): ").strip()


def run_emergency_flow():
    """
    Full emergency flow:
    Patient intake → Hospital search → Book bed
    """
    all_hospitals = get_all_hospitals()

    # Step 1: Record patient
    print("\n  🚨 EMERGENCY IN PROGRESS...")
    print("  Ambulance crew — please fill patient details:\n")
    patient = create_patient_record()

    # Step 2: Show patient summary
    display_patient_summary(patient)

    # Step 3: Search for hospitals
    print("\n  🔍 Searching for nearest suitable hospitals...")
    print("  Calculating distances and matching availability...\n")
    time.sleep(1)  # Simulate processing

    ranked = find_best_hospitals(patient, all_hospitals, top_n=5)

    # Step 4: Display options
    display_hospital_options(ranked, patient)

    # Step 5: Book confirmation
    result = confirm_booking(patient, ranked, __import__("hospitals"))

    if result:
        hdata = result["data"]
        print("\n" + "=" * 65)
        print("  ✅  BOOKING CONFIRMED — PROCEED TO HOSPITAL")
        print("=" * 65)
        print(f"  Hospital : {hdata['name']}")
        print(f"  Address  : {hdata['address']}")
        print(f"  Contact  : {hdata['contact']}")
        print(f"  ETA      : ~{result['travel_time_min']} minutes")
        print(f"  Distance : {result['distance_km']} km")
        print("\n  🚑  Drive safe. Patient's life depends on you.")
        print("=" * 65)
    else:
        print("\n  📝 Case recorded. No booking made.")


def main():
    """Main program loop."""
    print_banner()
    initialize_log()

    while True:
        choice = main_menu()

        if choice == "1":
            run_emergency_flow()

        elif choice == "2":
            all_hospitals = get_all_hospitals()
            view_hospital_stats(all_hospitals)

        elif choice == "3":
            view_case_history()

        elif choice == "4":
            print("\n  👋 Exiting Ambulance Dispatch System. Stay safe!\n")
            sys.exit(0)

        else:
            print("\n  ❌ Invalid choice. Please enter 1, 2, 3, or 4.")

        input("\n  Press Enter to return to main menu...")


if __name__ == "__main__":
    main()
