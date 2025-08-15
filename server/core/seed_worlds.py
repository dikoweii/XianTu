from typing import List, Dict, Any
from server.models import World, AdminAccount

# 从seed.py整合过来的完整世界数据
DEFAULT_WORLDS: List[Dict[str, Any]] = [
    {
        "name": '朝天大陆',
        "description": """此方世界名为"朝天大陆"，乃是一处天道完整、灵气充沛的上善之地。其核心法则是"万灵竞渡，一步登天"，无论是人、妖、精、怪，皆有缘法踏上修行之路，叩问长生。
仙凡之别在此界泾渭分明，宛若天渊。凡人寿不过百载，受生老病死之苦，终归一抔黄土；而修士一旦踏入道途，便能吞吐天地灵气，淬炼己身，寿元动辄千载，更有大能者与天地同寿。凡俗王朝更迭，于修士而言不过是弹指一瞬间。在凡人眼中，修士是高悬于九天的仙神，一言可定一国兴衰，一念可引风雨雷霆。然而，这种力量并非毫无代价。
此界奉行"大道争锋"的铁则，天道予万物机缘，却也降下无尽凶险。灵脉宝地、神功秘法、天材地宝，皆是有缘者居之，而"缘"字背后，往往是血与火的洗礼。修士之间，为求道途精进，争斗乃是常态。同门可能反目，挚友亦会背叛，杀人夺宝、斩草除根之事屡见不鲜。这是一个极度自由的世界，你可以选择成为守护一方的善仙，亦可成为肆虐八荒的魔头，只要你有足够的实力。但自由的背后，是无处不在的危险，一步踏错，便是万劫不复，身死道消。
然天道亦有制衡，修士若无故以大法力干涉凡俗王朝更迭、屠戮凡人，便会与此方天地结下因果。虽无业报加身，却会在日后冲击更高境界、渡劫飞升之时，引来更强大的天劫，平添无数变数。故而多数修士选择在山门清修，或于红尘历练，以求勘破心障，证得大道。修仙百艺——炼丹、炼器、符箓、阵法，在此界发展到了极致，共同构筑了一个无比兴盛、却也无比残酷的修仙文明。""",
        "era": '朝天历元年'
    }
]

async def seed():
    """
    使用 Tortoise-ORM 将预设的世界背景数据填充到数据库中。
    """
    print("--- [Worlds] 开始播种世界数据 (ORM)... ---")
    
    # 确保 admin 用户存在，作为作者（不创建重复用户）
    admin_user = await AdminAccount.get_or_none(user_name="admin")
    if not admin_user:
        # 如果admin不存在，检查是否有super_admin
        admin_user = await AdminAccount.filter(role="super_admin").first()
        if not admin_user:
            # 如果没有任何超级管理员，创建一个
            admin_user = await AdminAccount.create(
                user_name="admin",
                password="hashed_password_placeholder", 
                role="super_admin"
            )

    for world_data in DEFAULT_WORLDS:
        existing_world = await World.get_or_none(name=world_data["name"])
        
        if existing_world:
            # 更新描述
            if existing_world.description != world_data["description"]:
                existing_world.description = world_data["description"]
                existing_world.era = world_data.get("era")
                await existing_world.save()
                print(f"--- [Worlds] 成功更新世界: '{existing_world.name}' ---")
            else:
                print(f"--- [Worlds] 世界 '{existing_world.name}' 已是最新，无需更新。 ---")
        else:
            # 创建世界
            await World.create(
                name=world_data["name"],
                description=world_data["description"],
                era=world_data.get("era"),
                creator=admin_user
            )
            print(f"--- [Worlds] 成功创建世界: '{world_data['name']}' ---")

    print("--- [Worlds] 世界数据播种完毕 (ORM)。 ---")

if __name__ == '__main__':
    import asyncio
    from tortoise import Tortoise
    from server.main import TORTOISE_ORM

    async def run():
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()
        await seed()
        await Tortoise.close_connections()

    asyncio.run(run())