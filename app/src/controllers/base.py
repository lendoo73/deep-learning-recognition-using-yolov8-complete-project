from fastapi import APIRouter
from brain_tumor.controllers import brain_tumor_rest_controller

api_router = APIRouter()
api_router.include_router(brain_tumor_rest_controller.router)
