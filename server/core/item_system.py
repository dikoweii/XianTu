"""
物品系统模块
管理角色背包、装备和物品相关功能
"""

from typing import Dict, List, Any, Optional
from enum import Enum

class ItemType(str, Enum):
    """物品类型枚举"""
    CONSUMABLE = "consumable"  # 消耗品
    WEAPON = "weapon"          # 武器
    ARMOR = "armor"            # 防具
    ACCESSORY = "accessory"    # 饰品
    MATERIAL = "material"      # 材料
    BOOK = "book"             # 书籍
    PILL = "pill"             # 丹药
    TALISMAN = "talisman"     # 符箓
    TREASURE = "treasure"     # 宝物

class ItemRarity(str, Enum):
    """物品稀有度枚举"""
    COMMON = "common"      # 普通（白色）
    UNCOMMON = "uncommon"  # 不凡（绿色）
    RARE = "rare"          # 稀有（蓝色）
    EPIC = "epic"          # 史诗（紫色）
    LEGENDARY = "legendary" # 传说（橙色）
    MYTHIC = "mythic"      # 神话（红色）

class EquipSlot(str, Enum):
    """装备栏位枚举"""
    WEAPON = "weapon"          # 武器
    HEAD = "head"             # 头部
    CHEST = "chest"           # 胸甲
    LEGS = "legs"             # 腿甲
    FEET = "feet"             # 鞋子
    GLOVES = "gloves"         # 手套
    RING = "ring"             # 戒指
    NECKLACE = "necklace"     # 项链
    TALISMAN = "talisman"     # 护身符

def create_item(
    item_id: str,
    name: str,
    description: str,
    item_type: ItemType,
    rarity: ItemRarity = ItemRarity.COMMON,
    quantity: int = 1,
    attributes: Optional[Dict[str, Any]] = None,
    equip_slot: Optional[EquipSlot] = None,
    **kwargs
) -> Dict[str, Any]:
    """创建物品数据结构"""
    return {
        "id": item_id,
        "name": name,
        "description": description,
        "type": item_type.value,
        "rarity": rarity.value,
        "quantity": quantity,
        "attributes": attributes or {},
        "equip_slot": equip_slot.value if equip_slot else None,
        "created_at": kwargs.get("created_at"),
        "metadata": kwargs.get("metadata", {})
    }

def get_initial_items() -> Dict[str, Any]:
    """获取初始背包物品"""
    initial_items = {}
    
    # 新手物品
    initial_items["novice_robe"] = create_item(
        item_id="novice_robe",
        name="新手道袍",
        description="初入修仙界的基础道袍，虽然简陋但能提供基本的防护。",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.COMMON,
        quantity=1,
        equip_slot=EquipSlot.CHEST,
        attributes={
            "defense": 5,
            "spirit_defense": 3
        }
    )
    
    initial_items["wooden_sword"] = create_item(
        item_id="wooden_sword",
        name="木剑",
        description="新手使用的木制剑器，虽然攻击力有限，但是练习基础剑法的好工具。",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.COMMON,
        quantity=1,
        equip_slot=EquipSlot.WEAPON,
        attributes={
            "attack": 8,
            "durability": 100,
            "max_durability": 100
        }
    )
    
    initial_items["basic_shoes"] = create_item(
        item_id="basic_shoes",
        name="布鞋",
        description="朴素的布制鞋子，行走时较为舒适。",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.COMMON,
        quantity=1,
        equip_slot=EquipSlot.FEET,
        attributes={
            "defense": 2,
            "speed": 1
        }
    )
    
    # 初始消耗品
    initial_items["healing_pill"] = create_item(
        item_id="healing_pill",
        name="回春丹",
        description="最基础的疗伤丹药，能够快速恢复少量气血。",
        item_type=ItemType.PILL,
        rarity=ItemRarity.COMMON,
        quantity=3,
        attributes={
            "heal_amount": 50,
            "heal_type": "health"
        }
    )
    
    initial_items["qi_pill"] = create_item(
        item_id="qi_pill",
        name="聚气丹",
        description="补充灵气的基础丹药，能够快速恢复少量灵气。",
        item_type=ItemType.PILL,
        rarity=ItemRarity.COMMON,
        quantity=3,
        attributes={
            "heal_amount": 40,
            "heal_type": "spiritual"
        }
    )
    
    # 材料物品
    initial_items["spirit_grass"] = create_item(
        item_id="spirit_grass",
        name="灵草",
        description="含有微弱灵气的草药，是炼制低级丹药的基础材料。",
        item_type=ItemType.MATERIAL,
        rarity=ItemRarity.COMMON,
        quantity=5,
        attributes={
            "material_type": "herb",
            "spiritual_power": 1
        }
    )
    
    # 基础书籍
    initial_items["basic_cultivation_manual"] = create_item(
        item_id="basic_cultivation_manual",
        name="基础修炼手册",
        description="记录了修仙入门知识的册子，新手修士的必读之物。",
        item_type=ItemType.BOOK,
        rarity=ItemRarity.COMMON,
        quantity=1,
        attributes={
            "book_type": "manual",
            "knowledge_points": 10
        }
    )
    
    return initial_items

