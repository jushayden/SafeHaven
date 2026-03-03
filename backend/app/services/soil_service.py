"""
NRCS Soil Data Access (SDA) lookup.

Queries the USDA Natural Resources Conservation Service to get soil
properties for a given coordinate. Key outputs: drainage class,
hydrologic group, and dominant soil texture — used to assess
liquefaction risk (earthquake) and flooding susceptibility.

Free, no API key required.
"""

from __future__ import annotations

import logging

import httpx

logger = logging.getLogger("safehaven.soil")

SDA_URL = "https://sdmdataaccess.sc.egov.usda.gov/Tabular/SDMTabularService/post.rest"


async def get_soil_data(
    client: httpx.AsyncClient,
    lat: float,
    lng: float,
) -> dict:
    """
    Return soil properties for the location.

    Returns
    -------
    dict with keys:
        soil_type : str | None  (dominant component name, e.g. "Myakka fine sand")
        drainage_class : str | None  (e.g. "Poorly drained", "Well drained")
        hydrologic_group : str | None  (A/B/C/D — A=sandy, D=clay)
        texture : str | None  (dominant texture description)
        liquefaction_risk : str  ("Low" / "Moderate" / "High" / "Very High" / "Unknown")
        flood_susceptibility : str  ("Low" / "Moderate" / "High" / "Unknown")
    """
    try:
        # Single query: get map unit from point, then join to component data
        query = f"""
            SELECT TOP 1
                mu.muname,
                c.compname,
                c.comppct_r,
                c.drainagecl,
                c.hydgrp,
                c.taxorder,
                c.taxsubgrp,
                c.tfact
            FROM SDA_Get_Mukey_from_intersection_with_WktWgs84(
                'point({lng} {lat})'
            ) AS mk
            INNER JOIN mapunit AS mu ON mu.mukey = mk.mukey
            INNER JOIN component AS c ON c.mukey = mk.mukey
            WHERE c.comppct_r IS NOT NULL
            ORDER BY c.comppct_r DESC
        """

        resp = await client.post(
            SDA_URL,
            json={"format": "JSON", "query": query},
            timeout=12,
        )
        resp.raise_for_status()
        data = resp.json()

        table = data.get("Table")
        if not table or len(table) == 0:
            return _empty()

        row = table[0]
        mu_name = row[0]       # map unit name
        comp_name = row[1]     # component name (e.g. "Myakka")
        drainage = row[3]      # drainage class
        hydgrp = row[4]        # hydrologic group
        tax_order = row[5]     # taxonomic order
        tax_subgrp = row[6]    # taxonomic subgroup

        # Determine texture from component/map unit name and taxonomy
        texture = _classify_texture(mu_name, comp_name, tax_order, tax_subgrp)

        # Assess liquefaction risk
        liquefaction = _assess_liquefaction(drainage, hydgrp, texture, tax_order)

        # Assess flood susceptibility from soil drainage
        flood_susc = _assess_flood_susceptibility(drainage, hydgrp)

        return {
            "soil_type": mu_name,
            "drainage_class": drainage,
            "hydrologic_group": hydgrp,
            "texture": texture,
            "liquefaction_risk": liquefaction,
            "flood_susceptibility": flood_susc,
        }

    except Exception as exc:
        logger.warning("NRCS SDA query failed: %s", exc)
        return _empty()


def _classify_texture(
    mu_name: str | None,
    comp_name: str | None,
    tax_order: str | None,
    tax_subgrp: str | None,
) -> str:
    """Classify broad soil texture from available fields."""
    combined = " ".join(
        s.lower() for s in [mu_name, comp_name, tax_order, tax_subgrp] if s
    )

    if "sand" in combined or "psamment" in combined:
        return "Sandy"
    if "silt" in combined or "loess" in combined:
        return "Silty"
    if "clay" in combined or "vert" in combined:
        return "Clay"
    if "loam" in combined:
        return "Loam"
    if "peat" in combined or "muck" in combined or "histos" in combined:
        return "Organic/Peat"
    if "rock" in combined or "lithic" in combined:
        return "Bedrock/Rocky"
    if "gravel" in combined:
        return "Gravelly"
    if "fill" in combined or "urban" in combined:
        return "Urban Fill"
    return "Mixed"


def _assess_liquefaction(
    drainage: str | None,
    hydgrp: str | None,
    texture: str,
    tax_order: str | None,
) -> str:
    """
    Assess liquefaction risk.

    Liquefaction occurs when loose, water-saturated sandy/silty soils
    lose strength during earthquake shaking. Key factors:
    - Sandy or silty texture = more prone
    - Poor drainage / high water table = more prone
    - Clay or bedrock = resistant
    """
    d = (drainage or "").lower()
    h = (hydgrp or "").upper()

    # Bedrock/rocky is inherently stable
    if texture in ("Bedrock/Rocky", "Gravelly"):
        return "Very Low"

    # Clay resists liquefaction
    if texture == "Clay":
        return "Low"

    # Sandy/silty with poor drainage = classic liquefaction scenario
    if texture in ("Sandy", "Silty", "Urban Fill"):
        if "poorly" in d or h in ("D", "C/D", "D/A"):
            return "High"
        if "somewhat poorly" in d or h in ("C", "B/D"):
            return "Moderate"
        return "Moderate"  # Sandy soil is always somewhat at risk

    # Organic/peat soils can be unstable
    if texture == "Organic/Peat":
        return "Moderate"

    # Loam with poor drainage
    if texture == "Loam":
        if "poorly" in d:
            return "Moderate"
        return "Low"

    return "Low"


def _assess_flood_susceptibility(
    drainage: str | None,
    hydgrp: str | None,
) -> str:
    """
    Assess how soil drainage affects flood risk.

    Poorly drained soils can't absorb water → surface flooding.
    Hydrologic group D = highest runoff potential.
    """
    d = (drainage or "").lower()
    h = (hydgrp or "").upper()

    if "very poorly" in d or h == "D":
        return "High"
    if "poorly" in d or h in ("C/D", "D/A", "C"):
        return "Moderate"
    if "well" in d or h in ("A", "A/D"):
        return "Low"

    return "Moderate"


def _empty() -> dict:
    return {
        "soil_type": None,
        "drainage_class": None,
        "hydrologic_group": None,
        "texture": None,
        "liquefaction_risk": "Unknown",
        "flood_susceptibility": "Unknown",
    }
