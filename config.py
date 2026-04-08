"""
Configuration for The Lobbying Subsidy Tracker.
Loads API keys, defines PAC-to-industry mappings, target legislators,
and policy area mappings for the Congress.gov API.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── API Configuration ─────────────────────────────────────────────────────────
API_KEY = os.getenv("API_KEY")
FEC_BASE_URL = "https://api.open.fec.gov/v1"
CONGRESS_BASE_URL = "https://api.congress.gov/v3"
ELECTION_CYCLE = 2022       # Fully-reported cycle
CONGRESS_NUMBER = 117       # 117th Congress corresponds to 2021-2022

# ── Rate-Limiting ─────────────────────────────────────────────────────────────
FEC_REQUEST_DELAY = 0.6     # seconds between FEC API calls (1000/hr limit)
CONGRESS_REQUEST_DELAY = 0.3  # seconds between Congress API calls (5000/hr)

# ── Industry → PAC Mapping ────────────────────────────────────────────────────
# Each industry maps to a list of known PACs with their FEC committee IDs.
INDUSTRY_PACS = {
    "Fossil Fuels": [
        {"name": "ExxonMobil PAC",              "committee_id": "C00121368"},
        {"name": "Chevron Employees PAC",       "committee_id": "C00035006"},
        {"name": "Koch Industries PAC",         "committee_id": "C00236489"},
        {"name": "ConocoPhillips Spirit PAC",   "committee_id": "C00112896"},
        {"name": "Marathon Petroleum PAC",      "committee_id": "C00496307"},
    ],
    "Data Centers / Tech": [
        {"name": "Google NetPAC",               "committee_id": "C00428623"},
        {"name": "Meta Platforms PAC",          "committee_id": "C00502906"},
        {"name": "Amazon PAC",                  "committee_id": "C00360354"},
        {"name": "Microsoft PAC",               "committee_id": "C00227546"},
    ],
    "Defense / Iran": [
        {"name": "Lockheed Martin PAC",         "committee_id": "C00303024"},
        {"name": "Northrop Grumman PAC",        "committee_id": "C00088591"},
        {"name": "RTX (Raytheon) PAC",          "committee_id": "C00097568"},
        {"name": "General Dynamics PAC",        "committee_id": "C00078451"},
        {"name": "Boeing PAC",                  "committee_id": "C00142711"},
        {"name": "L3Harris PAC",                "committee_id": "C00100321"},
    ],
}

# ── Industry → Congress.gov Policy Areas ──────────────────────────────────────
# Used to count how many of a legislator's sponsored bills relate to each topic.
INDUSTRY_POLICY_AREAS = {
    "Fossil Fuels": [
        "Energy",
        "Environmental Protection",
        "Public Lands and Natural Resources",
    ],
    "Data Centers / Tech": [
        "Science, Technology, Communications",
        "Energy",
        "Commerce",
    ],
    "Defense / Iran": [
        "Armed Forces and National Security",
        "International Affairs",
        "Emergency Management",
    ],
}

# ── Target Legislators ────────────────────────────────────────────────────────
# Members from Energy & Commerce, Armed Services, and Science/Tech committees
# during the 117th Congress (2022 cycle).
# Format: {"name", "bioguide_id", "party", "state", "committees"}
#
# FEC candidate_id will be looked up dynamically via the FEC /candidates/search/
# endpoint using the legislator's name — this avoids hardcoding stale IDs.

TARGET_LEGISLATORS = [
    # ── Energy & Commerce Committee ───────────────────────────────────────
    {"name": "Frank Pallone",          "bioguide_id": "P000034", "party": "D", "state": "NJ",
     "committees": ["Energy and Commerce"]},
    {"name": "Cathy McMorris Rodgers", "bioguide_id": "M001159", "party": "R", "state": "WA",
     "committees": ["Energy and Commerce"]},
    {"name": "Bobby Rush",             "bioguide_id": "R000515", "party": "D", "state": "IL",
     "committees": ["Energy and Commerce"]},
    {"name": "Fred Upton",             "bioguide_id": "U000031", "party": "R", "state": "MI",
     "committees": ["Energy and Commerce"]},
    {"name": "Michael Burgess",        "bioguide_id": "B001248", "party": "R", "state": "TX",
     "committees": ["Energy and Commerce"]},
    {"name": "Diana DeGette",          "bioguide_id": "D000197", "party": "D", "state": "CO",
     "committees": ["Energy and Commerce"]},
    {"name": "Jan Schakowsky",         "bioguide_id": "S001145", "party": "D", "state": "IL",
     "committees": ["Energy and Commerce"]},
    {"name": "Morgan Griffith",        "bioguide_id": "G000568", "party": "R", "state": "VA",
     "committees": ["Energy and Commerce"]},
    {"name": "Gus Bilirakis",          "bioguide_id": "B001257", "party": "R", "state": "FL",
     "committees": ["Energy and Commerce"]},
    {"name": "Kurt Schrader",          "bioguide_id": "S001180", "party": "D", "state": "OR",
     "committees": ["Energy and Commerce"]},

    # ── Armed Services Committee ──────────────────────────────────────────
    {"name": "Adam Smith",             "bioguide_id": "S000510", "party": "D", "state": "WA",
     "committees": ["Armed Services"]},
    {"name": "Mike Rogers",            "bioguide_id": "R000575", "party": "R", "state": "AL",
     "committees": ["Armed Services"]},
    {"name": "Joe Courtney",           "bioguide_id": "C001069", "party": "D", "state": "CT",
     "committees": ["Armed Services"]},
    {"name": "Michael Turner",         "bioguide_id": "T000463", "party": "R", "state": "OH",
     "committees": ["Armed Services"]},
    {"name": "John Garamendi",         "bioguide_id": "G000559", "party": "D", "state": "CA",
     "committees": ["Armed Services"]},
    {"name": "Doug Lamborn",           "bioguide_id": "L000564", "party": "R", "state": "CO",
     "committees": ["Armed Services"]},
    {"name": "Rob Wittman",            "bioguide_id": "W000804", "party": "R", "state": "VA",
     "committees": ["Armed Services"]},
    {"name": "Ruben Gallego",          "bioguide_id": "G000574", "party": "D", "state": "AZ",
     "committees": ["Armed Services"]},
    {"name": "Don Bacon",              "bioguide_id": "B001298", "party": "R", "state": "NE",
     "committees": ["Armed Services"]},
    {"name": "Elissa Slotkin",         "bioguide_id": "S001208", "party": "D", "state": "MI",
     "committees": ["Armed Services"]},
    {"name": "Jim Banks",              "bioguide_id": "B001299", "party": "R", "state": "IN",
     "committees": ["Armed Services"]},
    {"name": "Jason Crow",             "bioguide_id": "C001121", "party": "D", "state": "CO",
     "committees": ["Armed Services"]},
    {"name": "Ro Khanna",              "bioguide_id": "K000389", "party": "D", "state": "CA",
     "committees": ["Armed Services"]},
    {"name": "Matt Gaetz",             "bioguide_id": "G000578", "party": "R", "state": "FL",
     "committees": ["Armed Services"]},
    {"name": "Mikie Sherrill",         "bioguide_id": "S001207", "party": "D", "state": "NJ",
     "committees": ["Armed Services"]},
    {"name": "Mike Waltz",             "bioguide_id": "W000823", "party": "R", "state": "FL",
     "committees": ["Armed Services"]},
    {"name": "Elaine Luria",           "bioguide_id": "L000591", "party": "D", "state": "VA",
     "committees": ["Armed Services"]},
    {"name": "Mike Gallagher",         "bioguide_id": "G000579", "party": "R", "state": "WI",
     "committees": ["Armed Services"]},
    {"name": "Seth Moulton",           "bioguide_id": "M001196", "party": "D", "state": "MA",
     "committees": ["Armed Services"]},
    {"name": "Liz Cheney",             "bioguide_id": "C001109", "party": "R", "state": "WY",
     "committees": ["Armed Services"]},

    # ── Science, Space & Technology Committee (Tech / Data Centers) ───────
    {"name": "Eddie Bernice Johnson",  "bioguide_id": "J000126", "party": "D", "state": "TX",
     "committees": ["Science, Space, and Technology"]},
    {"name": "Frank Lucas",            "bioguide_id": "L000491", "party": "R", "state": "OK",
     "committees": ["Science, Space, and Technology"]},
    {"name": "Zoe Lofgren",            "bioguide_id": "L000397", "party": "D", "state": "CA",
     "committees": ["Science, Space, and Technology"]},
    {"name": "Bill Foster",            "bioguide_id": "F000454", "party": "D", "state": "IL",
     "committees": ["Science, Space, and Technology"]},
    {"name": "Haley Stevens",          "bioguide_id": "S001215", "party": "D", "state": "MI",
     "committees": ["Science, Space, and Technology"]},
    {"name": "Randy Weber",            "bioguide_id": "W000814", "party": "R", "state": "TX",
     "committees": ["Science, Space, and Technology"]},
    {"name": "Brian Babin",            "bioguide_id": "B001291", "party": "R", "state": "TX",
     "committees": ["Science, Space, and Technology"]},
    {"name": "Jay Obernolte",          "bioguide_id": "O000019", "party": "R", "state": "CA",
     "committees": ["Science, Space, and Technology"]},
    {"name": "Suzanne Bonamici",       "bioguide_id": "B001278", "party": "D", "state": "OR",
     "committees": ["Science, Space, and Technology"]},
    {"name": "Jamaal Bowman",          "bioguide_id": "B001223", "party": "D", "state": "NY",
     "committees": ["Science, Space, and Technology"]},
]
