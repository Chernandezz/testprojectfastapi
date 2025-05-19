from fastapi import APIRouter
from config.supabase_client import supabase
from schemas.user import UserCreate
import os
from fastapi import HTTPException
from dotenv import load_dotenv

from cryptography.fernet import Fernet

load_dotenv()
key = os.getenv("FERNET_KEY")
f = Fernet(key)


user  = APIRouter()


@user.get("/users")
async def get_users():
    results = supabase.table("users").select("*").execute()
    return results.data

@user.post("/users")
async def get_users(user: UserCreate):
    data = user.model_dump()
    data["password"] = f.encrypt(user.password.encode()).decode()
    results = supabase.table("users").insert(data).execute()
    return results.data

@user.get("/users/{user_id}")
async def get_user(user_id: str):
    results = supabase.table("users").select("*").eq("id", user_id).execute()
    
    if not results.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"success": True, "user": results.data[0]}

@user.delete("/users/{user_id}")
async def delete_user(user_id: str):
    results = supabase.table("users").delete().eq("id", user_id).execute()
    if not results.data:
        raise HTTPException(status_code=404, detail="User not found")
