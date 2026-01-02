"""
系统配置服务层

将可动态调整的配置存储在数据库中，支持后台管理界面修改。
这些配置不需要重启服务即可生效。
"""

from typing import Any
from server.models import SystemConfig


# 默认配置值
DEFAULT_CONFIGS = {
    # Cloudflare Turnstile 人机验证
    "turnstile_enabled": True,
    "turnstile_secret_key": None,
    "turnstile_verify_url": "https://challenges.cloudflare.com/turnstile/v0/siteverify",

    # 邮箱验证
    "email_verification_enabled": False,
    "smtp_host": "smtp.qq.com",
    "smtp_port": 465,
    "smtp_user": None,
    "smtp_password": None,
    "smtp_from_email": None,
    "smtp_from_name": "仙途游戏",
    "email_code_expire_minutes": 10,

    # IP 限流
    "register_rate_limit_enabled": True,
    "register_rate_limit_max": 5,
    "register_rate_limit_window": 3600,
}


async def get_config(key: str, default: Any = None) -> Any:
    """获取单个配置值"""
    config = await SystemConfig.filter(key=key).first()
    if config:
        return config.value
    # 如果数据库没有，返回默认值
    return DEFAULT_CONFIGS.get(key, default)


async def get_configs(*keys: str) -> dict[str, Any]:
    """批量获取多个配置值"""
    result = {}
    configs = await SystemConfig.filter(key__in=keys).all()

    # 从数据库获取的值
    db_values = {c.key: c.value for c in configs}

    # 合并默认值和数据库值
    for key in keys:
        if key in db_values:
            result[key] = db_values[key]
        else:
            result[key] = DEFAULT_CONFIGS.get(key)

    return result


async def set_config(key: str, value: Any) -> None:
    """设置单个配置值"""
    await SystemConfig.update_or_create(
        key=key,
        defaults={"value": value}
    )


async def set_configs(configs: dict[str, Any]) -> None:
    """批量设置多个配置值"""
    for key, value in configs.items():
        await set_config(key, value)


async def get_all_configs() -> dict[str, Any]:
    """获取所有配置（合并默认值和数据库值）"""
    result = DEFAULT_CONFIGS.copy()

    # 数据库值覆盖默认值
    db_configs = await SystemConfig.all()
    for config in db_configs:
        result[config.key] = config.value

    return result


async def init_default_configs() -> None:
    """初始化默认配置到数据库（仅在配置不存在时创建）"""
    for key, value in DEFAULT_CONFIGS.items():
        existing = await SystemConfig.filter(key=key).first()
        if not existing:
            await SystemConfig.create(key=key, value=value)


# 便捷函数：获取特定类别的配置
async def get_turnstile_config() -> dict[str, Any]:
    """获取 Turnstile 相关配置"""
    return await get_configs(
        "turnstile_enabled",
        "turnstile_secret_key",
        "turnstile_verify_url",
    )


async def get_email_config() -> dict[str, Any]:
    """获取邮箱验证相关配置"""
    return await get_configs(
        "email_verification_enabled",
        "smtp_host",
        "smtp_port",
        "smtp_user",
        "smtp_password",
        "smtp_from_email",
        "smtp_from_name",
        "email_code_expire_minutes",
    )


async def get_rate_limit_config() -> dict[str, Any]:
    """获取限流相关配置"""
    return await get_configs(
        "register_rate_limit_enabled",
        "register_rate_limit_max",
        "register_rate_limit_window",
    )
