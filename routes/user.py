from fastapi import APIRouter
from config.supabase_client import supabase
from schemas.user import UserCreate, UserUpdate, User
import os
from fastapi import HTTPException
from dotenv import load_dotenv

from cryptography.fernet import Fernet

load_dotenv()
key = os.getenv("FERNET_KEY")
f = Fernet(key)


user  = APIRouter()


@user.get("/users", response_model=list[User], tags=["users"])
async def get_users():
    results = supabase.table("users").select("*").execute()
    return results.data

@user.post("/users", response_model=User, tags=["users"])
async def get_users(user: UserCreate):
    data = user.model_dump()
    data["password"] = f.encrypt(user.password.encode()).decode()
    results = supabase.table("users").insert(data).execute()
    return results.data

@user.get("/users/{user_id}", tags=["users"])
async def get_user(user_id: str):
    results = supabase.table("users").select("*").eq("id", user_id).execute()
    
    if not results.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"success": True, "user": results.data[0]}

@user.delete("/users/{user_id}", tags=["users"])
async def delete_user(user_id: str):
    results = supabase.table("users").delete().eq("id", user_id).execute()
    if not results.data:
        raise HTTPException(status_code=404, detail="User not found")


@user.put("/users/{user_id}", tags=["users"])
async def update_user(user_id: str, user_data: UserUpdate):
    try:
        data = user_data.model_dump()

        if "password" in data and data["password"]:
            data["password"] = f.encrypt(data["password"].encode()).decode()

        # Verificamos si el usuario existe antes de actualizar
        existing = supabase.table("users").select("id").eq("id", user_id).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Hacemos la actualización
        results = supabase.table("users").update(data).eq("id", user_id).execute()

        return {
            "success": True,
            "message": "Usuario actualizado correctamente",
            "user": results.data[0] if results.data else {}
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))