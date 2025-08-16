from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

# --- 密码哈希 ---
# 使用 bcrypt 算法，这是目前非常安全的选择
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- JWT 令牌设置 ---
# !! 警告: 这个密钥在生产环境中必须替换为一个真正的、随机生成的、保密的字符串 !!
# !! 可以通过 `openssl rand -hex 32` 命令生成
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080 # 令牌有效期 (7天)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证明文密码与哈希密码是否匹配"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """生成密码的哈希值"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    创建 JWT 访问令牌
    :param data: 需要编码到令牌中的数据 (通常是用户标识)
    :param expires_delta: 令牌的有效期，如果未提供，则使用默认值
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    解码 JWT 访问令牌
    :param token: JWT 令牌字符串
    :return: 解码后的载荷数据
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

