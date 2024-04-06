from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from cost_wiz.core.account.schema import AccountCreateRequestSchema
from cost_wiz.db import Account, Instance, Recommendation


class AccountService:

    def get_accounts(self, db: Session):

        connected_accounts = db.query(Account).count()

        optimization_runs = db.query(Recommendation.id).count()

        data = db.query(Account, func.count(Instance.id)).group_by(Account.id).all()

        print(data)

        # return {
        #     "connected_accounts": connected_accounts,
        #     "optimization_runs": optimization_runs,
        #     "data":        }

    def get_account(self, db: Session, id: int) -> Account:
        account = db.query(Account).filter(Account.id == id).one_or_none()

        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        return account

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
