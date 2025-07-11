from fastapi.testclient import TestClient
from main import app  # 실제 FastAPI app 객체 import

client = TestClient(app)

def test_invoke_agent():
    # 테스트용 요청 데이터
    payload = {
        "session_id": "test-session-001",
        "prompt": "Is there a game titled 조선메타실록 in Steam or google.",
    }
    # POST 요청 보내기
    response = client.post("/api/v1/agent/invoke", json=payload)
    # 결과 출력
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

# 함수 직접 실행
if __name__ == "__main__":
    test_invoke_agent()