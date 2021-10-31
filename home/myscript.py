from .models import Coisa, Grupo, GrupoCell
from django.contrib import auth


def grupos(request, nosQuaisFuiAceito = False):
    user = auth.get_user(request)
    grupos = []
    if nosQuaisFuiAceito:
        cells = GrupoCell.objects.filter(email = user.email, aproved=True)
    else:
        cells = GrupoCell.objects.filter(email = user.email)

    for cell in cells:
        grupos.append(cell.parent)

    grupos = set(grupos)
    return grupos