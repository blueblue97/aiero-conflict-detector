
import math

# Function to calculate distance between two coordinates (Haversine formula)
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c * 1000  # Return distance in meters

# Core function to detect conflicts in aircraft states
def detect_conflicts(states, horizontal_threshold=5000, vertical_threshold=300):
    conflicts = []
    for i in range(len(states)):
        for j in range(i+1, len(states)):
            a1 = states[i]
            a2 = states[j]

            if not all([a1[5], a1[6], a1[7], a2[5], a2[6], a2[7]]):
                continue  # skip if data missing

            lat1, lon1, alt1 = a1[6], a1[5], a1[7]
            lat2, lon2, alt2 = a2[6], a2[5], a2[7]

            h_dist = haversine_distance(lat1, lon1, lat2, lon2)
            v_dist = abs(alt1 - alt2)

            if h_dist < horizontal_threshold and v_dist < vertical_threshold:
                conflicts.append({
                    "aircraft_1": a1[0],
                    "aircraft_2": a2[0],
                    "horizontal_distance_m": h_dist,
                    "vertical_distance_m": v_dist
                })
    return conflicts
