from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Dict, Any, List

from server.schemas import schema
from server.crud import crud_character, crud_origins, crud_spirit_roots, crud_talents
from server.api.api_v1 import deps
from server.models import PlayerAccount

router = APIRouter()

@router.get("/creation_data", response_model=schema.CreationDataResponse, tags=["角色/存档体系"])
async def get_creation_data(world_id: int = Query(..., description="世界ID")):
    """
    获取角色创建所需的基础数据（出身、灵根、天赋等）
    """
    try:
        origins = await crud_origins.get_origins()
        spirit_roots = await crud_spirit_roots.get_spirit_roots()
        talents = await crud_talents.get_talents()
        
        # 转换为前端需要的格式
        origins_data = []
        for o in origins:
            attribute_modifiers = {
                "root_bone": o.root_bone_modifier,
                "spirituality": o.spirituality_modifier,  
                "comprehension": o.comprehension_modifier,
                "fortune": o.fortune_modifier,
                "charm": o.charm_modifier,
                "temperament": o.temperament_modifier
            }
            origins_data.append({
                "id": o.id, 
                "name": o.name, 
                "description": o.description,
                "attribute_modifiers": attribute_modifiers, 
                "rarity": o.rarity,
                "talent_cost": o.talent_cost
            })
        spirit_roots_data = [{"id": sr.id, "name": sr.name, "description": sr.description, 
                            "base_multiplier": sr.base_multiplier, "talent_cost": sr.talent_cost} for sr in spirit_roots]
        talents_data = [{"id": t.id, "name": t.name, "description": t.description, 
                        "effects": t.effects, "rarity": t.rarity, "talent_cost": t.talent_cost, "max_uses": t.max_uses} for t in talents]
        
        return schema.CreationDataResponse(
            origins=origins_data,
            spirit_roots=spirit_roots_data,
            talents=talents_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取创建数据失败: {str(e)}")

@router.post("/create", response_model=schema.CharacterBase)
async def create_character_base(
    character_data: schema.CharacterBaseCreate,
    current_user: PlayerAccount = Depends(deps.get_current_active_user)
):
    """
    创建新角色基础信息
    """
    # 验证天赋点数消耗
    total_cost = 0
    
    # 计算出身消耗
    if character_data.origin_id:
        origin = await crud_origins.get_origin_by_id(character_data.origin_id)
        if not origin:
            raise HTTPException(status_code=404, detail="出身不存在")
        total_cost += origin.talent_cost
    
    # 计算灵根消耗
    if character_data.spirit_root_id:
        spirit_root = await crud_spirit_roots.get_spirit_root_by_id(character_data.spirit_root_id)
        if not spirit_root:
            raise HTTPException(status_code=404, detail="灵根不存在")
        total_cost += spirit_root.talent_cost
    
    # 计算天赋消耗
    if character_data.selected_talent_ids:
        for talent_id in character_data.selected_talent_ids:
            talent = await crud_talents.get_talent_by_id(talent_id)
            if not talent:
                raise HTTPException(status_code=404, detail=f"天赋ID {talent_id} 不存在")
            total_cost += talent.talent_cost
    
    # TODO: 验证天赋点数是否足够（需要从天资等级获取总点数并减去基础属性消耗）
    
    new_character, error_msg = await crud_character.create_character_base(
        player_id=current_user.id,
        world_id=character_data.world_id,
        talent_tier_id=character_data.talent_tier_id,
        character_name=character_data.character_name,
        root_bone=character_data.root_bone,
        spirituality=character_data.spirituality,
        comprehension=character_data.comprehension,
        fortune=character_data.fortune,
        charm=character_data.charm,
        temperament=character_data.temperament,
        origin_id=character_data.origin_id,
        spirit_root_id=character_data.spirit_root_id,
        selected_talent_ids=character_data.selected_talent_ids
    )
    
    if not new_character:
        raise HTTPException(status_code=400, detail=error_msg)
    
    return new_character

@router.get("/my", response_model=List[schema.CharacterBase])
async def get_my_characters(
    current_user: PlayerAccount = Depends(deps.get_current_active_user)
):
    """
    获取当前用户的所有角色
    """
    characters = await crud_character.get_character_bases_by_player(current_user.id)
    return characters

@router.get("/{character_id}", response_model=schema.CharacterBase)
async def get_character(
    character_id: int,
    current_user: PlayerAccount = Depends(deps.get_current_active_user)
):
    """
    获取指定角色详情
    """
    character = await crud_character.get_character_base_by_id(character_id)
    if not character:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    # 验证角色属于当前用户
    if character.player_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权访问此角色")
    
    return character