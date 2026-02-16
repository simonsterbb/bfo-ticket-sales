from datetime import datetime

DATA_PATH_2024 = "S4 Ticket Data COMPLETE.csv"
DATA_PATH_2025 = "Copy of S5 Orders Report_04022025_test.csv"

ATTENDEES_PATHS = {"2025": "S5 Attendees Report.csv",
                   }

DATA_PATHS = {"2024": "S4 Ticket Data COMPLETE.csv",
              "2025": "S5 Orders Report.csv",

}
CONCERT_DATES = {'FIREBIRD': datetime(2024,7,14).date(),
                'SCHEHERAZADE': datetime(2024,7,28).date(),
                 'Tchaikovsky 5': datetime(2025, 8, 3).date(),
                 'Beethoven 5': datetime(2025, 7, 13).date(),
                 }

ZIPCODE_URLS = {"MA": 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/ma_massachusetts_zip_codes_geo.min.json',
                "NY": 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/ny_new_york_zip_codes_geo.min.json',
                "ME": 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/refs/heads/master/me_maine_zip_codes_geo.min.json',
                "CT": 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/refs/heads/master/ct_connecticut_zip_codes_geo.min.json',
                "RI": 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/refs/heads/master/ri_rhode_island_zip_codes_geo.min.json',
                "VT": 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/refs/heads/master/vt_vermont_zip_codes_geo.min.json',
                "NH": 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/refs/heads/master/nh_new_hampshire_zip_codes_geo.min.json',
                "NJ": 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/refs/heads/master/nj_new_jersey_zip_codes_geo.min.json'}

CLEAN_SOURCE_DATA_STRINGS = {
    "Word of Mouth": ['friend', 'mom', 'husband', 'performer', 'david', 'alyssa', 'nick', 'invited', 'musician', 'kid',
                      'violin', 'bassoon', 'artist', 'maestra', 'member', 'brown', 'family', 'person', 'co-founders',
                      'coworker', 'conductor'],
    "NEC": ['nec', 'jordan hall', 'new soi'],
    "AI": ['(?<!.)ai', 'gemini', 'artificial intelligence', 'chatgpt'],
    "BFO Newsletter": ['email', 'bfo website'],
    "Online Events Calendar (The Boston Calendar, ArtsBoston, etc.)": ['bostix', 'looked', 'online'],
    "Flyer/Poster": ['parade'],
    "Previous BFO Event": ['previous'],
    "Social Media": ['facebook'],
    "Other": ['south cove group sale', 'the nb', 'community partner', 'ticket leap', '\\.\\.\\.'],
}
