from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from cost_wiz.core.account.schema import (AccountCreateRequestSchema,
                                          AccountResponseSchema)
from cost_wiz.core.account.services import AccountService
from cost_wiz.deps import get_db

router = APIRouter()


@router.get("/accounts", response_model=list[AccountResponseSchema])
def get_accounts(service: AccountService = Depends(), db: Session = Depends(get_db)):
    return service.get_accounts(db)


@router.get("/accounts/{id}", response_model=AccountResponseSchema)
def get_account(id: int, service: AccountService = Depends(), db: Session = Depends(get_db)):
    return service.get_account(db, id)


@router.post("/accounts")
def create_account(
    account: AccountCreateRequestSchema, service: AccountService = Depends(), db: Session = Depends(get_db)
):
    return service.create_account(db, account)
