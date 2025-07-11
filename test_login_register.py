from fastapi.testclient import TestClient
from main import app  # FastAPI 앱이 main.py

client = TestClient(app)

def test_register():
    # 회원가입 테스트 데이터
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    response = client.post("/auth/register", json=data)
    # if response.status_code == 400:
    #     print("회원가입 에러(400):", response.json())
    #     assert False, f"회원가입 실패: {response.json()}"
    assert response.status_code == 200 or response.status_code == 201
    print("회원가입 결과:", response.json())

def test_login():
    # 로그인 테스트 데이터
    data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post("/auth/login", data=data)  # 보통 로그인은 form-data로 받음
    assert response.status_code == 200
    print("로그인 결과:", response.json())

if __name__ == "__main__":
    # test_register()
    test_login()
