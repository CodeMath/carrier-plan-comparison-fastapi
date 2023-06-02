from fastapi.testclient import TestClient
from app.main import app
from ..plan_list import router

client = TestClient(app)
prefix = router.prefix


def test_get_list_mobile():
    response = client.get(prefix + "/mobile", params={"price": 115000, "tp": "5g"})

    assert response.status_code == 200
    assert response.json() == [
        {
            "price": 130000,
            "title": "초이스 프리미엄",
            "carrier": "5G",
        }
    ]


def test_get_list_mobile_lte():
    response = client.get(prefix + "/mobile", params={"price": 30000, "tp": "lte"})

    assert response.status_code == 200
    assert response.json() == [
        {
            "price": 89000,
            "title": "데이터 온 프리미엄",
            "carrier": "LTE",
        },
        {
            "price": 89000,
            "title": "데이터 온 프리미엄",
            "carrier": "LTE",
        },
    ]


def test_get_list_mobile_404():
    response = client.get(prefix + "/kt", params={"price": 10, "tp": "none"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_get_list_internet():
    response = client.get(prefix + "/mobile", params={"price": 60000, "wifi": 2})

    assert response.status_code == 200
    assert response.json() == [
        {"internet": "슈퍼프리미엄", "price": 82500, "speed": 10000, "wifi": 2}
    ]


def test_get_list_internet_404():
    response = client.get(prefix + "/mobile", params={"price": 90000, "wifi": 2})

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
