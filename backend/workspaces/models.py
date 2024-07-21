from django.db import models

from django.contrib.auth.models import User


class Workspace(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='owned_workspaces', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='workspaces', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.id = None
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Workspace"
        verbose_name_plural = "Workspaces"
        ordering = ['id']
        
    def get_absolute_url(self):
        return f"/workspaces/{self.id}"


class Page(models.Model):
    title = models.CharField(max_length=255)
    workspace = models.ForeignKey(Workspace, related_name='pages', on_delete=models.CASCADE)
    parent_page = models.ForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_pages', on_delete=models.SET_NULL, null=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.id = None
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"
        ordering = ['id']
    
    def get_absolute_url(self):
        return f"/workspaces/{self.workspace.id}/pages/{self.id}"
    
    
class Block(models.Model):
    BLOCK_TYPES = [
        ('text', 'Text'),
        ('heading', 'Heading'),
        ('image', 'Image'),
        ('link', 'Link'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('quote', 'Quote'),
        ('code', 'Code'),
        ('document', 'Document'),
        ('todo_list', 'Todo List'),
    ]
    page = models.ForeignKey(Page, related_name='blocks', on_delete=models.CASCADE)
    block_type = models.CharField(max_length=20, choices=BLOCK_TYPES, default='text')
    content = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_blocks', on_delete=models.SET_NULL, null=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.id = None
        
    def __str__(self):
        return f"{self.block_type} block on {self.page.title}"
    
    class Meta:
        verbose_name = "Block"
        verbose_name_plural = "Blocks"
        ordering = ['page', 'order']
        
    def get_absolute_url(self):
        return f"/workspaces/{self.page.workspace.id}/pages/{self.page.id}/blocks/{self.id}"
    

class Database(models.Model):
    name = models.CharField(max_length=255)
    workspace = models.ForeignKey(Workspace, related_name='databases', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_databases', on_delete=models.SET_NULL, null=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.id = None
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f"/workspaces/{self.workspace.id}/databases/{self.id}"
    
    class Meta:
        verbose_name = "Database"
        verbose_name_plural = "Databases"
        ordering = ['id']
        
        
class DatabaseRow(models.Model):
    database = models.ForeignKey(Database, related_name='rows', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='created_database_rows', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.id = None
        
    def __str__(self):
        return f"Row in {self.database.name}"
    
    def get_absolute_url(self):
        return f"/workspaces/{self.database.workspace.id}/databases/{self.database.id}/rows/{self.id}"
    
    class Meta:
        verbose_name = "Database Row"
        verbose_name_plural = "Database Rows"
        ordering = ['-id']
    

class Property(models.Model):
    PROPERTY_TYPES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('dropdown', 'Dropdown'),
        ('multi_select', 'Multi-Select'),
    ]
    name = models.CharField(max_length=255)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default='text')
    database = models.ForeignKey(Database, related_name='properties', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.id = None
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f"/workspaces/{self.database.workspace.id}/databases/{self.database.id}/properties/{self.id}"
    
    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ['id']
        
        
class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    page = models.ForeignKey(Page, null=True, blank=True, on_delete=models.CASCADE)
    block = models.ForeignKey(Block, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.id = None
        
    def __str__(self):
        return f"Comment by {self.user.username}"
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['-id']
        
        
class ActivityLog(models.Model):
    ACTION_TYPES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
    ]
    user = models.ForeignKey(User, related_name='activity_logs', on_delete=models.CASCADE)
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    action = models.CharField(max_length=255)
    page = models.ForeignKey(Page, null=True, blank=True, on_delete=models.CASCADE)
    block = models.ForeignKey(Block, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.id = None
        
    def __str__(self):
        return f"{self.action.capitalize()} {self.action_type} {self.action}"
    
    class Meta:
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"
        ordering = ['-id']
