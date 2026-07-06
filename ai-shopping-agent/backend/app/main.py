from fastapi import FastAPI
#from app.database.base import Base
#from app.database.connection import engine
#from app.api.auth import router as auth_router
#from app.models.user import User
#from app.api.product import router as product_router
from app.core.config import settings
from app.core.config import settings
#from app.models.product import Product
#from app.models.price_history import PriceHistory
from app.api.agent import router as agent_router


print(settings.GOOGLE_API_KEY)

print("GOOGLE_API_KEY =", settings.GOOGLE_API_KEY)

#Base.metadata.create_all(bind=engine)
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1
    }
)

app.include_router(agent_router)
#app.include_router(auth_router)
#app.include_router(product_router)
#@app.get("/")
#def home():

 #   return {
  #      "project": settings.PROJECT_NAME,
   #     "version": settings.VERSION,
    #    "status": "running",
    #}
