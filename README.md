# 🚑 Smart Ambulance Dispatch & Hospital Routing System

A Python-based CLI application that simulates a smart ambulance dispatch system. When a medical emergency occurs, the ambulance crew fills in patient details on-site, and the system automatically finds the **nearest suitable hospital** with available beds, the required specialist, and ICU availability — then books a bed and logs the case.

---

## 🧠 Problem Statement

In real-world emergencies, ambulance crews often don't know:
- Which nearby hospital has beds available
- Which hospital has the required specialist (cardiologist, neurologist, etc.)
- Whether ICU is available before they arrive

This wastes critical time. This system solves that by **routing the ambulance to the most suitable hospital** using GPS-based distance, live bed availability, and specialist matching.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🏥 Hospital Database | 6 hospitals with beds, ICU, specialists, and facilities |
| 📋 Patient Intake Form | Ambulance crew fills name, age, symptoms, severity, GPS |
| 🧠 Specialist Detection | Auto-detects required specialist from symptoms |
| 📏 Haversine Distance | Real GPS-based distance calculation |
| ⭐ Scoring Algorithm | Ranks hospitals by distance + beds + ICU + specialist |
| ✅ Bed Booking | Confirms booking and updates availability |
| 📁 Case Logging | All cases saved to `case_log.csv` |
| 📚 History View | View all past emergency cases |
| 🏥 Live Stats | View current bed availability across all hospitals |

---

## 🗂️ Project Structure

```
ambulance_routing_system/
│
├── main.py          # Entry point — main menu and flow controller
├── hospitals.py     # Hospital database and bed update functions
├── patient.py       # Patient intake form and specialist detection
├── routing.py       # Haversine distance, scoring, hospital ranking
├── booking.py       # Bed confirmation, CSV logging, history view
├── case_log.csv     # Auto-generated case history file
└── README.md        # This file
```

---

## ⚙️ How to Run

### Requirements
- Python 3.x (no external libraries needed — uses only standard library)

### Steps

```bash
# Clone the repository
git clone https://github.com/AdityaSrivastav10058/ambulance-routing-system
cd ambulance_routing_system

# Run the program
python main.py
```

---

## 🔄 Workflow

```
[Emergency Occurs]
      ↓
[Ambulance arrives → crew opens app]
      ↓
[Fill Patient Intake Form]
  - Name, age, gender
  - Symptoms (e.g., chest pain, fracture, burns)
  - Severity level (1=Critical to 4=Minor)
  - ICU needed?
  - GPS coordinates of incident
      ↓
[System auto-detects specialist needed]
  chest pain → Cardiologist
  head injury → Neurologist
  burns → Burns Specialist ... etc.
      ↓
[Haversine distance calculated to all hospitals]
      ↓
[Hospitals scored on:]
  - Distance from pickup (closer = higher score)
  - Available general beds
  - ICU availability (if needed)
  - Required specialist available
      ↓
[Top 5 hospitals displayed with ETA]
      ↓
[Crew selects hospital → bed booked]
      ↓
[Case saved to case_log.csv]
```

---

## 📊 Scoring Algorithm

Each hospital gets a score out of 110:

| Factor | Max Points |
|---|---|
| Distance (closer = more) | 40 |
| Available general beds | 20 |
| ICU availability (if needed) | 20 |
| Specialist match | 30 |

Hospitals with no beds or emergency closed are excluded.

---

## 🗺️ Distance Calculation

Uses the **Haversine Formula** — the standard formula for computing great-circle distance between two GPS coordinates:

```
a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
distance = 2 × R × atan2(√a, √(1−a))
```

Where R = 6371 km (Earth's radius).

---

## 📁 CSV Case Log Format

Each case is saved with:
- Case ID, timestamp, patient details
- Incident description, symptoms, specialist needed
- Assigned hospital name, address, contact
- Distance, ETA, bed type booked, status

---

## 🧩 Python Concepts Demonstrated

- **Functions & Modules**: 5 separate `.py` modules
- **Dictionaries**: Hospital database, patient records
- **Lists**: Ranked hospital results, symptoms
- **File Handling**: CSV read/write using `csv` module
- **Math Module**: Haversine formula with `math.radians`, `math.sin`, etc.
- **String Operations**: Parsing symptoms, formatting output
- **UUID & Datetime**: Case ID generation and timestamping
- **Error Handling**: try/except for input validation
- **CLI Design**: Clean formatted terminal UI with icons

---

## 🎯 Sample Run

```
🚑  SMART AMBULANCE DISPATCH SYSTEM
Emergency Hospital Routing with Specialist Matching

=== PATIENT INTAKE FORM ===
Patient Name: Raju Verma
Age: 45 | Gender: M
Symptoms: chest pain, unconscious
Severity: 1 (Critical) | ICU: Yes
Location: Ring Road, Delhi

Specialist auto-detected: Cardiologist

=== HOSPITALS RANKED ===
[1] City General Hospital — 2.3 km, ETA 3 min, ⭐ 95/110
    ✅ Cardiologist: 2 | ICU: 8 beds
[2] Apollo Medical Center — 3.1 km, ETA 4 min, ⭐ 87/110
    ✅ Cardiologist: 3 | ICU: 2 beds
...

Booking confirmed at City General Hospital!
📝 Case logged to case_log.csv
```

---

## 👤 Author

**Aditya Srivastav**  
Roll No: 25BEC10058  
Course: Python Essentials — VITyarthi Platform
