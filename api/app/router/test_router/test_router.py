from fastapi.testclient import TestClient
from ....app.main import app
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
