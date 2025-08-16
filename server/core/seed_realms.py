# -*- coding: utf-8 -*-
"""
境界体系种子数据
包含从凡人到渡劫期的完整境界设定
"""

from server.models import Realm

async def seed_realms():
    """
    创建修仙境界体系的核心数据
    """
    print("正在种下境界体系...")
    
    realms_data = [
        {
            "name": "凡人",
            "title": "未入修行",  
            "description": "尚未踏入修仙之道的凡俗生灵，寿命有限，无法感应灵气。",
            "order": 0
        },
        {
            "name": "炼气",
            "title": "问道童子",
            "description": "引气入体，洗涤凡躯。在凡间已是异人，可施展微末法术。",
            "order": 1
        },
        {
            "name": "筑基", 
            "title": "入道之士",
            "description": "灵气液化，丹田筑基。正式脱凡，可御器飞行。",
            "order": 2
        },
        {
            "name": "金丹",
            "title": "真人",
            "description": "灵液结丹，法力自生。在修行界可开宗立派，为一派老祖。",
            "order": 3
        },
        {
            "name": "元婴",
            "title": "真君", 
            "description": "丹碎婴生，神魂寄托。元婴不灭，真灵不死。",
            "order": 4
        },
        {
            "name": "化神",
            "title": "道君",
            "description": "神游太虚，感悟法则。神识即领域，意念可干涉现实。",
            "order": 5
        },
        {
            "name": "炼虚",
            "title": "尊者", 
            "description": "身融虚空，掌握空间。咫尺天涯，可短暂撕裂空间。",
            "order": 6
        },
        {
            "name": "合体",
            "title": "大能",
            "description": "法则归体，身即是道。一举一动皆引动大道共鸣。",
            "order": 7
        },
        {
            "name": "渡劫",
            "title": "问天者",
            "description": "超脱世界，叩问天道。已是人间道之极致，引动天劫。",
            "order": 8
        }
    ]
    
    created_count = 0
    for realm_data in realms_data:
        existing = await Realm.get_or_none(name=realm_data["name"])
        if not existing:
            await Realm.create(**realm_data)
            created_count += 1
            print(f"   创建境界：{realm_data['name']} ({realm_data['title']})")
        else:
            print(f"   境界已存在：{realm_data['name']}")
    
    print(f"境界体系种子完成！新增 {created_count} 个境界")
    return created_count

if __name__ == '__main__':
    import asyncio
    from tortoise import Tortoise
    from server.main import TORTOISE_ORM

    async def run():
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()
        await seed_realms()
        await Tortoise.close_connections()

    asyncio.run(run())