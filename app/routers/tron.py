from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Union
from tronpy import Tron
from sqlalchemy.orm import Session
from app.database import get_db, WalletRequest
from tronpy.providers import HTTPProvider
from dotenv import load_dotenv
import os

load_dotenv()
router = APIRouter()
tron_client = Tron(HTTPProvider(api_key=os.getenv("TRONGRID_API_KEY")))
class WalletRequestModel(BaseModel):
    address: str

@router.post("/wallet")
def get_wallet_info(request: WalletRequestModel, db: Session = Depends(get_db)):
    try:
        wallet = tron_client.get_account(request.address)
        bandwidth = tron_client.get_bandwidth(request.address) or "Not found"
        energy = tron_client.get_energy(request.address) or "Not found"
        trx_balance = wallet['balance'] / 1_000_000 or -1
        db_request = WalletRequest(address=request.address)
        db.add(db_request)
        db.commit()

        return {
            "address": request.address,
            "bandwidth": bandwidth,
            "energy": energy,
            "trx_balance": trx_balance
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
DEFAULT_WALLET_REQUEST_LIMIT = int(os.getenv("DEFAULT_WALLET_REQUEST_LIMIT", 10))
DEFAULT_WALLET_REQUEST_SKIP = int(os.getenv("DEFAULT_WALLET_REQUEST_SKIP", 0))

@router.get("/wallets")
def get_wallet_requests(skip: int = DEFAULT_WALLET_REQUEST_SKIP, limit: int = DEFAULT_WALLET_REQUEST_LIMIT, db: Session = Depends(get_db)):
    wallets = db.query(WalletRequest).offset(skip).limit(limit).all()
    return wallets
