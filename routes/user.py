from fastapi import APIRouter
from config.supabase_client import supabase

user  = APIRouter()

@user.get("/users")
async def get_users():
    results = supabase.table("users").select("*").execute()
    return results.data