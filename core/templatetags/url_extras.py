from django import template

register = template.Library()


@register.filter
def remove_page(url_string):
    params = url_string.split("&")
    filtered_params = [p for p in params if not p.startswith("page=")]
    return "&".join(filtered_params)


#
