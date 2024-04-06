from fastapi import FastAPI
from loguru import logger

import alembic.config
from cost_wiz.core.account.views import router as account_router

app = FastAPI()

app.include_router(account_router)


@app.on_event("startup")
def run_migration():
    alembicArgs = [
        "--config",
        "alembic.ini",
        "upgrade",
        "head",
    ]
    alembic.config.main(argv=alembicArgs)
