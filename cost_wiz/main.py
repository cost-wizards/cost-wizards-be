from fastapi import FastAPI

from cost_wiz.core.account.views import router as account_router

app = FastAPI()

app.include_router(account_router)
