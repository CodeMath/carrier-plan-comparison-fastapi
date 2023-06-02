from fastapi.testclient import TestClient
from app.main import app
from ..combination import router

client = TestClient(app)
prefix = router.prefix


def test_select_carrier_single():
    response = client.get(prefix + "/kt", params={"q": "basic", "ith": "slim"})

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
    response = client.get(prefix + "/kt", params={"q": "basic", "ith": "no internet"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_select_carriers_family():
    response = client.get(
        prefix + "/kt", params={"q": ["basic", "special"], "ith": "slim"}
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
    response = client.get(
        prefix + "/kt", params={"q": ["basic", "special"], "ith": "slimsssss"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
