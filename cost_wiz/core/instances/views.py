from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from cost_wiz.core.account.services import AccountService
from cost_wiz.core.instances.schema import Ec2InstanceResponseSchema
from cost_wiz.core.instances.services import InstanceService
from cost_wiz.deps import get_db

router = APIRouter()


@router.get("/account/{id}/available-instances", response_model=list[Ec2InstanceResponseSchema])
def get_available_instances(
    id: int,
    session: Session = Depends(get_db),
    service: InstanceService = Depends(),
    account_service: AccountService = Depends(),
):
    return service.get_available_instances(session, account_service, account_id=id)


@router.get("/account/{id}/instances")
def get_instances(
    id: int,
    session: Session = Depends(get_db),
    account_service: AccountService = Depends(),
    service: InstanceService = Depends(),
):
    return service.get_instances(session, account_service, account_id=id)


@router.post("/account/{account_id}/instance/{id}")
def get_instance(
    account_id: int,
    id: int,
    service: InstanceService = Depends(),
    account_service: AccountService = Depends(),
    session: Session = Depends(get_db),
):
    return service.get_instance(session, account_service, account_id=account_id, instance_id=id)
