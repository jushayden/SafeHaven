"""
Curated state-level natural-hazard risk data for all 50 US states.

Each state maps to a dict with scores (0-100) and human-readable descriptions
for four hazard categories: hurricane, flood, earthquake, and wildfire.

Scores reflect a composite of historical frequency, projected intensity, and
population-adjusted impact.  They are intentionally opinionated so that the
frontend can render meaningful visualizations even when live APIs are down.

Severity thresholds
    0-24   -> Low
    25-49  -> Moderate
    50-74  -> High
    75-100 -> Extreme
"""

from typing import Dict, Any


def severity_label(score: int) -> str:
    """Convert a 0-100 risk score into a human-readable severity label."""
    if score >= 75:
        return "Extreme"
    if score >= 50:
        return "High"
    if score >= 25:
        return "Moderate"
    return "Low"


# ---- master dataset -------------------------------------------------------

STATE_RISK_DATA: Dict[str, Dict[str, Any]] = {
    "AL": {
        "hurricane_score": 70,
        "hurricane_desc": "Alabama's Gulf Coast is highly susceptible to hurricanes and tropical storms, with major landfalls occurring every few years.",
        "flood_score": 65,
        "flood_desc": "Significant riverine and flash flooding risk, particularly in the Mobile River basin and low-lying coastal zones.",
        "earthquake_score": 10,
        "earthquake_desc": "Minimal seismic activity. Minor tremors occasionally felt from the New Madrid Seismic Zone to the north.",
        "wildfire_score": 25,
        "wildfire_desc": "Moderate wildfire risk during dry autumn months, primarily in forested northern regions.",
    },
    "AK": {
        "hurricane_score": 0,
        "hurricane_desc": "Alaska is outside the typical hurricane track. Severe storms can still affect coastal areas.",
        "flood_score": 40,
        "flood_desc": "Glacial outburst floods, snowmelt flooding, and coastal erosion threaten many communities.",
        "earthquake_score": 95,
        "earthquake_desc": "Alaska is the most seismically active state in the US, with frequent large earthquakes along the Aleutian subduction zone.",
        "wildfire_score": 55,
        "wildfire_desc": "Interior Alaska experiences large wildfire seasons driven by lightning and dry boreal forests.",
    },
    "AZ": {
        "hurricane_score": 5,
        "hurricane_desc": "Remnants of tropical storms occasionally bring heavy rain, but direct hurricane impact is extremely rare.",
        "flood_score": 35,
        "flood_desc": "Flash flooding in desert washes and slot canyons is a significant hazard during monsoon season.",
        "earthquake_score": 20,
        "earthquake_desc": "Low to moderate seismic risk concentrated near the state's western border fault systems.",
        "wildfire_score": 75,
        "wildfire_desc": "Extreme wildfire risk in forested highlands. The 2021 Telegraph Fire and 2020 Bush Fire illustrate growing danger.",
    },
    "AR": {
        "hurricane_score": 35,
        "hurricane_desc": "Tropical storm remnants can bring damaging winds and flooding, though direct hurricane strikes are uncommon.",
        "flood_score": 60,
        "flood_desc": "The Arkansas and Mississippi River systems create high flood risk, especially during spring rainfall events.",
        "earthquake_score": 30,
        "earthquake_desc": "The New Madrid Seismic Zone poses a meaningful earthquake risk to eastern Arkansas.",
        "wildfire_score": 20,
        "wildfire_desc": "Low wildfire risk overall, with occasional prescribed burn escapes in the Ozark and Ouachita forests.",
    },
    "CA": {
        "hurricane_score": 5,
        "hurricane_desc": "Tropical cyclones rarely reach California, though warming Pacific waters may increase future risk.",
        "flood_score": 55,
        "flood_desc": "Atmospheric rivers drive severe flooding, and aging levees in the Central Valley remain a critical vulnerability.",
        "earthquake_score": 90,
        "earthquake_desc": "California sits atop the San Andreas and numerous other active faults. A major earthquake is considered inevitable.",
        "wildfire_score": 90,
        "wildfire_desc": "Extreme wildfire risk across much of the state. Santa Ana and Diablo winds accelerate catastrophic fire events.",
    },
    "CO": {
        "hurricane_score": 0,
        "hurricane_desc": "Landlocked state with no hurricane risk.",
        "flood_score": 40,
        "flood_desc": "Flash flooding in mountain canyons and along the Front Range corridor is a recurring hazard.",
        "earthquake_score": 20,
        "earthquake_desc": "Low seismic risk, though induced seismicity from wastewater injection has been observed.",
        "wildfire_score": 80,
        "wildfire_desc": "Extreme wildfire risk in the wildland-urban interface. The Marshall Fire (2021) was the most destructive in state history.",
    },
    "CT": {
        "hurricane_score": 35,
        "hurricane_desc": "Nor'easters and occasional hurricanes (e.g., Superstorm Sandy) can bring destructive storm surge and winds.",
        "flood_score": 40,
        "flood_desc": "Coastal flooding and riverine flooding from heavy rain events are both significant concerns.",
        "earthquake_score": 10,
        "earthquake_desc": "Minor seismic activity. Small earthquakes are felt occasionally but rarely cause damage.",
        "wildfire_score": 5,
        "wildfire_desc": "Very low wildfire risk due to humid climate and relatively small forested areas.",
    },
    "DE": {
        "hurricane_score": 40,
        "hurricane_desc": "Low-lying coastal geography makes Delaware vulnerable to storm surge from hurricanes and nor'easters.",
        "flood_score": 50,
        "flood_desc": "Coastal and tidal flooding is a persistent challenge, exacerbated by sea-level rise.",
        "earthquake_score": 5,
        "earthquake_desc": "Very low seismic risk. Occasionally feels effects of distant earthquakes.",
        "wildfire_score": 5,
        "wildfire_desc": "Minimal wildfire risk. Flat, developed landscape limits fire spread.",
    },
    "FL": {
        "hurricane_score": 85,
        "hurricane_desc": "Florida is the most hurricane-prone state, with the entire coastline exposed to major storm landfalls.",
        "flood_score": 75,
        "flood_desc": "Extremely high flood risk from storm surge, heavy rainfall, and rising sea levels across South Florida.",
        "earthquake_score": 5,
        "earthquake_desc": "Negligible seismic risk. Florida sits on a stable carbonate platform.",
        "wildfire_score": 40,
        "wildfire_desc": "Moderate wildfire risk in interior scrubland and pine flatwoods, especially during spring dry season.",
    },
    "GA": {
        "hurricane_score": 55,
        "hurricane_desc": "Coastal Georgia faces hurricane and tropical storm threats, while inland areas can see damaging winds and flooding.",
        "flood_score": 50,
        "flood_desc": "Flash flooding and riverine flooding are common, particularly in urbanized areas around Atlanta.",
        "earthquake_score": 10,
        "earthquake_desc": "Low seismic risk. Occasional minor earthquakes in the northeastern part of the state.",
        "wildfire_score": 30,
        "wildfire_desc": "Moderate wildfire risk in the Okefenokee Swamp region and north Georgia mountains during dry periods.",
    },
    "HI": {
        "hurricane_score": 60,
        "hurricane_desc": "Hawaiian islands are vulnerable to Central Pacific hurricanes. Hurricane Lane (2018) brought record rainfall.",
        "flood_score": 55,
        "flood_desc": "Orographic rainfall creates intense flash flooding on windward slopes; coastal areas face tsunami risk.",
        "earthquake_score": 70,
        "earthquake_desc": "Active volcanism on the Big Island produces frequent earthquakes. The 2018 Kilauea eruption was accompanied by a M6.9 quake.",
        "wildfire_score": 50,
        "wildfire_desc": "The 2023 Lahaina fire demonstrated catastrophic wildfire potential, driven by invasive grasses and dry leeward conditions.",
    },
    "ID": {
        "hurricane_score": 0,
        "hurricane_desc": "Landlocked state with no hurricane risk.",
        "flood_score": 30,
        "flood_desc": "Snowmelt flooding along the Snake River and its tributaries is the primary flood hazard.",
        "earthquake_score": 45,
        "earthquake_desc": "Moderate seismic risk from the Intermountain Seismic Belt and the Borah Peak fault (M7.3 in 1983).",
        "wildfire_score": 70,
        "wildfire_desc": "High wildfire risk in the forested mountains and rangeland. Large fire seasons are increasingly common.",
    },
    "IL": {
        "hurricane_score": 5,
        "hurricane_desc": "Remnant tropical moisture can cause heavy rain, but hurricane-force winds are extremely rare.",
        "flood_score": 55,
        "flood_desc": "Major Mississippi and Illinois River flooding affects large portions of the state. Chicago faces urban flash flood risk.",
        "earthquake_score": 30,
        "earthquake_desc": "The New Madrid Seismic Zone poses a significant threat to southern Illinois.",
        "wildfire_score": 5,
        "wildfire_desc": "Very low wildfire risk due to agricultural land use and humid climate.",
    },
    "IN": {
        "hurricane_score": 5,
        "hurricane_desc": "Tropical storm remnants occasionally bring heavy rain and minor wind damage.",
        "flood_score": 45,
        "flood_desc": "The Wabash and Ohio River valleys are prone to significant flooding events.",
        "earthquake_score": 20,
        "earthquake_desc": "Southwestern Indiana has moderate seismic risk from the Wabash Valley Seismic Zone.",
        "wildfire_score": 5,
        "wildfire_desc": "Very low wildfire risk. Agricultural landscape limits large fire events.",
    },
    "IA": {
        "hurricane_score": 5,
        "hurricane_desc": "Derecho events (inland hurricane-force winds) are the primary wind hazard, as seen in the 2020 derecho.",
        "flood_score": 60,
        "flood_desc": "Major flood risk along the Mississippi, Missouri, and Des Moines Rivers. The 2008 floods caused billions in damage.",
        "earthquake_score": 5,
        "earthquake_desc": "Very low seismic risk. Occasional small tremors are felt.",
        "wildfire_score": 5,
        "wildfire_desc": "Minimal wildfire risk due to the predominantly agricultural landscape.",
    },
    "KS": {
        "hurricane_score": 10,
        "hurricane_desc": "No direct hurricane risk, but severe thunderstorms and tornadoes are the primary wind hazard.",
        "flood_score": 45,
        "flood_desc": "Flash flooding from intense thunderstorms and riverine flooding along the Kansas and Arkansas Rivers.",
        "earthquake_score": 20,
        "earthquake_desc": "Induced seismicity from oil and gas operations has increased earthquake frequency in recent years.",
        "wildfire_score": 40,
        "wildfire_desc": "Grassland wildfires in western Kansas can be large and destructive, particularly during dry windy conditions.",
    },
    "KY": {
        "hurricane_score": 10,
        "hurricane_desc": "Tropical storm remnants occasionally bring heavy rain. Tornadoes are a more significant wind hazard.",
        "flood_score": 55,
        "flood_desc": "Flash flooding in Appalachian valleys is a major hazard. The 2022 eastern Kentucky floods were devastating.",
        "earthquake_score": 25,
        "earthquake_desc": "Western Kentucky has moderate seismic risk from the New Madrid Seismic Zone.",
        "wildfire_score": 15,
        "wildfire_desc": "Low wildfire risk, with occasional fires in the Daniel Boone National Forest during dry spells.",
    },
    "LA": {
        "hurricane_score": 90,
        "hurricane_desc": "Louisiana is among the most hurricane-impacted states. Katrina (2005), Laura (2020), and Ida (2021) caused catastrophic damage.",
        "flood_score": 80,
        "flood_desc": "Extreme flood risk from hurricanes, Mississippi River flooding, and subsiding coastal marshes.",
        "earthquake_score": 5,
        "earthquake_desc": "Very low seismic risk. No significant earthquake history.",
        "wildfire_score": 15,
        "wildfire_desc": "Low wildfire risk. Humid subtropical climate limits fire spread.",
    },
    "ME": {
        "hurricane_score": 20,
        "hurricane_desc": "Occasional tropical or post-tropical storms affect Maine, typically with weakened intensity.",
        "flood_score": 35,
        "flood_desc": "Spring snowmelt flooding and coastal storm surge are the primary flood hazards.",
        "earthquake_score": 10,
        "earthquake_desc": "Low seismic risk. Occasional small earthquakes are part of broader New England seismicity.",
        "wildfire_score": 10,
        "wildfire_desc": "Low wildfire risk. The 1947 Maine fires remain an outlier event.",
    },
    "MD": {
        "hurricane_score": 40,
        "hurricane_desc": "Chesapeake Bay geography amplifies storm surge. Hurricane Isabel (2003) caused major flooding.",
        "flood_score": 50,
        "flood_desc": "Coastal and tidal flooding in the Chesapeake region, plus flash flooding in the Appalachian west.",
        "earthquake_score": 5,
        "earthquake_desc": "Very low seismic risk with occasional minor tremors.",
        "wildfire_score": 5,
        "wildfire_desc": "Minimal wildfire risk due to humid climate and developed landscape.",
    },
    "MA": {
        "hurricane_score": 35,
        "hurricane_desc": "New England hurricanes, while infrequent, can be devastating. The 1938 hurricane remains a benchmark.",
        "flood_score": 45,
        "flood_desc": "Coastal flooding from nor'easters and storm surge, plus urban flooding in the Greater Boston area.",
        "earthquake_score": 15,
        "earthquake_desc": "Low seismic risk, but the Cape Ann Seismic Zone has produced notable historical earthquakes.",
        "wildfire_score": 5,
        "wildfire_desc": "Very low wildfire risk. Humid climate and managed forests limit fire activity.",
    },
    "MI": {
        "hurricane_score": 5,
        "hurricane_desc": "No hurricane risk. Severe thunderstorms and derechos are the primary wind hazards.",
        "flood_score": 35,
        "flood_desc": "Great Lakes shoreline flooding and riverine flooding from spring snowmelt are the main concerns.",
        "earthquake_score": 5,
        "earthquake_desc": "Very low seismic risk. Minor earthquakes are rare.",
        "wildfire_score": 15,
        "wildfire_desc": "Low wildfire risk, primarily in northern Michigan pine forests during dry springs.",
    },
    "MN": {
        "hurricane_score": 0,
        "hurricane_desc": "No hurricane risk.",
        "flood_score": 50,
        "flood_desc": "Red River of the North flooding is a recurring catastrophic hazard. Mississippi River flooding also significant.",
        "earthquake_score": 5,
        "earthquake_desc": "Very low seismic risk.",
        "wildfire_score": 20,
        "wildfire_desc": "Low to moderate wildfire risk in the Boundary Waters and northern forests.",
    },
    "MS": {
        "hurricane_score": 80,
        "hurricane_desc": "Mississippi's Gulf Coast is highly vulnerable. Hurricane Katrina's storm surge devastated the coast in 2005.",
        "flood_score": 70,
        "flood_desc": "Mississippi River and tributary flooding, plus hurricane-driven storm surge create extreme flood risk.",
        "earthquake_score": 15,
        "earthquake_desc": "Northern Mississippi has some risk from the New Madrid Seismic Zone.",
        "wildfire_score": 20,
        "wildfire_desc": "Low to moderate wildfire risk in pine forests during dry periods.",
    },
    "MO": {
        "hurricane_score": 10,
        "hurricane_desc": "No direct hurricane risk. Tornadoes and severe thunderstorms are the primary wind hazards.",
        "flood_score": 55,
        "flood_desc": "Major flood risk at the confluence of the Mississippi and Missouri Rivers. The 1993 Great Flood was historic.",
        "earthquake_score": 40,
        "earthquake_desc": "The New Madrid Seismic Zone in southeastern Missouri is one of the most significant seismic hazards east of the Rockies.",
        "wildfire_score": 10,
        "wildfire_desc": "Low wildfire risk. Occasional grass and brush fires in the Ozarks.",
    },
    "MT": {
        "hurricane_score": 0,
        "hurricane_desc": "Landlocked state with no hurricane risk.",
        "flood_score": 35,
        "flood_desc": "Snowmelt flooding along the Missouri and Yellowstone Rivers. Flash flooding in mountainous terrain.",
        "earthquake_score": 50,
        "earthquake_desc": "Moderate to high seismic risk in western Montana near the Intermountain Seismic Belt. The 1959 Hebgen Lake earthquake (M7.3) was catastrophic.",
        "wildfire_score": 70,
        "wildfire_desc": "High wildfire risk in forested mountains. Large fires are a near-annual occurrence in western Montana.",
    },
    "NE": {
        "hurricane_score": 0,
        "hurricane_desc": "No hurricane risk. Severe thunderstorms and tornadoes are significant hazards.",
        "flood_score": 50,
        "flood_desc": "The 2019 bomb cyclone caused catastrophic flooding along the Missouri and Platte Rivers.",
        "earthquake_score": 5,
        "earthquake_desc": "Very low seismic risk.",
        "wildfire_score": 30,
        "wildfire_desc": "Moderate wildfire risk in the Nebraska Sandhills and Pine Ridge grasslands.",
    },
    "NV": {
        "hurricane_score": 0,
        "hurricane_desc": "No hurricane risk.",
        "flood_score": 25,
        "flood_desc": "Flash flooding in desert washes during monsoon season. Las Vegas has experienced significant flash flood events.",
        "earthquake_score": 55,
        "earthquake_desc": "High seismic risk in western Nevada. The Walker Lane fault zone produces significant earthquakes.",
        "wildfire_score": 60,
        "wildfire_desc": "High wildfire risk driven by invasive cheatgrass fueling range fires across the Great Basin.",
    },
    "NH": {
        "hurricane_score": 20,
        "hurricane_desc": "Occasional post-tropical storms bring damaging winds and rain.",
        "flood_score": 35,
        "flood_desc": "Spring snowmelt and heavy rain events drive riverine flooding, particularly along the Merrimack River.",
        "earthquake_score": 10,
        "earthquake_desc": "Low seismic risk. Part of broader New England seismic activity.",
        "wildfire_score": 5,
        "wildfire_desc": "Very low wildfire risk.",
    },
    "NJ": {
        "hurricane_score": 45,
        "hurricane_desc": "Superstorm Sandy (2012) demonstrated New Jersey's extreme vulnerability to hurricane storm surge.",
        "flood_score": 55,
        "flood_desc": "Coastal flooding, tidal flooding, and intense rainstorm flooding (Ida, 2021) are major hazards.",
        "earthquake_score": 10,
        "earthquake_desc": "Low seismic risk. Occasional small earthquakes from the Ramapo Fault zone.",
        "wildfire_score": 15,
        "wildfire_desc": "Pine Barrens region has moderate wildfire risk, but overall state risk is low.",
    },
    "NM": {
        "hurricane_score": 5,
        "hurricane_desc": "Occasional remnant tropical moisture brings heavy rain but no direct hurricane threat.",
        "flood_score": 30,
        "flood_desc": "Flash flooding in arroyos and desert terrain is a significant hazard during monsoon season.",
        "earthquake_score": 25,
        "earthquake_desc": "Moderate seismic risk along the Rio Grande Rift zone.",
        "wildfire_score": 80,
        "wildfire_desc": "Extreme wildfire risk. The 2022 Hermit's Peak/Calf Canyon Fire was the largest in state history.",
    },
    "NY": {
        "hurricane_score": 40,
        "hurricane_desc": "Superstorm Sandy caused catastrophic flooding in NYC. Long Island and coastal areas remain highly vulnerable.",
        "flood_score": 50,
        "flood_desc": "Urban flooding in NYC, Hudson River flooding, and Finger Lakes / Mohawk River flooding are key risks.",
        "earthquake_score": 15,
        "earthquake_desc": "Low seismic risk, but the NYC metro area could experience amplified impacts from even moderate quakes.",
        "wildfire_score": 5,
        "wildfire_desc": "Very low wildfire risk.",
    },
    "NC": {
        "hurricane_score": 70,
        "hurricane_desc": "North Carolina's Outer Banks and coast are frequently struck by hurricanes. Florence (2018) caused catastrophic inland flooding.",
        "flood_score": 65,
        "flood_desc": "Extreme flood risk from hurricanes, river flooding, and dam failures in the Piedmont.",
        "earthquake_score": 10,
        "earthquake_desc": "Low seismic risk with occasional minor earthquakes in the western mountains.",
        "wildfire_score": 20,
        "wildfire_desc": "Low to moderate wildfire risk in the Appalachian mountains during autumn.",
    },
    "ND": {
        "hurricane_score": 0,
        "hurricane_desc": "No hurricane risk.",
        "flood_score": 55,
        "flood_desc": "Red River flooding is a catastrophic, recurring hazard. The 2009 flood threatened Fargo with record crests.",
        "earthquake_score": 5,
        "earthquake_desc": "Very low seismic risk, though some induced seismicity from oil production in the Bakken.",
        "wildfire_score": 25,
        "wildfire_desc": "Moderate grassland fire risk in western North Dakota.",
    },
    "OH": {
        "hurricane_score": 5,
        "hurricane_desc": "Tropical storm remnants occasionally bring heavy rain. Tornadoes are a more significant wind threat.",
        "flood_score": 45,
        "flood_desc": "Ohio River flooding and flash flooding in urban areas are significant hazards.",
        "earthquake_score": 15,
        "earthquake_desc": "Low seismic risk. Some induced seismicity from wastewater injection wells.",
        "wildfire_score": 5,
        "wildfire_desc": "Very low wildfire risk.",
    },
    "OK": {
        "hurricane_score": 30,
        "hurricane_desc": "No direct hurricane risk, but Oklahoma is in Tornado Alley with extreme severe thunderstorm and tornado frequency.",
        "flood_score": 50,
        "flood_desc": "Flash flooding from severe thunderstorms and riverine flooding along the Arkansas and Red Rivers.",
        "earthquake_score": 40,
        "earthquake_desc": "Dramatic increase in induced seismicity from wastewater disposal. Oklahoma briefly surpassed California in earthquake frequency.",
        "wildfire_score": 45,
        "wildfire_desc": "Moderate to high wildfire risk in western grasslands, particularly during winter and spring droughts.",
    },
    "OR": {
        "hurricane_score": 0,
        "hurricane_desc": "No hurricane risk.",
        "flood_score": 40,
        "flood_desc": "Atmospheric river-driven flooding in the Willamette Valley and coastal flooding from winter storms.",
        "earthquake_score": 70,
        "earthquake_desc": "The Cascadia Subduction Zone poses a megathrust earthquake risk (potentially M9+). Portland sits near active crustal faults.",
        "wildfire_score": 80,
        "wildfire_desc": "Extreme wildfire risk. The 2020 Labor Day fires burned over 1 million acres in days.",
    },
    "PA": {
        "hurricane_score": 20,
        "hurricane_desc": "Tropical storm remnants can bring heavy flooding. Hurricane Agnes (1972) caused historic damage.",
        "flood_score": 50,
        "flood_desc": "Flash flooding in steep Appalachian valleys and riverine flooding along the Susquehanna and Delaware Rivers.",
        "earthquake_score": 10,
        "earthquake_desc": "Low seismic risk. Occasional minor earthquakes.",
        "wildfire_score": 10,
        "wildfire_desc": "Low wildfire risk, primarily in the Pocono Mountains during dry spring seasons.",
    },
    "RI": {
        "hurricane_score": 40,
        "hurricane_desc": "Rhode Island is exposed to hurricane storm surge across its extensive coastline. The 1938 and 1954 hurricanes were devastating.",
        "flood_score": 45,
        "flood_desc": "Coastal flooding and riverine flooding from heavy rain events. The 2010 floods were historic.",
        "earthquake_score": 10,
        "earthquake_desc": "Low seismic risk.",
        "wildfire_score": 5,
        "wildfire_desc": "Very low wildfire risk.",
    },
    "SC": {
        "hurricane_score": 70,
        "hurricane_desc": "South Carolina's coast is highly exposed to hurricanes. Hugo (1989) and Matthew (2016) caused widespread devastation.",
        "flood_score": 60,
        "flood_desc": "Hurricane-driven flooding, dam failures, and coastal flooding are major risks.",
        "earthquake_score": 25,
        "earthquake_desc": "The Charleston area has moderate seismic risk. The 1886 Charleston earthquake (estimated M7) was one of the most damaging in the eastern US.",
        "wildfire_score": 20,
        "wildfire_desc": "Low to moderate wildfire risk in the coastal plain during dry seasons.",
    },
    "SD": {
        "hurricane_score": 0,
        "hurricane_desc": "No hurricane risk.",
        "flood_score": 40,
        "flood_desc": "Flash flooding from severe thunderstorms and snowmelt flooding along the Missouri River.",
        "earthquake_score": 5,
        "earthquake_desc": "Very low seismic risk.",
        "wildfire_score": 35,
        "wildfire_desc": "Moderate wildfire risk in the Black Hills and western grasslands.",
    },
    "TN": {
        "hurricane_score": 15,
        "hurricane_desc": "Tropical storm remnants bring heavy rain. Tornadoes are a more significant wind hazard.",
        "flood_score": 55,
        "flood_desc": "The 2010 Nashville flood demonstrated the state's vulnerability. Flash flooding in Appalachian valleys is also significant.",
        "earthquake_score": 35,
        "earthquake_desc": "Western Tennessee has moderate to high seismic risk from the New Madrid Seismic Zone.",
        "wildfire_score": 20,
        "wildfire_desc": "Low to moderate wildfire risk in the Great Smoky Mountains during drought years.",
    },
    "TX": {
        "hurricane_score": 75,
        "hurricane_desc": "Texas Gulf Coast faces major hurricane risk. Harvey (2017) brought unprecedented flooding to Houston.",
        "flood_score": 70,
        "flood_desc": "Extreme flood risk from hurricanes, flash flooding in Hill Country, and riverine flooding statewide.",
        "earthquake_score": 15,
        "earthquake_desc": "Low seismic risk, though induced seismicity in the Permian Basin has increased.",
        "wildfire_score": 65,
        "wildfire_desc": "High wildfire risk, particularly in the western part of the state. The 2024 Smokehouse Creek Fire was the largest in Texas history.",
    },
    "UT": {
        "hurricane_score": 0,
        "hurricane_desc": "No hurricane risk.",
        "flood_score": 25,
        "flood_desc": "Flash flooding in slot canyons and desert terrain. Snowmelt flooding along the Wasatch Front.",
        "earthquake_score": 55,
        "earthquake_desc": "The Wasatch Fault running through Salt Lake City poses significant seismic risk. A major earthquake is overdue.",
        "wildfire_score": 60,
        "wildfire_desc": "High wildfire risk in the wildland-urban interface along the Wasatch Front and in southern Utah.",
    },
    "VT": {
        "hurricane_score": 15,
        "hurricane_desc": "Post-tropical storms like Irene (2011) can cause catastrophic flooding in Vermont's narrow river valleys.",
        "flood_score": 45,
        "flood_desc": "River flooding from heavy rain and snowmelt is the primary natural hazard.",
        "earthquake_score": 10,
        "earthquake_desc": "Low seismic risk. Minor earthquakes are occasionally felt.",
        "wildfire_score": 5,
        "wildfire_desc": "Very low wildfire risk.",
    },
    "VA": {
        "hurricane_score": 50,
        "hurricane_desc": "Coastal Virginia and the Hampton Roads area are vulnerable to hurricane storm surge and flooding.",
        "flood_score": 50,
        "flood_desc": "Coastal flooding, tidal flooding in Norfolk, and Appalachian flash flooding are significant hazards.",
        "earthquake_score": 15,
        "earthquake_desc": "Low seismic risk. The 2011 Mineral earthquake (M5.8) was widely felt but caused limited damage.",
        "wildfire_score": 15,
        "wildfire_desc": "Low wildfire risk in the Shenandoah Valley and Blue Ridge during dry autumns.",
    },
    "WA": {
        "hurricane_score": 0,
        "hurricane_desc": "No hurricane risk.",
        "flood_score": 45,
        "flood_desc": "Atmospheric river-driven flooding, particularly in the Skagit and Chehalis River valleys.",
        "earthquake_score": 80,
        "earthquake_desc": "The Cascadia Subduction Zone threatens western Washington with a potential M9+ megathrust earthquake. The Seattle Fault is also a concern.",
        "wildfire_score": 65,
        "wildfire_desc": "High wildfire risk in eastern Washington's dryland forests and the wildland-urban interface around communities.",
    },
    "WV": {
        "hurricane_score": 10,
        "hurricane_desc": "Tropical storm remnants can cause heavy rain and flooding in the mountains.",
        "flood_score": 55,
        "flood_desc": "Flash flooding in narrow Appalachian valleys is a severe and recurring hazard. The 2016 floods killed 23 people.",
        "earthquake_score": 10,
        "earthquake_desc": "Low seismic risk. Occasional minor earthquakes.",
        "wildfire_score": 15,
        "wildfire_desc": "Low wildfire risk, with occasional fires in the Monongahela National Forest.",
    },
    "WI": {
        "hurricane_score": 0,
        "hurricane_desc": "No hurricane risk.",
        "flood_score": 40,
        "flood_desc": "Riverine flooding from spring snowmelt and heavy summer rainstorms along the Mississippi and Wisconsin Rivers.",
        "earthquake_score": 5,
        "earthquake_desc": "Very low seismic risk.",
        "wildfire_score": 15,
        "wildfire_desc": "Low wildfire risk. The Peshtigo Fire (1871) remains the deadliest in US history, but modern risk is limited.",
    },
    "WY": {
        "hurricane_score": 0,
        "hurricane_desc": "No hurricane risk.",
        "flood_score": 25,
        "flood_desc": "Snowmelt flooding and flash flooding in mountainous terrain. The 2022 Yellowstone floods were exceptional.",
        "earthquake_score": 55,
        "earthquake_desc": "Yellowstone seismic swarms and western Wyoming's location on the Intermountain Seismic Belt create moderate to high risk.",
        "wildfire_score": 50,
        "wildfire_desc": "High wildfire risk in forested mountain areas, particularly in the Greater Yellowstone Ecosystem.",
    },
}


def get_state_risk(state_code: str) -> Dict[str, Any] | None:
    """
    Look up curated risk data for a US state.

    Parameters
    ----------
    state_code : str
        Two-letter state abbreviation (case-insensitive).

    Returns
    -------
    dict or None
        A dictionary with structured risk information, or ``None`` if the
        state code is not recognized.
    """
    data = STATE_RISK_DATA.get(state_code.upper())
    if data is None:
        return None

    risks = {}
    for hazard in ("hurricane", "flood", "earthquake", "wildfire"):
        score = data[f"{hazard}_score"]
        risks[hazard] = {
            "score": score,
            "severity": severity_label(score),
            "description": data[f"{hazard}_desc"],
        }

    # Overall risk is the maximum severity found across all four categories
    max_score = max(data[f"{h}_score"] for h in ("hurricane", "flood", "earthquake", "wildfire"))
    return {
        "risks": risks,
        "overall_risk": severity_label(max_score),
    }
