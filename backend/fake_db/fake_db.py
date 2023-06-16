fake_plan = {
    "choice_premiem": {
        "price": 130000,
        "title": "초이스 프리미엄",
        "carrier": "5G",
        "url": "https://kt.com",
        "eng_title": "choice_premiem",
    },
    "choice_special": {
        "price": 110000,
        "title": "초이스 스페셜",
        "carrier": "5G",
        "eng_title": "choice_special",
        "url": "https://kt.com",
    },
    "choice_basic": {
        "price": 90000,
        "title": "초이스 베이직",
        "carrier": "5G",
        "eng_title": "choice_basic",
        "url": "https://kt.com",
    },
    "special": {
        "price": 100000,
        "title": "스페셜",
        "carrier": "5G",
        "eng_title": "special",
        "url": "https://kt.com",
    },
    "special_Y": {
        "price": 100000,
        "title": "스페셜Y",
        "carrier": "5G",
        "eng_title": "special_Y",
        "url": "https://kt.com",
    },
    "basic": {
        "price": 80000,
        "title": "베이직",
        "carrier": "5G",
        "eng_title": "basic",
        "url": "https://kt.com",
    },
    "basic_Y": {
        "price": 80000,
        "title": "베이직Y",
        "carrier": "5G",
        "eng_title": "basic_Y",
        "url": "https://kt.com",
    },
    "data_on_premiem": {
        "price": 89000,
        "title": "데이터 온 프리미엄",
        "carrier": "LTE",
        "eng_title": "data_on_premiem",
        "url": "https://kt.com",
    },
    "data_on_premiem_Y": {
        "price": 89000,
        "title": "데이터 온 프리미엄",
        "carrier": "LTE",
        "eng_title": "data_on_premiem_Y",
        "url": "https://kt.com",
    },
}


fake_combination_rule = {
    "single": {
        "name": "싱글 결합",
        "carrier_line": 1,
        "is_flat_discount": False,
        "combination_discount": 0.25,
    },
    "family_base": {
        "name": "프리미엄 가족 결합 베이스 회선",
        "carrier_line": -1,
        "is_flat_discount": True,
        "combination_discount": 11000,
    },
    "family_other": {
        "name": "프리미엄 가족 결합 추가 회선",
        "carrier_line": -1,
        "is_flat_discount": False,
        "combination_discount": 0.25,
    },
    "sums": {
        "name": "총액 가족 결합 회선",
        "carrier_line": -1,
        "is_flat_discount": True,
        "combination_discount": 0,
    },
}


fake_internet = {
    "slim": {"internet": "슬림", "price": 20900, "speed": 100, "wifi": 0},
    "slim_plus": {"internet": "슬림 플러스", "price": 30250, "speed": 200, "wifi": 0},
    "basic": {"internet": "베이직", "price": 31350, "speed": 500, "wifi": 0},
    "essense": {"internet": "에센스", "price": 36300, "speed": 1000, "wifi": 0},
    "slim_wifi": {"internet": "슬림 와이파이", "price": 22000, "speed": 100, "wifi": 1},
    "basic_wifi": {"internet": "베이직 와이파이", "price": 32450, "speed": 500, "wifi": 1},
    "essense_wifi": {"internet": "에센스 와이파이", "price": 36300, "speed": 1000, "wifi": 1},
    "premien_wifi": {"internet": "프리미엄 와이파이", "price": 41250, "speed": 2500, "wifi": 1},
    "basic_wifi_wide": {"internet": "베이직 와이드", "price": 34100, "speed": 500, "wifi": 1},
    "essense_wifi_wide": {
        "internet": "에센스 와이드",
        "price": 37950,
        "speed": 1000,
        "wifi": 1,
    },
    "premien_wifi_wide": {
        "internet": "프리미엄 와이드",
        "price": 42350,
        "speed": 2500,
        "wifi": 1,
    },
    "premien": {"internet": "프리미엄", "price": 41250, "speed": 2500, "wifi": 1},
    "premien_plus": {"internet": "프리미엄플러스", "price": 56650, "speed": 5000, "wifi": 2},
    "super_premien": {"internet": "슈퍼프리미엄", "price": 82500, "speed": 10000, "wifi": 2},
}


fake_sum_combination = {
    "22000": {
        "slim": {
            "mobile_sum_price": [0, 22000],
            "mobile_discount": 0,
            "internet_discount": 1650,
        },
        "none-slim": {
            "mobile_sum_price": [0, 22000],
            "mobile_discount": 0,
            "internet_discount": 2200,
        },
    },
    "64899": {
        "slim": {
            "mobile_sum_price": [22000, 64899],
            "mobile_discount": 5500,
            "internet_discount": 5500,
        },
        "none-slim": {
            "mobile_sum_price": [22000, 64899],
            "mobile_discount": 0,
            "internet_discount": 3300,
        },
    },
    "108899": {
        "slim": {
            "mobile_sum_price": [64900, 108899],
            "mobile_discount": 3300,
            "internet_discount": 5500,
        },
        "none-slim": {
            "mobile_sum_price": [64900, 108899],
            "mobile_discount": 5500,
            "internet_discount": 5500,
        },
    },
    "141899": {
        "slim": {
            "mobile_sum_price": [108900, 141899],
            "mobile_discount": 14300,
            "internet_discount": 5500,
        },
        "none-slim": {
            "mobile_sum_price": [108900, 141899],
            "mobile_discount": 16610,
            "internet_discount": 5500,
        },
    },
    "174899": {
        "slim": {
            "mobile_sum_price": [141900, 174899],
            "mobile_discount": 18700,
            "internet_discount": 5500,
        },
        "none-slim": {
            "mobile_sum_price": [141900, 174899],
            "mobile_discount": 22110,
            "internet_discount": 5500,
        },
    },
    "999999": {
        "slim": {
            "mobile_sum_price": [174900, 999999],
            "mobile_discount": 23100,
            "internet_discount": 5500,
        },
        "none-slim": {
            "mobile_sum_price": [174900, 999999],
            "mobile_discount": 27610,
            "internet_discount": 5500,
        },
    },
}
