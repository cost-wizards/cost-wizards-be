from fastapi import FastAPI

import alembic.config
from cost_wiz.core.account.views import router as account_router
from cost_wiz.core.instances.views import router as instance_router
from cost_wiz.core.llm.views import router as llm_router

app = FastAPI()

app.include_router(account_router)
app.include_router(instance_router)
app.include_router(llm_router)


# @app.on_event("startup")
def run_migration():
    print("asdf")
    alembicArgs = [
        "--config",
        "alembic.ini",
        "upgrade",
        "head",
    ]
    alembic.config.main(argv=alembicArgs)
