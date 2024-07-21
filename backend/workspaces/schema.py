from ninja import  Schema
from typing import List, Optional
from pydantic import Field
from datetime import datetime


class UserSchema(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_staff: bool
    last_login: Optional[datetime]
    date_joined: Optional[datetime]
    is_active: bool
    groups: List[str] = []
    

class WorkspaceSchema(Schema):
    id: int
    name: str
    owner: UserSchema
    created_at: datetime
    updated_at: datetime
    

class PageSchema(Schema):
    id: int
    title: str
    workspace: WorkspaceSchema
    parent_page: Optional[int]
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UserSchema]
    
    
class BlockSchema(Schema):
    id: int
    workspace: WorkspaceSchema
    block_type: str
    content: Optional[str]
    order: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UserSchema]
    page: Optional[PageSchema]
    
    
class DatabaseSchema(Schema):
    id: int
    name: str
    workspace: WorkspaceSchema
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UserSchema]
    
    
class DatabaseRowSchema(Schema):
    id: int
    database: DatabaseSchema
    created_by: Optional[UserSchema]
    created_at: datetime
    updated_at: datetime
    
    
class PropertySchema(Schema):
    id: int
    name: str
    property_type: str
    database: DatabaseSchema
    created_at: datetime
    updated_at: datetime


class CommentSchema(Schema):
    id: int
    content: str
    user: UserSchema
    page: Optional[PageSchema]
    block: Optional[BlockSchema]
    created_at: datetime
    updated_at: datetime
    

class ActivityLogSchema(Schema):
    id: int
    user: UserSchema
    action_type: str
    action: str
    page: Optional[PageSchema]
    block: Optional[BlockSchema]
    created_at: datetime
