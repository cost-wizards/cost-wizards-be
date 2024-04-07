from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from cost_wiz.core.account.services import AccountService
from cost_wiz.core.instances.schema import InstanceRequestSchema
from cost_wiz.db import Account, Instance
from cost_wiz.utils.utils import get_instances


class InstanceService:

    def get_available_instances(self, session: Session, *, account_id: int):

        _account = session.query(Account).filter(Account.id == account_id).first()

        params = {
            "access_key": _account.access_key,
            "secret_key": _account.secret_key,
            "session_token": _account.session_key,
            "region": _account.region,
        }

        ec2_instances: list[dict] = get_instances(**params)

        for i, ec2 in enumerate(ec2_instances):
            obj = Instance(
                name=f"EC2-{i}",
                instance_id=ec2["instance_id"],
                instance_type=ec2["instance_type"],
                vcpu=ec2["vcpu"],
                instance_memory=ec2["instance_memory"],
                on_demand_price=ec2["on_demand_price"],
                network_performance=ec2["network_performance"],
                account_id=account_id,
            )
            session.add(obj)

    def get_instances(self, session: Session, account_service: AccountService, *, account_id: int):

        _instances = session.query(Instance).filter(Instance.account_id == account_id).all()

        return _instances

    def get_instance(self, session: Session, *, instance_id: int):

        _instance = session.query(Instance).filter(Instance.id == instance_id).one_or_none()

        if not _instance:
            raise HTTPException(status_code=404, detail="Instance not found")

        return _instance

    def select_instances(
        self,
        session: Session,
        account_service: AccountService,
        *,
        payload: List[InstanceRequestSchema],
        account_id: int,
    ):

        account_service.get_account(session, id=account_id)

        _instances = []

        for data in payload:
            _instances.append(
                Instance(
                    instance_id=data.instance_id,
                    instance_type=data.instance_type,
                    vcpu=data.vcpu,
                    instance_memory=data.instance_memory,
                    network_performance=data.network_performance,
                    on_demand_price=data.on_demand_price,
                    status=data.status,
                    account_id=account_id,
                )
            )

        session.add_all(_instances)
