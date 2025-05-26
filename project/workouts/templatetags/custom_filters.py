from django import template

register = template.Library()

@register.filter
def get_item(container, key):
    if hasattr(container, 'get'):
        return container.get(key)
    # fallback for string or list: try index if key is int
    try:
        return container[int(key)]
    except (IndexError, ValueError, TypeError):
        return None
