from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from cost_wiz.config.settings import env
from cost_wiz.core.account.schema import AccountCreateRequestSchema
from cost_wiz.db import Account, Instance, Recommendation
from cost_wiz.utils.utils import billing_data


class AccountService:

    def get_accounts(self, db: Session):

        connected_accounts = db.query(Account).count()

        optimization_runs = db.query(Recommendation.id).count()

        total_cost_for_ec2 = billing_data(
            env.aws_access_key_id, env.aws_secret_access_key, env.aws_session_token, env.aws_region_name
        )

        data = db.query(Account, func.count(Instance.id)).group_by(Account.id).all()
        if data:

            accounts, ec2_count = data[0]

            return {
                "connected_accounts": connected_accounts,
                "optimization_runs": optimization_runs,
                "data": accounts,
                "ec2_count": ec2_count,
                "total_ec2_cost": total_cost_for_ec2,
            }

        return {
            "connected_accounts": connected_accounts,
            "optimization_runs": optimization_runs,
            "data": [],
            "ec2_count": 0,
            "total_ec2_cost": total_cost_for_ec2,
        }

    def get_account(self, db: Session, id: int):
        account = db.query(Account).filter(Account.id == id).one_or_none()

        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        optimization_runs = db.query(Recommendation.id).filter(Recommendation.account_id == id).count()
        total_cost_for_ec2 = billing_data(
            env.aws_access_key_id, env.aws_secret_access_key, env.aws_session_token, env.aws_region_name
        )

        data = db.query(Account, func.count(Instance.id)).filter(Instance.account_id == id).group_by(Account.id).all()

        if data:

            accounts, ec2_count = data[0]

            return {
                "optimization_runs": optimization_runs,
                "data": accounts,
                "ec2_count": ec2_count,
                "total_ec2_cost": total_cost_for_ec2,
            }

        return {
            "optimization_runs": optimization_runs,
            "data": None,
            "ec2_count": 0,
            "total_ec2_cost": total_cost_for_ec2,
        }

    def create_account(self, db: Session, account: AccountCreateRequestSchema):

        _account = Account(
            name=account.name,
            access_key=account.access_key,
            secret_key=account.secret_key,
            region=account.region,
            session_key=account.session_key,
            has_account_setup=False,
        )

        db.add(_account)
        db.flush()
