from fastapi import Depends
from sqlalchemy.orm import Session

from cost_wiz.db import Account
from cost_wiz.deps import get_db


class AccountService:

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db: Session = db

    def get_accounts(self):
        return self.db.query(Account).all()
