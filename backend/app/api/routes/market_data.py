from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.providers.mock_provider import MockProvider
from app.repositories import market_data
from app.services.indicators import IndicatorService

router = APIRouter(tags=["market-data"])
provider = MockProvider()
indicator_service = IndicatorService()


@router.get("/provider/status")
def provider_status() -> dict:
    return provider.get_status().model_dump()


@router.get("/symbols")
def list_symbols(db: Session = Depends(get_db)) -> list[dict]:
    symbols = market_data.list_symbols(db)
    return [symbol.model_dump() for symbol in symbols]


@router.get("/symbols/{symbol}/bars")
def get_daily_bars(symbol: str, db: Session = Depends(get_db)) -> list[dict]:
    bars = market_data.get_daily_bars(db, symbol.upper())
    if not bars:
        raise HTTPException(status_code=404, detail=f"No persisted bars found for {symbol.upper()}")
    return [bar.model_dump() for bar in bars]


@router.get("/symbols/{symbol}/indicators")
def get_indicator_snapshot(symbol: str, db: Session = Depends(get_db)) -> dict:
    bars = market_data.get_daily_bars(db, symbol.upper())
    if not bars:
        raise HTTPException(status_code=404, detail=f"No persisted bars found for {symbol.upper()}")
    return indicator_service.build_snapshot(symbol, bars).model_dump()


@router.get("/profiles/{symbol}")
def get_company_profile(symbol: str, db: Session = Depends(get_db)) -> dict:
    profile = market_data.get_company_profile(db, symbol.upper())
    if profile is None:
        raise HTTPException(status_code=404, detail=f"No persisted profile found for {symbol.upper()}")
    return profile.model_dump()


@router.get("/earnings/{symbol}")
def get_earnings(symbol: str, db: Session = Depends(get_db)) -> dict:
    event = market_data.get_earnings_event(db, symbol.upper())
    if event is None:
        raise HTTPException(status_code=404, detail=f"No persisted earnings event found for {symbol.upper()}")
    return event.model_dump()
