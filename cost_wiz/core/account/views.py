from fastapi import APIRouter, Depends

from cost_wiz.core.account.services import AccountService

router = APIRouter(tags=["iot"])


@router.get("/accounts")
def get_accounts(service: AccountService = Depends()):
    return service.get_accounts()
