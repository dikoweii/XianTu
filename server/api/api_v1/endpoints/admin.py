from fastapi import APIRouter, HTTPException, Depends
from typing import List
from server.models import AdminAccount
from server.schemas import schema
from server.crud import crud_user
from server.api.api_v1 import deps

router = APIRouter(prefix="/admin", tags=["后台管理"])

# 注意：兑换码管理功能已移至 redemption.py 以避免重复路由
# 用户权限管理通过 AdminAccount 的 `role` 字段进行控制

@router.get("/accounts", response_model=List[schema.AdminAccount])
async def get_all_admin_accounts(
    current_admin: AdminAccount = Depends(deps.get_admin_or_super_admin)
):
    """获取所有管理员账号"""
    admins = await AdminAccount.all()
    return admins

@router.get("/accounts/{admin_id}", response_model=schema.AdminAccount)
async def get_admin_account(
    admin_id: int,
    current_admin: AdminAccount = Depends(deps.get_admin_or_super_admin)
):
    """获取指定管理员账号"""
    admin = await AdminAccount.get_or_none(id=admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="仙官不存在")
    return admin

@router.put("/accounts/{admin_id}", response_model=schema.AdminAccount)
async def update_admin_account(
    admin_id: int,
    updates: dict,
    current_admin: AdminAccount = Depends(deps.get_admin_or_super_admin)
):
    """更新管理员账号"""
    admin = await AdminAccount.get_or_none(id=admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="仙官不存在")
    
    # 如果是修改自己的账号，需要验证当前密码
    if current_admin.id == admin_id:
        if "current_password" in updates:
            from server.core import security
            if not security.verify_password(updates["current_password"], admin.password):
                raise HTTPException(status_code=400, detail="当前密码不正确")
            del updates["current_password"]  # 移除current_password，不保存到数据库
        elif "password" in updates or "user_name" in updates:
            # 如果要修改密码或用户名但没有提供当前密码，拒绝请求
            raise HTTPException(status_code=400, detail="修改密码或用户名时必须提供当前密码")
    
    # 检查新用户名是否已被使用
    if "user_name" in updates and updates["user_name"] != admin.user_name:
        existing = await AdminAccount.filter(user_name=updates["user_name"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="此道号已被使用")
    
    # 处理密码哈希
    if "password" in updates and updates["password"]:
        from server.core import security
        updates["password"] = security.get_password_hash(updates["password"])
    elif "password" in updates:
        del updates["password"]
    
    await admin.update_from_dict(updates)
    await admin.save()
    
    return admin

@router.delete("/accounts/{admin_id}")
async def delete_admin_account(
    admin_id: int,
    current_admin: AdminAccount = Depends(deps.get_admin_or_super_admin)
):
    """删除管理员账号"""
    if current_admin.id == admin_id:
        raise HTTPException(status_code=400, detail="不能删除自己的账号")
    
    admin = await AdminAccount.get_or_none(id=admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="仙官不存在")
    
    await admin.delete()
    return {"message": "仙官已被免职"}

@router.get("/me", response_model=schema.AdminAccount)
async def get_current_admin(
    current_admin: AdminAccount = Depends(deps.get_admin_or_super_admin)
):
    """获取当前登录管理员信息"""
    return current_admin

@router.post("/accounts", response_model=schema.AdminAccount)
async def create_admin_account(
    admin_data: dict,
    current_admin: AdminAccount = Depends(deps.get_admin_or_super_admin)
):
    """创建新的管理员账号"""
    from server.core import security
    
    # 检查用户名是否已存在
    existing = await AdminAccount.filter(user_name=admin_data["user_name"]).first()
    if existing:
        raise HTTPException(status_code=400, detail="此道号已被使用")
    
    # 哈希密码
    if "password" in admin_data:
        admin_data["password"] = security.get_password_hash(admin_data["password"])
    
    admin = await AdminAccount.create(**admin_data)
    return admin
