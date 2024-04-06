from fastapi import HTTPException
from sqlalchemy import Float, Integer, cast
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from cost_wiz.config.settings import env
from cost_wiz.core.account.schema import AccountCreateRequestSchema
from cost_wiz.db import Account, Instance, InstanceStat, Recommendation
from cost_wiz.utils.utils import billing_data, get_instances


class AccountService:

    def get_accounts(self, db: Session):
        query = (
            db.query(
                Account.id.label("account_id"),
                Account.name.label("account_name"),
                Account.access_key,
                Account.secret_key,
                Account.region,
                Account.session_key,
                func.count(Instance.id).label("instance_count"),
            )
            .outerjoin(Instance, Account.id == Instance.account_id)
            .group_by(Account.id, Account.name)
        )

        parsed_data = []

        result = db.query(func.sum(func.round(cast(Recommendation.sug_2_diff_cost_per_hour, Float)))).scalar()
        recommendation_count = db.query(Recommendation.id).count()

        for data in query.all():
            access_key = data.access_key
            secret_key = data.secret_key
            region = data.region
            session_key = data.session_key

            total_cost_for_ec2 = 0

            # try:
            #     total_cost_for_ec2 = billing_data(access_key, secret_key, session_key, region)
            # except:
            #     pass
            parsed_data.append(
                {
                    "total_savings": result,
                    "recommendation_count": recommendation_count,
                    "id": data.account_id,
                    "name": data.account_name,
                    "instance_count": data.instance_count,
                    "total_cost_for_ec2": total_cost_for_ec2,
                }
            )

        return parsed_data

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

        return {"data": _account.id}
