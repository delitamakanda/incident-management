from ninja.pagination import paginate, PaginationBase
from ninja import Schema
from typing import List, Any

class CustomPagination(PaginationBase):
    class Input(Schema):
        skip: int

    class Output(Schema):
        total: int
        items: List[Any]
        per_page: int
    
    def paginate_queryset(self, queryset, pagination: Input, **params):
        skip = pagination.skip
        return {
            'items': queryset[skip:skip + 5],
            'per_page': 5,
            'total': queryset.count(),
        }