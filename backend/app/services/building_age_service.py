"""
Census ACS Building Age lookup.

Uses the Census Bureau ACS 5-Year API (Table B25034: Year Structure Built)
to determine the age distribution of housing in the census tract containing
the given coordinates. Older structures are more vulnerable to disasters.
"""

from __future__ import annotations

import logging

import httpx

logger = logging.getLogger("safehaven.building_age")

CENSUS_GEOCODER_URL = (
    "https://geocoding.geo.census.gov/geocoder/geographies/coordinates"
)
CENSUS_ACS_URL = "https://api.census.gov/data/2022/acs/acs5"

# B25034 variables: total + each era bucket
_VARS = [
    "B25034_001E",  # Total
    "B25034_002E",  # 2020 or later
    "B25034_003E",  # 2010-2019
    "B25034_004E",  # 2000-2009
    "B25034_005E",  # 1990-1999
    "B25034_006E",  # 1980-1989
    "B25034_007E",  # 1970-1979
    "B25034_008E",  # 1960-1969
    "B25034_009E",  # 1950-1959
    "B25034_010E",  # 1940-1949
    "B25034_011E",  # 1939 or earlier
]

_ERA_LABELS = [
    "2020+", "2010-2019", "2000-2009", "1990-1999",
    "1980-1989", "1970-1979", "1960-1969", "1950-1959",
    "1940-1949", "Pre-1939",
]


async def get_building_age(
    client: httpx.AsyncClient,
    lat: float,
    lng: float,
) -> dict:
    """
    Return building age distribution for the census tract at the coordinate.

    Returns
    -------
    dict with keys:
        median_era : str | None  (e.g., "1970-1979")
        pct_pre_1980 : float | None  (percentage of structures built before 1980)
        vulnerability : str  ("Low" / "Moderate" / "High" / "Very High")
        era_distribution : list[dict] | None  (era label + count + percentage)
    """
    # Step 1: Get FIPS codes from coordinates
    try:
        geo_params = {
            "x": lng,
            "y": lat,
            "benchmark": "Public_AR_Current",
            "vintage": "Current_Current",
            "format": "json",
        }
        resp = await client.get(CENSUS_GEOCODER_URL, params=geo_params, timeout=10)
        resp.raise_for_status()
        geo_data = resp.json()

        geographies = geo_data.get("result", {}).get("geographies", {})
        tracts = geographies.get("Census Tracts", [])
        if not tracts:
            return _empty()

        tract = tracts[0]
        state_fips = tract.get("STATE")
        county_fips = tract.get("COUNTY")
        tract_code = tract.get("TRACT")

        if not all([state_fips, county_fips, tract_code]):
            return _empty()

    except Exception as exc:
        logger.warning("Census geocoder failed: %s", exc)
        return _empty()

    # Step 2: Query ACS B25034 for this tract
    try:
        acs_params = {
            "get": ",".join(_VARS),
            "for": f"tract:{tract_code}",
            "in": f"state:{state_fips} county:{county_fips}",
        }
        resp = await client.get(CENSUS_ACS_URL, params=acs_params, timeout=10)
        resp.raise_for_status()
        acs_data = resp.json()

        if len(acs_data) < 2:
            return _empty()

        # First row is headers, second row is data
        values = [int(v) if v and v != "null" else 0 for v in acs_data[1][:11]]
        total = values[0]
        if total == 0:
            return _empty()

        era_counts = values[1:]  # 10 era buckets

        # Build distribution
        distribution = []
        for i, label in enumerate(_ERA_LABELS):
            count = era_counts[i] if i < len(era_counts) else 0
            pct = round(count / total * 100, 1)
            distribution.append({"era": label, "count": count, "pct": pct})

        # Calculate pre-1980 percentage (indices 5-9: 1970s, 1960s, 1950s, 1940s, pre-1939)
        pre_1980 = sum(era_counts[5:])
        pct_pre_1980 = round(pre_1980 / total * 100, 1)

        # Find median era (the era containing the 50th percentile unit)
        cumulative = 0
        median_era = _ERA_LABELS[-1]
        for i, count in enumerate(era_counts):
            cumulative += count
            if cumulative >= total / 2:
                median_era = _ERA_LABELS[i]
                break

        # Vulnerability based on pre-1980 percentage
        if pct_pre_1980 >= 70:
            vulnerability = "Very High"
        elif pct_pre_1980 >= 50:
            vulnerability = "High"
        elif pct_pre_1980 >= 30:
            vulnerability = "Moderate"
        else:
            vulnerability = "Low"

        return {
            "median_era": median_era,
            "pct_pre_1980": pct_pre_1980,
            "vulnerability": vulnerability,
            "era_distribution": distribution,
        }

    except Exception as exc:
        logger.warning("Census ACS query failed: %s", exc)
        return _empty()


def _empty() -> dict:
    return {
        "median_era": None,
        "pct_pre_1980": None,
        "vulnerability": "Unknown",
        "era_distribution": None,
    }
