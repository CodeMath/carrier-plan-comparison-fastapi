from fastapi.testclient import TestClient
from main import app
from router.combination import router

client = TestClient(app)
prefix = router.prefix


def test_select_carrier_single():
    response = client.post(
        prefix + "/kt", json={"mobile_line": ["basic"], "internet_line": "slim"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "base_line": {
            "price": 80000,
            "title": "베이직",
            "carrier": "5G",
            "contract_discount": 0.25,
            "combination_rule": {
                "name": "싱글 결합",
                "carrier_line": 1,
                "is_flat_discount": False,
                "combination_discount": 0.25,
            },
        },
        "internet": {"internet": "슬림", "price": 20900, "speed": 100, "wifi": 0},
        "sum_payment": 60900,
    }


def test_select_carrier_single_404():
    response = client.post(
        prefix + "/kt", json={"mobile_line": ["basic"], "internet_line": "slim1"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_select_carriers_family():
    response = client.post(
        prefix + "/kt",
        json={"mobile_line": ["basic", "special"], "internet_line": "slim"},
    )

    assert response.status_code == 200

    assert response.json() == {
        "base_line": {
            "price": 80000,
            "title": "베이직",
            "carrier": "5G",
            "contract_discount": 0.25,
            "combination_rule": {
                "name": "프리미엄 가족 결합 베이스 회선",
                "carrier_line": -1,
                "is_flat_discount": True,
                "combination_discount": 11000,
            },
        },
        "other_line": [
            {
                "price": 100000,
                "title": "스페셜",
                "carrier": "5G",
                "contract_discount": 0.25,
                "combination_rule": {
                    "name": "프리미엄 가족 결합 추가 회선",
                    "carrier_line": -1,
                    "is_flat_discount": False,
                    "combination_discount": 0.25,
                },
            }
        ],
        "internet": {"internet": "슬림", "price": 20900, "speed": 100, "wifi": 0},
        "sum_payment": 119900,
    }


def test_select_carriers_family_404():
    response = client.post(
        prefix + "/kt", json={"mobile_line": ["basic"], "internet_line": "slimless"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_between_carrieres_family_sums():
    response = client.post(
        prefix + "/kt/between",
        json={"mobile_line": ["basic", "special"], "internet_line": "slim"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "family_pay": 119900,
        "sum_pay": 127300,
        "family_plan": {
            "base_line": {
                "price": 80000,
                "title": "베이직",
                "url": None,
                "carrier": "5G",
                "contract_discount": 0.25,
                "combination_rule": {
                    "name": "프리미엄 가족 결합 베이스 회선",
                    "carrier_line": -1,
                    "is_flat_discount": True,
                    "combination_discount": 11000,
                },
            },
            "other_line": [
                {
                    "price": 100000,
                    "title": "스페셜",
                    "url": None,
                    "carrier": "5G",
                    "contract_discount": 0.25,
                    "combination_rule": {
                        "name": "프리미엄 가족 결합 추가 회선",
                        "carrier_line": -1,
                        "is_flat_discount": False,
                        "combination_discount": 0.25,
                    },
                }
            ],
            "internet": {"internet": "슬림", "price": 20900, "speed": 100, "wifi": 0},
            "sum_payment": 119900,
        },
        "sum_plan": {
            "mobile_plan_list": [
                {
                    "price": 80000,
                    "title": "베이직",
                    "url": None,
                    "carrier": "5G",
                    "contract_discount": 0.25,
                    "combination_rule": {
                        "name": "총액 가족 결합 회선",
                        "carrier_line": -1,
                        "is_flat_discount": True,
                        "combination_discount": 0,
                    },
                },
                {
                    "price": 100000,
                    "title": "스페셜",
                    "url": None,
                    "carrier": "5G",
                    "contract_discount": 0.25,
                    "combination_rule": {
                        "name": "총액 가족 결합 회선",
                        "carrier_line": -1,
                        "is_flat_discount": True,
                        "combination_discount": 0,
                    },
                },
            ],
            "mobile_discount": 23100,
            "internet": {"internet": "슬림", "price": 20900, "speed": 100, "wifi": 0},
            "internet_discount": 5500,
        },
    }
