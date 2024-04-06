from fastapi import HTTPException
from sqlalchemy.orm import Session

from cost_wiz.core.account.services import AccountService
from cost_wiz.db import Account, Instance
from cost_wiz.utils.utils import get_instances


class InstanceService:

    def get_available_instances(self, session: Session, account_service: AccountService, *, account_id: int):

        _account: Account = account_service.get_account(session, id=account_id)

        params = {
            "access_key": _account.access_key,
            "secret_key": _account.secret_key,
            "session_token": _account.session_key,
            "region": _account.region,
        }

        ec2_instances: list[dict] = get_instances(**params)

        return ec2_instances

    def get_instances(self, session: Session, account_service: AccountService, *, account_id: int):
        _account = account_service.get_account(session, id=account_id)

        _instances = session.query(Instance).filter(Instance.account_id == _account.id).all()

        return _instances

    def get_instance(self, session: Session, account_service: AccountService, *, account_id: int, instance_id: int):
        account_service.get_account(session, id=account_id)

        _instance = (
            session.query(Instance).filter(Instance.id == instance_id, Instance.account_id == account_id).one_or_none()
        )

        if not _instance:
            raise HTTPException(status_code=404, detail="Instance not found")

        return _instance
