from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from cost_wiz.core.account.schema import AccountCreateRequestSchema
from cost_wiz.db import Account
from cost_wiz.deps import get_db


class AccountService:

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db: Session = db

    def get_accounts(self):
        return self.db.query(Account).all()

    def get_account(self, id: int):
        account = self.db.query(Account).filter(Account.id == id).one_or_none()

        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        return account

    def create_account(self, account: AccountCreateRequestSchema):

        _account = Account(
            name=account.name,
            access_key=account.access_key,
            secret_key=account.secret_key,
            region=account.region,
            session_key=account.session_key,
        )

        self.db.add(_account)
        self.db.flush()
