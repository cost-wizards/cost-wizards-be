from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import alembic.config
from cost_wiz.core.account.views import router as account_router
from cost_wiz.core.instances.views import router as instance_router
from cost_wiz.core.llm.views import router as llm_router
from cost_wiz.core.stats.views import router as stat_router

app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(account_router)
app.include_router(instance_router)
app.include_router(llm_router)
app.include_router(stat_router)


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
