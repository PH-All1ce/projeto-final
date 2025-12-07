from django import template

register = template.Library()


@register.filter
def remove_page(url_string):  # filtro pra tirar o page da url
    params = url_string.split("&")
    filtered_params = [p for p in params if not p.startswith("page=")]
    return "&".join(filtered_params)


# basicamente serve pra remover o page=num da pagina e manter os filtros ao trocar de pagina
