from fastapi import HTTPException
from sqlalchemy.orm import Session

from cost_wiz.core.account.schema import AccountCreateRequestSchema
from cost_wiz.db import Account


class AccountService:

    def get_accounts(self, db: Session):
        return db.query(Account).all()

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
