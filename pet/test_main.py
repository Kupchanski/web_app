from fastapi.testclient import TestClient
import pet.main as main


client = TestClient(main.app)


def test_home_route():
    response = client.get("/")
    assert response.status_code == 200


def test_predict_route():
    file_name = 'pet/static/images/cat_image.jpeg'
    response = client.post(
        "/predict",
        files = {'file': ("cat_image", open(file_name, 'rb'), "image/jpeg")},
        )

    assert response.status_code == 200
    