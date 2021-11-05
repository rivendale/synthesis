from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def get_paginator(qs, count, page_size, page, paginated_type, **kwargs):
    """
    Function to create custom pagination
    Args:
        qs (obj): queryset
        count (int): objects count
        page_size (int): page size
        page (int): page number
        paginated_type (obj): graphql object type
    Return:
       paginated_type (obj): paginated object type
    """
    p = Paginator(qs, page_size)
    try:
        page_obj = p.page(page)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return paginated_type(
        count=count,
        page=page_obj.number,
        pages=p.num_pages,
        has_next=page_obj.has_next(),
        has_prev=page_obj.has_previous(),
        items=page_obj.object_list,
        **kwargs
    )


def pagination_helper(items, page, page_size, paginatedType, **kwargs):
    count = items.count()
    return get_paginator(items, count, page_size, page, paginatedType, **kwargs)