def get_initial_equipment() -> Dict[str, Any]:
    """获取初始装备（已装备的物品）"""
    return {
        "weapon": None,      # 武器栏位
        "head": None,        # 头部栏位
        "chest": None,       # 胸甲栏位
        "legs": None,        # 腿甲栏位
        "feet": None,        # 鞋子栏位
        "gloves": None,      # 手套栏位
        "ring": None,        # 戒指栏位
        "necklace": None,    # 项链栏位
        "talisman": None,    # 护身符栏位
    }

def calculate_equipment_stats(equipped_items: Dict[str, Any]) -> Dict[str, int]:
    """计算装备属性加成"""
    stats = {
        "attack": 0,
        "defense": 0,
        "spirit_defense": 0,
        "speed": 0,
        "critical_rate": 0,
        "accuracy": 0
    }
    
    for slot, item_id in equipped_items.items():
        if item_id:
            # 这里应该从物品数据库或缓存中获取物品属性
            # 暂时返回基础属性，后续可以扩展
            pass
    
    return stats

def add_item_to_inventory(inventory: Dict[str, Any], item: Dict[str, Any]) -> bool:
    """向背包添加物品"""
    item_id = item["id"]
    
    if item_id in inventory:
        # 如果物品已存在，增加数量
        inventory[item_id]["quantity"] += item["quantity"]
    else:
        # 添加新物品
        inventory[item_id] = item.copy()
    
    return True

def remove_item_from_inventory(inventory: Dict[str, Any], item_id: str, quantity: int = 1) -> bool:
    """从背包移除物品"""
    if item_id not in inventory:
        return False
    
    current_quantity = inventory[item_id]["quantity"]
    if current_quantity < quantity:
        return False
    
    inventory[item_id]["quantity"] -= quantity
    
    # 如果数量为0，移除该物品
    if inventory[item_id]["quantity"] <= 0:
        del inventory[item_id]
    
    return True

def equip_item(inventory: Dict[str, Any], equipped_items: Dict[str, Any], item_id: str) -> bool:
    """装备物品"""
    if item_id not in inventory:
        return False
    
    item = inventory[item_id]
    equip_slot = item.get("equip_slot")
    
    if not equip_slot:
        return False  # 该物品不能装备
    
    # 如果装备栏已有物品，先卸下
    if equipped_items[equip_slot]:
        unequip_item(inventory, equipped_items, equip_slot)
    
    # 装备新物品
    equipped_items[equip_slot] = item_id
    
    # 从背包中移除一个（装备不消耗物品，只是转移）
    remove_item_from_inventory(inventory, item_id, 1)
    
    return True

def unequip_item(inventory: Dict[str, Any], equipped_items: Dict[str, Any], equip_slot: str) -> bool:
    """卸下装备"""
    if equip_slot not in equipped_items or not equipped_items[equip_slot]:
        return False
    
    item_id = equipped_items[equip_slot]
    equipped_items[equip_slot] = None
    
    # 将物品放回背包
    # 这里需要根据item_id重新创建物品数据
    # 暂时简化处理
    return True

def use_consumable_item(inventory: Dict[str, Any], item_id: str, character_state: Dict[str, Any]) -> bool:
    """使用消耗品"""
    if item_id not in inventory:
        return False
    
    item = inventory[item_id]
    if item["type"] != ItemType.CONSUMABLE.value and item["type"] != ItemType.PILL.value:
        return False
    
    # 根据物品属性应用效果
    attributes = item.get("attributes", {})
    heal_amount = attributes.get("heal_amount", 0)
    heal_type = attributes.get("heal_type", "health")
    
    if heal_type == "health":
        character_state["health_points"] = min(
            character_state["health_points"] + heal_amount,
            character_state["max_health_points"]
        )
    elif heal_type == "spiritual":
        character_state["spiritual_power"] = min(
            character_state["spiritual_power"] + heal_amount,
            character_state["max_spiritual_power"]
        )
    
    # 消耗物品
    remove_item_from_inventory(inventory, item_id, 1)
    
    return True