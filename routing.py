"""
routing.py - Distance calculation and hospital ranking algorithm
Uses Haversine formula to compute real geographic distances
Ranks hospitals by: availability + specialist match + proximity
"""

import math


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate straight-line distance between two GPS coordinates.
    Returns distance in kilometers using the Haversine formula.
    """
    R = 6371  # Earth's radius in km

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def estimate_travel_time(distance_km, traffic="moderate"):
    """
    Estimate ambulance travel time based on distance and traffic.
    Ambulance average speed with siren: 60 km/h normal, 40 km/h heavy traffic.
    """
    speed = {
        "light": 65,
        "moderate": 50,
        "heavy": 35,
    }.get(traffic, 50)

    time_hours = distance_km / speed
    time_minutes = round(time_hours * 60)
    return time_minutes


def score_hospital(hospital_data, patient, distance_km):
    """
    Score a hospital for suitability. Higher = better.

    Scoring factors:
    - Distance: closer is better (max 40 pts)
    - Bed availability: more beds = better (max 20 pts)
    - ICU availability: if needed (max 20 pts)
    - Specialist available: exact match (max 30 pts)
    - Emergency status: must be open
    """
    if not hospital_data["emergency_available"]:
        return -1  # Cannot route here

    score = 0

    # Distance score (closer = higher score, max 40)
    if distance_km <= 2:
        score += 40
    elif distance_km <= 5:
        score += 30
    elif distance_km <= 10:
        score += 20
    elif distance_km <= 20:
        score += 10
    else:
        score += 5

    # Bed availability score (max 20)
    beds = hospital_data["available_beds"]
    if beds >= 30:
        score += 20
    elif beds >= 15:
        score += 15
    elif beds >= 5:
        score += 10
    elif beds >= 1:
        score += 5
    else:
        return -1  # No beds, skip

    # ICU score (max 20)
    if patient.get("icu_required"):
        icu = hospital_data["icu_beds_available"]
        if icu >= 5:
            score += 20
        elif icu >= 2:
            score += 15
        elif icu >= 1:
            score += 8
        else:
            score -= 30  # ICU needed but none available — penalize heavily

    # Specialist match (max 30)
    specialist = patient.get("specialist_needed", "General Surgeon")
    specialist_count = hospital_data["specialists"].get(specialist, 0)
    if specialist_count >= 3:
        score += 30
    elif specialist_count == 2:
        score += 22
    elif specialist_count == 1:
        score += 15
    else:
        score += 0  # No specialist — still okay for emergencies

    return score


def find_best_hospitals(patient, all_hospitals, top_n=5):
    """
    Main routing function.
    Takes patient GPS, finds all hospitals, scores and ranks them.
    Returns sorted list of (hospital_id, hospital_data, distance, travel_time, score).
    """
    pickup_lat = patient["pickup_lat"]
    pickup_lon = patient["pickup_lon"]

    ranked = []

    for hid, hdata in all_hospitals.items():
        h_lat, h_lon = hdata["location"]
        distance = haversine_distance(pickup_lat, pickup_lon, h_lat, h_lon)
        travel_time = estimate_travel_time(distance)
        score = score_hospital(hdata, patient, distance)

        if score > 0:  # Only include viable hospitals
            ranked.append({
                "id": hid,
                "data": hdata,
                "distance_km": round(distance, 2),
                "travel_time_min": travel_time,
                "score": score,
                "specialist_available": hdata["specialists"].get(
                    patient.get("specialist_needed", ""), 0
                ) > 0,
            })

    # Sort by score descending
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked[:top_n]


def display_hospital_options(ranked_hospitals, patient):
    """
    Display hospital recommendations in a clean CLI format.
    """
    specialist = patient.get("specialist_needed", "General Surgeon")
    icu_needed = patient.get("icu_required", False)

    print("\n" + "=" * 65)
    print("     🏥  AVAILABLE HOSPITALS — RANKED BY SUITABILITY")
    print(f"     Patient needs: {specialist}", end="")
    if icu_needed:
        print(" + ICU", end="")
    print()
    print("=" * 65)

    if not ranked_hospitals:
        print("\n  ⚠️  NO SUITABLE HOSPITALS FOUND NEARBY.")
        print("  Please extend search radius or contact emergency control.\n")
        return

    for i, h in enumerate(ranked_hospitals, 1):
        hdata = h["data"]
        specialist_count = hdata["specialists"].get(specialist, 0)
        match_icon = "✅" if h["specialist_available"] else "⚠️ "
        icu_icon = "🛏️ ICU:" + str(hdata["icu_beds_available"]) if icu_needed else ""

        print(f"\n  [{i}] {hdata['name']}")
        print(f"       📍 {hdata['address']}")
        print(f"       📏 Distance : {h['distance_km']} km")
        print(f"       🕐 ETA      : ~{h['travel_time_min']} minutes")
        print(f"       🛏️  Gen Beds : {hdata['available_beds']} available  {icu_icon}")
        print(f"       {match_icon} {specialist}: {specialist_count} available")
        print(f"       🏥 Facilities: {', '.join(hdata['facilities'])}")
        print(f"       📞 Contact  : {hdata['contact']}")
        print(f"       ⭐ Score    : {h['score']}/110")
        print(f"       {'─'*50}")
