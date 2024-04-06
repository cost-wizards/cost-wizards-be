from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from cost_wiz.core.instances.services import InstanceService
from cost_wiz.core.llm.services import LLMService
from cost_wiz.deps import get_db

router = APIRouter()


@router.get("/account/{account_id}/instance/{id}/predict")
def predict_cost(
    id: int,
    account_id: int,
    session: Session = Depends(get_db),
    service: LLMService = Depends(),
    instance_service: InstanceService = Depends(),
):
    return service.predict_cost(session, instance_service, instance_id=id, account_id=account_id)
