from fastapi import APIRouter, Request
from server.models import CharacterBase

router = APIRouter()

@router.get("/test_direct")
async def test_direct_access():
    """
    直接测试角色数据访问，无任何认证
    """
    try:
        characters = await CharacterBase.filter().count()
        return {"message": "成功", "character_count": characters}
    except Exception as e:
        return {"error": str(e)}

@router.get("/test_with_request")
async def test_with_request(request: Request):
    """
    测试带Request的访问
    """
    return {"message": "请求成功", "headers": dict(request.headers)}