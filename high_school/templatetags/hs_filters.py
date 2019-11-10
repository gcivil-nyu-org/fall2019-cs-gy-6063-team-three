from django import template

register = template.Library()


@register.filter(name="split_string")
def split_string(val, arg):
    if arg in val:
        splits = str(val).split(arg)
        return splits[1]
