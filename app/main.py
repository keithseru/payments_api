from fastapi import FastAPI

from app.routes.customers import router as customers_router
#from app.routes.payments import router as payments_router
#from app.routes.refunds import router as refunds_router

app = FastAPI(
    title = "Payments API",
    description = "A fake payment server built with FastAPI",
    version = "1.0.0"
)

app.include_router(customers_router, prefix="/customers", tags=['Customers'])
#app.include_router(payments_router, prefix="/payments", tags=['Payments'])
#app.include_router(refunds_router, prefix="/refunds", tags=['Refunds'])



