from django import template

register = template.Library()

# Create a custom filter to retrieve dictionary item by key
@register.filter(name='get_item')
def get_item(dictionary, key):
    """Get item from dictionary by key."""
    try:
        return dictionary.get(key)
    except (AttributeError, TypeError):
        return None
