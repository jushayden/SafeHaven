"""
Curated emergency-contact data keyed by US state abbreviation.

Covers the 20 most populous states with specific contacts.  A generic
fallback entry (key ``"DEFAULT"``) is returned for all other states.

Each entry contains:
    general         -- universal numbers (911, etc.)
    state_agency    -- state-level emergency management office
    fema_region     -- FEMA regional office contact
    red_cross       -- American Red Cross regional chapter
    nws_office      -- National Weather Service local forecast office
"""

from typing import Any, Dict

STATE_EMERGENCY_CONTACTS: Dict[str, Dict[str, Any]] = {
    "CA": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "California Governor's Office of Emergency Services (Cal OES)",
            "phone": "1-916-845-8510",
            "website": "https://www.caloes.ca.gov",
        },
        "fema_region": {
            "name": "FEMA Region 9",
            "phone": "1-510-627-7100",
            "website": "https://www.fema.gov/about/organization/region-9",
        },
        "red_cross": {
            "name": "American Red Cross - California Region",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/california.html",
        },
        "nws_office": {
            "name": "NWS Los Angeles / San Francisco",
            "phone": "1-805-988-6610",
            "website": "https://www.weather.gov/lox/",
        },
    },
    "TX": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "Texas Division of Emergency Management (TDEM)",
            "phone": "1-512-424-2208",
            "website": "https://tdem.texas.gov",
        },
        "fema_region": {
            "name": "FEMA Region 6",
            "phone": "1-940-898-5399",
            "website": "https://www.fema.gov/about/organization/region-6",
        },
        "red_cross": {
            "name": "American Red Cross - Texas Gulf Coast Region",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/texas.html",
        },
        "nws_office": {
            "name": "NWS Houston / Fort Worth",
            "phone": "1-281-337-5074",
            "website": "https://www.weather.gov/hgx/",
        },
    },
    "FL": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "Florida Division of Emergency Management (FDEM)",
            "phone": "1-850-815-4000",
            "website": "https://www.floridadisaster.org",
        },
        "fema_region": {
            "name": "FEMA Region 4",
            "phone": "1-770-220-5200",
            "website": "https://www.fema.gov/about/organization/region-4",
        },
        "red_cross": {
            "name": "American Red Cross - Florida Region",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/florida.html",
        },
        "nws_office": {
            "name": "NWS Miami / Tampa Bay",
            "phone": "1-305-229-4522",
            "website": "https://www.weather.gov/mfl/",
        },
    },
    "NY": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "New York State Division of Homeland Security and Emergency Services (DHSES)",
            "phone": "1-518-292-2301",
            "website": "https://www.dhses.ny.gov",
        },
        "fema_region": {
            "name": "FEMA Region 2",
            "phone": "1-212-680-3600",
            "website": "https://www.fema.gov/about/organization/region-2",
        },
        "red_cross": {
            "name": "American Red Cross - Greater New York Region",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/new-york.html",
        },
        "nws_office": {
            "name": "NWS New York City",
            "phone": "1-631-924-0517",
            "website": "https://www.weather.gov/okx/",
        },
    },
    "PA": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "Pennsylvania Emergency Management Agency (PEMA)",
            "phone": "1-717-651-2001",
            "website": "https://www.pema.pa.gov",
        },
        "fema_region": {
            "name": "FEMA Region 3",
            "phone": "1-215-931-5608",
            "website": "https://www.fema.gov/about/organization/region-3",
        },
        "red_cross": {
            "name": "American Red Cross - Southeastern Pennsylvania",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/pennsylvania.html",
        },
        "nws_office": {
            "name": "NWS Philadelphia / State College",
            "phone": "1-814-231-2295",
            "website": "https://www.weather.gov/phi/",
        },
    },
    "IL": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "Illinois Emergency Management Agency (IEMA)",
            "phone": "1-217-782-2700",
            "website": "https://www.illinois.gov/iema",
        },
        "fema_region": {
            "name": "FEMA Region 5",
            "phone": "1-312-408-5500",
            "website": "https://www.fema.gov/about/organization/region-5",
        },
        "red_cross": {
            "name": "American Red Cross - Chicago & Northern Illinois",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/illinois.html",
        },
        "nws_office": {
            "name": "NWS Chicago",
            "phone": "1-815-834-0600",
            "website": "https://www.weather.gov/lot/",
        },
    },
    "OH": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "Ohio Emergency Management Agency (Ohio EMA)",
            "phone": "1-614-889-7150",
            "website": "https://ema.ohio.gov",
        },
        "fema_region": {
            "name": "FEMA Region 5",
            "phone": "1-312-408-5500",
            "website": "https://www.fema.gov/about/organization/region-5",
        },
        "red_cross": {
            "name": "American Red Cross - Greater Cleveland / Columbus",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/ohio.html",
        },
        "nws_office": {
            "name": "NWS Cleveland",
            "phone": "1-440-834-0059",
            "website": "https://www.weather.gov/cle/",
        },
    },
    "GA": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "Georgia Emergency Management and Homeland Security Agency (GEMA/HS)",
            "phone": "1-404-635-7000",
            "website": "https://gema.georgia.gov",
        },
        "fema_region": {
            "name": "FEMA Region 4",
            "phone": "1-770-220-5200",
            "website": "https://www.fema.gov/about/organization/region-4",
        },
        "red_cross": {
            "name": "American Red Cross - Georgia Region",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/georgia.html",
        },
        "nws_office": {
            "name": "NWS Atlanta",
            "phone": "1-770-486-1133",
            "website": "https://www.weather.gov/ffc/",
        },
    },
    "NC": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "North Carolina Emergency Management (NCEM)",
            "phone": "1-919-825-2500",
            "website": "https://www.ncdps.gov/emergency-management",
        },
        "fema_region": {
            "name": "FEMA Region 4",
            "phone": "1-770-220-5200",
            "website": "https://www.fema.gov/about/organization/region-4",
        },
        "red_cross": {
            "name": "American Red Cross - Eastern North Carolina",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/north-carolina.html",
        },
        "nws_office": {
            "name": "NWS Raleigh",
            "phone": "1-919-326-1190",
            "website": "https://www.weather.gov/rah/",
        },
    },
    "MI": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "Michigan State Police - Emergency Management Division",
            "phone": "1-517-284-3745",
            "website": "https://www.michigan.gov/msp/divisions/emhsd",
        },
        "fema_region": {
            "name": "FEMA Region 5",
            "phone": "1-312-408-5500",
            "website": "https://www.fema.gov/about/organization/region-5",
        },
        "red_cross": {
            "name": "American Red Cross - Michigan Region",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/michigan.html",
        },
        "nws_office": {
            "name": "NWS Detroit",
            "phone": "1-248-620-2355",
            "website": "https://www.weather.gov/dtx/",
        },
    },
    "NJ": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "New Jersey Office of Emergency Management (NJOEM)",
            "phone": "1-609-538-6050",
            "website": "https://www.nj.gov/njoem/",
        },
        "fema_region": {
            "name": "FEMA Region 2",
            "phone": "1-212-680-3600",
            "website": "https://www.fema.gov/about/organization/region-2",
        },
        "red_cross": {
            "name": "American Red Cross - New Jersey Region",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/new-jersey.html",
        },
        "nws_office": {
            "name": "NWS Mount Holly",
            "phone": "1-609-261-6600",
            "website": "https://www.weather.gov/phi/",
        },
    },
    "VA": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "Virginia Department of Emergency Management (VDEM)",
            "phone": "1-804-897-6500",
            "website": "https://www.vaemergency.gov",
        },
        "fema_region": {
            "name": "FEMA Region 3",
            "phone": "1-215-931-5608",
            "website": "https://www.fema.gov/about/organization/region-3",
        },
        "red_cross": {
            "name": "American Red Cross - Virginia Region",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/virginia.html",
        },
        "nws_office": {
            "name": "NWS Sterling (Washington DC area)",
            "phone": "1-703-996-2200",
            "website": "https://www.weather.gov/lwx/",
        },
    },
    "WA": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "Washington Emergency Management Division (WA EMD)",
            "phone": "1-253-512-7000",
            "website": "https://mil.wa.gov/emergency-management-division",
        },
        "fema_region": {
            "name": "FEMA Region 10",
            "phone": "1-425-487-4600",
            "website": "https://www.fema.gov/about/organization/region-10",
        },
        "red_cross": {
            "name": "American Red Cross - Northwest Region",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/washington.html",
        },
        "nws_office": {
            "name": "NWS Seattle",
            "phone": "1-206-526-6087",
            "website": "https://www.weather.gov/sew/",
        },
    },
    "AZ": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "Arizona Department of Emergency and Military Affairs (DEMA)",
            "phone": "1-602-464-6200",
            "website": "https://dema.az.gov",
        },
        "fema_region": {
            "name": "FEMA Region 9",
            "phone": "1-510-627-7100",
            "website": "https://www.fema.gov/about/organization/region-9",
        },
        "red_cross": {
            "name": "American Red Cross - Arizona Region",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/arizona.html",
        },
        "nws_office": {
            "name": "NWS Phoenix",
            "phone": "1-602-275-1386",
            "website": "https://www.weather.gov/psr/",
        },
    },
    "MA": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "Massachusetts Emergency Management Agency (MEMA)",
            "phone": "1-508-820-2000",
            "website": "https://www.mass.gov/mema",
        },
        "fema_region": {
            "name": "FEMA Region 1",
            "phone": "1-617-956-7506",
            "website": "https://www.fema.gov/about/organization/region-1",
        },
        "red_cross": {
            "name": "American Red Cross - Massachusetts Region",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/massachusetts.html",
        },
        "nws_office": {
            "name": "NWS Boston",
            "phone": "1-508-622-3250",
            "website": "https://www.weather.gov/box/",
        },
    },
    "TN": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "Tennessee Emergency Management Agency (TEMA)",
            "phone": "1-615-741-0001",
            "website": "https://www.tn.gov/tema.html",
        },
        "fema_region": {
            "name": "FEMA Region 4",
            "phone": "1-770-220-5200",
            "website": "https://www.fema.gov/about/organization/region-4",
        },
        "red_cross": {
            "name": "American Red Cross - Tennessee Region",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/tennessee.html",
        },
        "nws_office": {
            "name": "NWS Nashville",
            "phone": "1-615-754-4633",
            "website": "https://www.weather.gov/ohx/",
        },
    },
    "IN": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "Indiana Department of Homeland Security (IDHS)",
            "phone": "1-317-232-3980",
            "website": "https://www.in.gov/dhs/",
        },
        "fema_region": {
            "name": "FEMA Region 5",
            "phone": "1-312-408-5500",
            "website": "https://www.fema.gov/about/organization/region-5",
        },
        "red_cross": {
            "name": "American Red Cross - Indiana Region",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/indiana.html",
        },
        "nws_office": {
            "name": "NWS Indianapolis",
            "phone": "1-317-856-0360",
            "website": "https://www.weather.gov/ind/",
        },
    },
    "MO": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "Missouri State Emergency Management Agency (SEMA)",
            "phone": "1-573-526-9100",
            "website": "https://sema.dps.mo.gov",
        },
        "fema_region": {
            "name": "FEMA Region 7",
            "phone": "1-816-283-7061",
            "website": "https://www.fema.gov/about/organization/region-7",
        },
        "red_cross": {
            "name": "American Red Cross - Missouri/Arkansas Region",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/missouri.html",
        },
        "nws_office": {
            "name": "NWS St. Louis / Kansas City",
            "phone": "1-636-441-8467",
            "website": "https://www.weather.gov/lsx/",
        },
    },
    "MD": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "Maryland Emergency Management Agency (MEMA)",
            "phone": "1-410-517-3600",
            "website": "https://mema.maryland.gov",
        },
        "fema_region": {
            "name": "FEMA Region 3",
            "phone": "1-215-931-5608",
            "website": "https://www.fema.gov/about/organization/region-3",
        },
        "red_cross": {
            "name": "American Red Cross - Central Maryland",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/maryland.html",
        },
        "nws_office": {
            "name": "NWS Baltimore / Washington",
            "phone": "1-703-996-2200",
            "website": "https://www.weather.gov/lwx/",
        },
    },
    "CO": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
        ],
        "state_agency": {
            "name": "Colorado Division of Homeland Security and Emergency Management (DHSEM)",
            "phone": "1-720-852-6600",
            "website": "https://dhsem.colorado.gov",
        },
        "fema_region": {
            "name": "FEMA Region 8",
            "phone": "1-303-235-4800",
            "website": "https://www.fema.gov/about/organization/region-8",
        },
        "red_cross": {
            "name": "American Red Cross - Colorado Region",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org/local/colorado.html",
        },
        "nws_office": {
            "name": "NWS Boulder / Denver",
            "phone": "1-303-494-3210",
            "website": "https://www.weather.gov/bou/",
        },
    },
    # ---------- DEFAULT fallback for states not listed above ----------
    "DEFAULT": {
        "general": [
            {"name": "Emergency Services", "number": "911", "description": "Police, Fire, EMS"},
            {"name": "FEMA Helpline", "number": "1-800-621-3362", "description": "FEMA Disaster Assistance"},
            {"name": "Poison Control", "number": "1-800-222-1222", "description": "National Poison Control Center"},
            {"name": "National Suicide Prevention Lifeline", "number": "988", "description": "Mental health crisis support"},
        ],
        "state_agency": {
            "name": "State Emergency Management Agency",
            "phone": "Contact your state governor's office",
            "website": "https://www.fema.gov/emergency-management-agencies",
        },
        "fema_region": {
            "name": "FEMA National",
            "phone": "1-800-621-3362",
            "website": "https://www.fema.gov",
        },
        "red_cross": {
            "name": "American Red Cross",
            "phone": "1-800-733-2767",
            "website": "https://www.redcross.org",
        },
        "nws_office": {
            "name": "National Weather Service",
            "phone": "See weather.gov for local office",
            "website": "https://www.weather.gov",
        },
    },
}


def get_emergency_contacts(state_code: str) -> Dict[str, Any]:
    """Return emergency contacts for *state_code*, falling back to defaults."""
    code = state_code.upper()
    return STATE_EMERGENCY_CONTACTS.get(code, STATE_EMERGENCY_CONTACTS["DEFAULT"])
