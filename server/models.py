from tortoise import fields
from tortoise.models import Model
from datetime import datetime

# --- 核心账户模型 ---

class PlayerAccount(Model):
    id = fields.IntField(pk=True)
    user_name = fields.CharField(max_length=50, unique=True, description="玩家道号")
    password = fields.CharField(max_length=255, description="哈希后的凭证")
    created_at = fields.DatetimeField(auto_now_add=True, description="创角时间")
    is_banned = fields.BooleanField(default=False, description="是否被封禁")

    class Meta:
        table = "player_accounts"

class AdminAccount(Model):
    id = fields.IntField(pk=True)
    user_name = fields.CharField(max_length=50, unique=True, description="仙官道号")
    password = fields.CharField(max_length=255, description="哈希后的凭证")
    role = fields.CharField(max_length=20, default="admin", description="仙官品阶 (admin, super_admin)")
    redemption_code_limit = fields.IntField(default=-1, description="可创建兑换码上限 (-1为无限制)")
    created_at = fields.DatetimeField(auto_now_add=True, description="授印时间")

    class Meta:
        table = "admin_accounts"

# --- 游戏内容模型 ---

class World(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True, description="世界名称")
    description = fields.TextField(null=True, description="世界描述")
    era = fields.CharField(max_length=50, null=True, description="时代背景")
    core_rules = fields.JSONField(null=True, description="核心规则设定")
    creator = fields.ForeignKeyField("models.AdminAccount", related_name="created_worlds", description="创世仙官")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "worlds"

# --- 天资等级和先天属性模型 ---

class TalentTier(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, description="天资等级名称")  # 如：废柴、普通、优秀、天才、妖孽、逆天
    description = fields.TextField(null=True, description="等级描述")
    total_points = fields.IntField(description="总可分配点数")  # 如：60, 70, 80, 90, 100, 120
    rarity = fields.IntField(description="稀有度，数字越小越稀有")
    color = fields.CharField(max_length=20, default="white", description="显示颜色")

    class Meta:
        table = "talent_tiers"

class CharacterBase(Model):
    """角色基础创建信息"""
    id = fields.IntField(pk=True)
    character_name = fields.CharField(max_length=100, description="角色名称")
    player = fields.ForeignKeyField("models.PlayerAccount", related_name="character_bases")
    world = fields.ForeignKeyField("models.World", related_name="character_bases")
    talent_tier = fields.ForeignKeyField("models.TalentTier", related_name="characters")
    
    # 先天六司 - 永恒基础属性
    root_bone = fields.IntField(description="根骨 - 体质根基")  # 决定气血、恢复、寿命
    spirituality = fields.IntField(description="灵性 - 灵气亲和")  # 决定灵气上限、吸收效率
    comprehension = fields.IntField(description="悟性 - 理解天赋")  # 决定神识、学习效率
    fortune = fields.IntField(description="福缘 - 机缘造化")  # 决定奇遇概率、物品品质
    charm = fields.IntField(description="魅力 - 容貌气质")  # 决定好感度、社交加成
    temperament = fields.IntField(description="心性 - 道心坚韧")  # 决定心魔抗性、意志力
    
    # 选择的天赋、灵根、出身
    origin = fields.ForeignKeyField("models.Origin", related_name="characters", null=True)
    spirit_root = fields.ForeignKeyField("models.SpiritRoot", related_name="characters", null=True)
    selected_talents = fields.JSONField(null=True, description="选择的天赋列表")
    
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "character_bases"

class Origin(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, description="出身名称")
    description = fields.TextField(null=True, description="出身描述")
    
    # 六司属性加成
    root_bone_modifier = fields.IntField(default=0, description="根骨修正")
    spirituality_modifier = fields.IntField(default=0, description="灵性修正") 
    comprehension_modifier = fields.IntField(default=0, description="悟性修正")
    fortune_modifier = fields.IntField(default=0, description="福缘修正")
    charm_modifier = fields.IntField(default=0, description="魅力修正")
    temperament_modifier = fields.IntField(default=0, description="心性修正")
    
    # 特殊效果
    special_effects = fields.JSONField(null=True, description="特殊效果")
    
    rarity = fields.IntField(default=3, description="稀有度")
    talent_cost = fields.IntField(default=0, description="天赋点消耗")

    class Meta:
        table = "core_origins"

class SpiritRoot(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    description = fields.TextField(null=True)
    base_multiplier = fields.FloatField()
    talent_cost = fields.IntField(default=0, description="天赋点消耗")

    class Meta:
        table = "core_spirit_roots"

class Talent(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    description = fields.TextField(null=True)
    effects = fields.JSONField(null=True)
    rarity = fields.IntField(default=2)
    talent_cost = fields.IntField(default=1, description="天赋点消耗")
    max_uses = fields.IntField(default=1, description="最大使用次数")

    class Meta:
        table = "core_talents"

class Realm(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    title = fields.CharField(max_length=50, null=True)
    description = fields.TextField(null=True)
    order = fields.IntField(unique=True)

    class Meta:
        table = "realms"

class RedemptionCode(Model):
    id = fields.IntField(pk=True)
    code = fields.CharField(max_length=50, unique=True)
    type = fields.CharField(max_length=50)
    payload = fields.JSONField(null=True)
    max_uses = fields.IntField(default=1)
    times_used = fields.IntField(default=0)
    expires_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    creator = fields.ForeignKeyField("models.AdminAccount", related_name="created_codes", null=True, on_delete=fields.SET_NULL, description="创建此码的仙官")
    used_by = fields.ForeignKeyField("models.PlayerAccount", related_name="used_codes", null=True, on_delete=fields.CASCADE)

    class Meta:
        table = "redemption_codes"

# --- 扩展内容模型 ---

class CultivationArt(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    function = fields.TextField(null=True)
    level_system = fields.JSONField(null=True)
    experience_curve = fields.JSONField(null=True)
    success_formula = fields.JSONField(null=True)
    resource_cost = fields.JSONField(null=True)
    recipes = fields.JSONField(null=True)
    note = fields.TextField(null=True)

    class Meta:
        table = "cultivation_arts"

class CultivationPath(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    concept = fields.TextField(null=True)
    description = fields.TextField(null=True)

    class Meta:
        table = "cultivation_paths"

class Organization(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    type = fields.CharField(max_length=50, null=True)

    class Meta:
        table = "organizations"

class Profession(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    description = fields.TextField(null=True)

    class Meta:
        table = "professions"

class WeaponType(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    category = fields.CharField(max_length=50, null=True)

    class Meta:
        table = "weapon_types"