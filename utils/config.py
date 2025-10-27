CATEGORY_ORDER = ['tops', 'bottoms', 'coats', 'accessories', 'precipitation', 'wind', 'lightning']

# Weather Thresholds
WIND_MODERATE = 7.9
WIND_STRONG = 10.8

PRECIP_LIGHT = 0.5
PRECIP_MODERATE = 1.0

SNOW_VARIANTS = ['snow', 'lightsnow', 'lightssnow', 'heavysnow']
SUNNY_VARIANTS = ['clearsky_day', 'clearsky_polartwilight', 'fair_day', 'fair_polartwilight']

# Temperature-based clothing rules (temp_max, icons_dict)
TEMP_CLOTHING_RULES = [
    (-5,    {'tops': ['sweater-thick'],     'bottoms': ['jeans', 'wool-pants'], 'coats': ['coat-fur'],  'accessories': ['mitten', 'hat', 'scarf']}),
    (0,     {'tops': ['sweater-thick'],     'bottoms': ['jeans'],               'coats': ['coat'],      'accessories': ['mitten', 'hat', 'scarf']}),
    (5,     {'tops': ['sweater-thick'],     'bottoms': ['jeans'],               'coats': ['coat'],      'accessories': ['mitten', 'hat']}),
    (10,    {'tops': ['sweater'],           'bottoms': ['jeans'],               'coats': ['coat']}),
    (15,    {'tops': ['sweater'],           'bottoms': ['jeans'],               'coats': ['coat-thin']}),
    (20,    {'tops': ['sweater'],           'bottoms': ['jeans']}),
    (25,    {'tops': ['t-shirt'],           'bottoms': ['jeans']}),
    (100,   {'tops': ['t-shirt'],           'bottoms': ['shorts']})
]

ICON_CATEGORIES = {
    "Tops": [
        ("t-shirt", "T-Shirt"),
        ("sweater", "Sweater"),
        ("sweater-thick", "Thick Sweater"),
    ],
    "Bottoms": [
        ("shorts", "Shorts"),
        ("jeans", "Jeans"),
        ("wool-pants", "Wool Pants"),
    ],
    "Coats": [
        ("coat-thin", "Light Jacket"),
        ("coat", "Coat"),
        ("coat-fur", "Heavy Winter Coat (Fur)"),
    ],
    "Accessories": [
        ("mitten", "Mittens"),
        ("scarf", "Scarf"),
        ("hat", "Hat"),
        ("sun-cream", "Sun Cream"),
        ("sunglasses", "Sunglasses"),
    ],
    "Precipitation": [
        ("rain-boots", "Rain Boots"),
        ("rain-coat", "Rain Coat"),
        ("umbrella", "Umbrella (light rain)"),
        ("umbrella-with-rain-drops", "Umbrella (heavy rain)"),
        ("umbrella-cross", "No Umbrella (dangerous conditions)"),
        ("snowflake", "Snow"),
        ("snowman", "Heavy snow)"),
    ],
    "Wind": [
        ("wind-face", "Windy"),
        ("kite", "Strong Wind"),
    ],
    "Lightning": [
        ("lightning", "Lightning/Thunderstorm"),
    ],
}