from fastapi import APIRouter, Depends

from cost_wiz.core.account.schema import (AccountCreateRequestSchema,
                                          AccountResponseSchema)
from cost_wiz.core.account.services import AccountService

router = APIRouter()


@router.get("/accounts", response_model=list[AccountResponseSchema])
def get_accounts(service: AccountService = Depends()):
    return service.get_accounts()


@router.get("/accounts/{id}", response_model=AccountResponseSchema)
def get_account(id: int, service: AccountService = Depends()):
    return service.get_account(id)


@router.post("/accounts")
def create_account(account: AccountCreateRequestSchema, service: AccountService = Depends()):
    return service.create_account(account)
