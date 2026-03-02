"""
Proximity-to-coast calculation.

Uses a simplified set of US coastline reference points to estimate how
far inland a location is.  Closer to the coast = higher storm surge and
hurricane risk.
"""

from __future__ import annotations

import math

# Representative coastline points along the US Atlantic, Gulf, and Pacific coasts.
# These are spaced roughly every ~50-100 miles along the coast.
_COASTLINE_POINTS: list[tuple[float, float]] = [
    # Atlantic coast (north to south)
    (44.65, -67.20),  # Maine
    (43.07, -70.76),  # New Hampshire
    (42.36, -70.97),  # Boston
    (41.49, -71.31),  # Rhode Island
    (41.04, -71.95),  # Connecticut
    (40.57, -73.97),  # NYC
    (39.36, -74.42),  # Atlantic City
    (38.78, -75.09),  # Delaware
    (37.00, -76.33),  # Virginia Beach
    (35.78, -75.53),  # Outer Banks
    (34.21, -77.89),  # Wilmington NC
    (33.84, -78.66),  # Myrtle Beach
    (32.78, -79.93),  # Charleston
    (32.08, -81.09),  # Savannah
    (30.33, -81.66),  # Jacksonville
    (29.21, -81.02),  # Daytona
    (28.03, -80.60),  # Melbourne FL
    (26.71, -80.05),  # West Palm Beach
    (25.76, -80.19),  # Miami
    (24.56, -81.80),  # Key West
    # Gulf coast (west from Florida)
    (26.64, -81.87),  # Fort Myers
    (27.95, -82.46),  # Tampa
    (30.40, -87.21),  # Pensacola
    (30.25, -88.07),  # Mobile
    (30.37, -89.09),  # Biloxi
    (29.95, -90.07),  # New Orleans
    (29.31, -94.80),  # Galveston
    (27.80, -97.40),  # Corpus Christi
    (26.07, -97.21),  # South Padre
    # Pacific coast (south to north)
    (32.72, -117.16),  # San Diego
    (33.74, -118.29),  # Long Beach
    (34.01, -118.49),  # Santa Monica
    (34.41, -119.69),  # Santa Barbara
    (35.37, -120.85),  # San Luis Obispo
    (36.60, -121.89),  # Monterey
    (37.77, -122.51),  # San Francisco
    (38.34, -123.06),  # Bodega Bay
    (40.80, -124.16),  # Eureka
    (42.05, -124.28),  # Oregon border
    (43.37, -124.22),  # Coos Bay
    (44.63, -124.05),  # Newport OR
    (45.98, -123.93),  # Astoria
    (46.90, -124.10),  # Westport WA
    (47.56, -122.34),  # Seattle
    (48.41, -122.67),  # Anacortes
    # Hawaii
    (21.31, -157.86),  # Honolulu
    # Alaska (major coastal cities)
    (61.22, -149.90),  # Anchorage
    (58.30, -134.42),  # Juneau
]


def _haversine_miles(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Great-circle distance in miles between two points."""
    R = 3958.8  # Earth radius in miles
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlng / 2) ** 2
    )
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def get_coast_proximity(lat: float, lng: float) -> dict:
    """
    Calculate approximate distance to the nearest coastline.

    Returns
    -------
    dict with keys:
        coast_distance_miles : float
        coast_zone : str  ("Coastal" / "Near-Coast" / "Inland" / "Deep Inland")
    """
    min_dist = min(
        _haversine_miles(lat, lng, clat, clng)
        for clat, clng in _COASTLINE_POINTS
    )
    min_dist = round(min_dist, 1)

    if min_dist <= 10:
        zone = "Coastal"
    elif min_dist <= 50:
        zone = "Near-Coast"
    elif min_dist <= 150:
        zone = "Inland"
    else:
        zone = "Deep Inland"

    return {
        "coast_distance_miles": min_dist,
        "coast_zone": zone,
    }
