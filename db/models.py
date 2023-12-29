# from ctypes import Union
from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, EmailStr
import time
from sqlmodel import SQLModel, Field, Relationship, Session


class UserBase(SQLModel, table=True):
    __tablename__ = "globaluser"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = None
    nickname: str = None
    is_superuser: Optional[int]
    # pip install pydantic[email] 使用email验证的时候需要增加这个库
    email: Optional[EmailStr] = None
    password: str = None
