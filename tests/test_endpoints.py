import requests
from dotenv import load_dotenv
import os
load_dotenv()

def test_post_wallet() -> None:
    test_wallet_address = os.getenv("TEST_WALLET_ADDRESS")
    response = requests.post("http://tron-service:8000/wallet", json={"address": test_wallet_address})
    assert response.status_code == 200
    assert "address" in response.json()

def test_get_wallets() -> None:
    response = requests.get("http://tron-service:8000/wallets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
