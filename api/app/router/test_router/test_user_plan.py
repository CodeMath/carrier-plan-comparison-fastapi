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
                "is_flat_discount": false,
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
