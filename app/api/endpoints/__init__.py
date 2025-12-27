"""API router for Pokémon-related endpoints."""

from fastapi import APIRouter

from .cards_api import router as cards_router

endpoints_router = APIRouter()

endpoints_router.include_router(cards_router)
