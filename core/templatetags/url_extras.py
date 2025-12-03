from django import template

register = template.Library()


@register.filter
def remove_page(url_string):
    """
    Remove o parâmetro 'page' de uma string de parâmetros de URL (query string).
    Isso é crucial para manter os filtros ao paginar.
    """
    params = url_string.split("&")
    filtered_params = [p for p in params if not p.startswith("page=")]
    return "&".join(filtered_params)
