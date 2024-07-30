from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from .models import Workspace, Page, Block, Database, DatabaseRow, Property, Comment, ActivityLog
from .schema import WorkspaceSchema, PageSchema, BlockSchema, DatabaseSchema, DatabaseRowSchema, PropertySchema, CommentSchema, ActivityLogSchema
from incidentmanagement.response import response_wrapper

router = Router()


@router.get("/workspaces/", response=List[WorkspaceSchema])
def get_workspaces(request):
    qs = Workspace.object.all()
    return response_wrapper(WorkspaceSchema(many=True).dump(qs), status_code=200, message="Success")


@router.get("/workspaces/{workspace_id}/", response=WorkspaceSchema)
def get_workspace(request, workspace_id: int):
    return get_object_or_404(Workspace, id=workspace_id)


@router.post("/workspaces/", response=WorkspaceSchema)
def create_workspace(request, payload: WorkspaceSchema):
    qs = Workspace.objects.create(**payload.dict())
    return response_wrapper(WorkspaceSchema().dump(qs), status_code=201, message="Workspace created successfully")


@router.put("/workspaces/{workspace_id}/", response=WorkspaceSchema)
def update_workspace(request, workspace_id: int, payload: WorkspaceSchema):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    workspace.name = payload.name
    workspace.save()
    return {"success": True}


@router.delete("/workspaces/{workspace_id}/", response=WorkspaceSchema)
def delete_workspace(request, workspace_id: int):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    workspace.delete()
    return {"success": True}


@router.get("/workspaces/{workspace_id}/pages/", response=List[PageSchema])
def get_pages(request, workspace_id: int):
    return Page.objects.filter(workspace_id=workspace_id)


@router.get("/workspaces/{workspace_id}/pages/{page_id}/", response=PageSchema)
def get_page(request, workspace_id: int, page_id: int):
    return get_object_or_404(Page, workspace_id=workspace_id, id=page_id)


@router.post("/workspaces/{workspace_id}/pages/", response=PageSchema)
def create_page(request, workspace_id: int, payload: PageSchema):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    return Page.objects.create(workspace=workspace, **payload.dict())


@router.put("/workspaces/{workspace_id}/pages/{page_id}/", response=PageSchema)
def update_page(request, workspace_id: int, page_id: int, payload: PageSchema):
    page = get_object_or_404(Page, workspace_id=workspace_id, id=page_id)
    page.title = payload.title
    page.save()
    return {"success": True}


@router.delete("/workspaces/{workspace_id}/pages/{page_id}/", response=PageSchema)
def delete_page(request, workspace_id: int, page_id: int):
    page = get_object_or_404(Page, workspace_id=workspace_id, id=page_id)
    page.delete()
    return {"success": True}



@router.get("/workspaces/{workspace_id}/pages/{page_id}/blocks/", response=List[BlockSchema])
def get_blocks(request, workspace_id: int, page_id: int):
    return Block.objects.filter(page_id=page_id)


@router.get("/workspaces/{workspace_id}/pages/{page_id}/blocks/{block_id}/", response=BlockSchema)
def get_block(request, workspace_id: int, page_id: int, block_id: int):
    return get_object_or_404(Block, page_id=page_id, id=block_id)


@router.post("/workspaces/{workspace_id}/pages/{page_id}/blocks/", response=BlockSchema)
def create_block(request, workspace_id: int, page_id: int, payload: BlockSchema):
    page = get_object_or_404(Page, workspace_id=workspace_id, id=page_id)
    return Block.objects.create(page=page, **payload.dict())


@router.put("/workspaces/{workspace_id}/pages/{page_id}/blocks/{block_id}/", response=BlockSchema)
def update_block(request, workspace_id: int, page_id: int, block_id: int, payload: BlockSchema):
    block = get_object_or_404(Block, page_id=page_id, id=block_id)
    block.content = payload.content
    block.save()
    return {"success": True}


@router.delete("/workspaces/{workspace_id}/pages/{page_id}/blocks/{block_id}/", response=BlockSchema)
def delete_block(request, workspace_id: int, page_id: int, block_id: int):
    block = get_object_or_404(Block, page_id=page_id, id=block_id)
    block.delete()
    return {"success": True}


@router.get("/workspaces/{workspace_id}/databases/", response=List[DatabaseSchema])
def get_databases(request, workspace_id: int):
    return Database.objects.filter(workspace_id=workspace_id)


@router.get("/workspaces/{workspace_id}/databases/{database_id}/", response=DatabaseSchema)
def get_database(request, workspace_id: int, database_id: int):
    return get_object_or_404(Database, workspace_id=workspace_id, id=database_id)


@router.get("/workspaces/{workspace_id}/databases/{database_id}/rows/", response=List[DatabaseRowSchema])
def get_rows(request, workspace_id: int, database_id: int):
    return DatabaseRow.objects.filter(database_id=database_id)


@router.get("/workspaces/{workspace_id}/databases/{database_id}/rows/{row_id}/", response=DatabaseRowSchema)
def get_row(request, workspace_id: int, database_id: int, row_id: int):
    return get_object_or_404(DatabaseRow, database_id=database_id, id=row_id)


@router.post("/workspaces/{workspace_id}/databases/{database_id}/rows/", response=DatabaseRowSchema)
def create_row(request, workspace_id: int, database_id: int, payload: DatabaseRowSchema):
    database = get_object_or_404(Database, workspace_id=workspace_id, id=database_id)
    return DatabaseRow.objects.create(database=database, **payload.dict())


@router.get("/workspaces/{workspace_id}/databases/{database_id}/properties/", response=List[PropertySchema])
def get_properties(request, workspace_id: int, database_id: int):
    return Property.objects.filter(database_id=database_id)


@router.get("/workspaces/{workspace_id}/databases/{database_id}/properties/{property_id}/", response=PropertySchema)
def get_property(request, workspace_id: int, database_id: int, property_id: int):
    return get_object_or_404(Property, database_id=database_id, id=property_id)


@router.post("/workspaces/{workspace_id}/databases/{database_id}/properties/", response=PropertySchema)
def create_property(request, workspace_id: int, database_id: int, payload: PropertySchema):
    database = get_object_or_404(Database, workspace_id=workspace_id, id=database_id)
    return Property.objects.create(database=database, **payload.dict())


# get all comments for a given block or page
@router.get("/workspaces/{workspace_id}/pages/{page_id}/comments/", response=List[CommentSchema])
def get_comments_for_page(request, workspace_id: int, page_id: int):
    return Comment.objects.filter(page_id=page_id)


@router.get("/workspaces/{workspace_id}/blocks/{block_id}/comments/", response=List[CommentSchema])
def get_comments_for_block(request, workspace_id: int, block_id: int):
    return Comment.objects.filter(block_id=block_id)


# get activity logs for a given block or page
@router.get("/workspaces/{workspace_id}/pages/{page_id}/activity/", response=List[ActivityLogSchema])
def get_activity_logs_for_page(request, workspace_id: int, page_id: int):
    return ActivityLog.objects.filter(page_id=page_id)


@router.get("/workspaces/{workspace_id}/blocks/{block_id}/activity/", response=List[ActivityLogSchema])
def get_activity_logs_for_block(request, workspace_id: int, block_id: int):
    return ActivityLog.objects.filter(block_id=block_id)
