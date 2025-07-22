from dotenv import load_dotenv
import os
import requests

load_dotenv()

def test_wallet_request() -> None:
    test_wallet_address = os.getenv("TEST_WALLET_ADDRESS")
    response = requests.post("http://tron-service:8000/wallet", json={"address": test_wallet_address})
    assert response.status_code == 200
    assert "address" in response.json()

    response = requests.get("http://tron-service:8000/wallets")
    assert response.status_code == 200
    wallets = response.json()
    assert any(wallet["address"] == test_wallet_address for wallet in wallets)
