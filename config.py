from datetime import datetime

DATA_PATH_2024 = "S4 Ticket Data COMPLETE.csv"
DATA_PATH_2025 = "S5 Orders Report_04022025.csv"
CONCERT_DATES = {'FIREBIRD': datetime(2024,7,14).date(),
                'SCHEHERAZADE': datetime(2024,7,28).date(),
                 'Tchaikovsky 5': datetime(2025, 4, 1, ).date(),
                 'Beethoven 5': datetime(2025, 4, 2).date(),
                 }

ZIPCODE_URLS = {"MA": 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/ma_massachusetts_zip_codes_geo.min.json',
                "NY": 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/ny_new_york_zip_codes_geo.min.json',
                "ME": 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/refs/heads/master/me_maine_zip_codes_geo.min.json',
                "CT": 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/refs/heads/master/ct_connecticut_zip_codes_geo.min.json',
                "RI": 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/refs/heads/master/ri_rhode_island_zip_codes_geo.min.json',
                "VT": 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/refs/heads/master/vt_vermont_zip_codes_geo.min.json',
                "NH": 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/refs/heads/master/nh_new_hampshire_zip_codes_geo.min.json',
                "NJ": 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/refs/heads/master/nj_new_jersey_zip_codes_geo.min.json'}