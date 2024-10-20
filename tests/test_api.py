import pytest
from fastapi.testclient import TestClient
from ai_assistant.api import app, get_agent

client = TestClient(app)

def get_mocked_agent():
    class MockedAgent:
        def query(self, prompt):
            return "Mocked agent response"
    return MockedAgent()

app.dependency_overrides[get_agent] = get_mocked_agent

@pytest.mark.parametrize("path",["places","hotels","activities"])
@pytest.mark.parametrize("city",["La Paz","Santa Cruz","Cochabamba"])
@pytest.mark.parametrize("notes",[[], ["Answer in germany"], ["I like to eat spicy food","I like to visit museums"]])
def test_get_recommendations(path, city, notes):
    response = client.get(f"/recommendations/{path}", params={"city": city, "notes": notes})

    assert response.status_code == 200

    body = response.json() 
    assert body.get("status") == "OK"
    assert body.get("message") == "Recommendations obtained successfully"
    assert body.get("agent_response") == "Mocked agent response"