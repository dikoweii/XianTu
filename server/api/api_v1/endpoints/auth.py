import httpx
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from server.core import security, config
from server.crud import crud_user
from server.schemas import schema
from server.api.api_v1 import deps
from server.models import PlayerAccount

router = APIRouter()

# Cloudflare Turnstile 验证函数
async def verify_turnstile(token: str, remote_ip: str) -> bool:
    # 在开发环境下，直接通过验证
    print(f"环境设置: {config.settings.ENVIRONMENT}")
    if config.settings.ENVIRONMENT == "development":
        print("开发环境，跳过人机验证")
        return True
        
    if not token:
        return False
        
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://challenges.cloudflare.com/turnstile/v0/siteverify",
                data={
                    "secret": config.settings.TURNSTILE_SECRET_KEY,
                    "response": token,
                    "remoteip": remote_ip,
                },
            )
            response.raise_for_status()
            result = response.json()
            return result.get("success", False)
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

@router.get("/test_no_deps", tags=["测试"])
async def test_no_dependencies():
    """
    测试没有依赖项的端点
    """
    return {"message": "在auth router中，没有依赖项", "status": "ok"}

@router.post("/token", response_model=schema.Token)
async def login_for_access_token(request: Request, login_data: schema.LoginRequest):
    """
    **修者登录**
    
    用道号和凭证换取访问令牌，并进行人机验证。
    """
    # 验证 Turnstile token
    remote_ip = request.client.host
    is_human = await verify_turnstile(login_data.turnstile_token, remote_ip)
    if not is_human:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="人机验证失败，请重试",
        )

    player = await crud_user.authenticate_player(
        user_name=login_data.username, password=login_data.password
    )
    if not player:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="道号或凭证错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(
        data={"sub": player.user_name}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=schema.PlayerAccount)
async def register_player(request: Request, player_in: schema.PlayerAccountCreateWithTurnstile):
    """
    **接引新修者**
    
    创建新的修者账号，并进行人机验证。
    """
    # 验证 Turnstile token
    remote_ip = request.client.host
    is_human = await verify_turnstile(player_in.turnstile_token, remote_ip)
    if not is_human:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="人机验证失败，请重试",
        )

    player_create_data = schema.PlayerAccountCreate(
        user_name=player_in.user_name,
        password=player_in.password
    )
    
    new_player, message = await crud_user.create_player(player_data=player_create_data)
    if not new_player:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )
    return new_player

@router.get("/me", response_model=schema.PlayerAccount)
async def read_current_user(
    current_user: PlayerAccount = Depends(deps.get_current_user),
):
    """
    **获取当前修者信息**
    
    需要有效的访问令牌。
    """
    return current_user