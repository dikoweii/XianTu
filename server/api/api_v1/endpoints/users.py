from fastapi import APIRouter, Depends, HTTPException
from typing import List
from server.schemas import schema
from server.crud import crud_user
from server.api.api_v1 import deps
from server.models import AdminAccount

router = APIRouter()

@router.get('/by-username/{username}', response_model=schema.User, tags=["用户"])
async def get_user_by_username(username: str):
    """
    根据道号（用户名）查询用户信息。
    """
    db_user = await crud_user.get_player_by_username(user_name=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="未找到此道号的拥有者")
    return {"id": db_user.id, "user_name": db_user.user_name}

@router.get('/', response_model=List[schema.PlayerAccount], tags=["用户管理"])
async def get_all_users(current_admin: AdminAccount = Depends(deps.get_current_admin)):
    """
    获取所有用户列表（管理员权限）
    """
    return await crud_user.get_all_players()

@router.get('/{user_id}', response_model=schema.PlayerAccount, tags=["用户管理"])
async def get_user(user_id: int, current_admin: AdminAccount = Depends(deps.get_current_admin)):
    """
    根据ID获取用户信息（管理员权限）
    """
    user = await crud_user.get_player_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@router.put('/{user_id}', response_model=schema.PlayerAccount, tags=["用户管理"])
async def update_user(
    user_id: int, 
    user_data: schema.PlayerAccountUpdate,
    current_admin: AdminAccount = Depends(deps.get_super_admin_user)
):
    """
    更新用户信息（超级管理员权限）
    """
    updated_user = await crud_user.update_player(user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="用户不存在或更新失败")
    return updated_user

@router.delete('/{user_id}', response_model=dict, tags=["用户管理"])
async def delete_user(
    user_id: int,
    current_admin: AdminAccount = Depends(deps.get_super_admin_user)
):
    """
    删除用户（超级管理员权限）
    """
    success = await crud_user.delete_player(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在或删除失败")
    return {"message": "用户删除成功"}