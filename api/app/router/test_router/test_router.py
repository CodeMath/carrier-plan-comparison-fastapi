from fastapi.testclient import TestClient
from app.main import app
from ..user_plan import router

client = TestClient(app)
prefix = router.prefix


def test_get_list():
    response = client.get(prefix + "/kt", params={"price": 115000, "tp": "5g"})

    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "choice_premiem",
            "price": 130000,
            "title": "초이스 프리미엄",
            "carrier": "5G",
        }
    ]


def test_get_list_lte():
    response = client.get(prefix + "/kt", params={"price": 30000, "tp": "lte"})

    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "data_on_premiem",
            "price": 89000,
            "title": "데이터 온 프리미엄",
            "carrier": "LTE",
        },
        {
            "name": "data_on_premiem_Y",
            "price": 89000,
            "title": "데이터 온 프리미엄",
            "carrier": "LTE",
        },
    ]


def test_select_carrier_single():
    response = client.get(prefix + "/kt/combination", params={"q": "choice_special"})

    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "choice_special",
            "price": 110000,
            "title": "싱글 결합",
            "carrier": "5G",
            "contract_discount_25%": 27500,
            "single_contract_discount_25%": 27500,
            "discount_sum": 55000,
            "internet": {"plan": "인터넷 베이직 3년 약정", "mbps": 500, "price": 31350},
            "payment": 86350,
        }
    ]
