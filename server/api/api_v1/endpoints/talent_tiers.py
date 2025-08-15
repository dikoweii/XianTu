from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from server.models import TalentTier
from server.schemas import schema
from server.api.api_v1 import deps

router = APIRouter()

@router.get("/", response_model=List[schema.TalentTier])
async def get_talent_tiers():
    """
    获取所有天资等级
    """
    talent_tiers = await TalentTier.all().order_by('rarity')
    return talent_tiers

@router.get("/{tier_id}", response_model=schema.TalentTier)
async def get_talent_tier(tier_id: int):
    """
    根据ID获取天资等级
    """
    talent_tier = await TalentTier.get_or_none(id=tier_id)
    if not talent_tier:
        raise HTTPException(status_code=404, detail="天资等级不存在")
    return talent_tier