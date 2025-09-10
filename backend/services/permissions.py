from typing import Iterable
from functools import wraps
from django.shortcuts import redirect
from rest_framework.exceptions import PermissionDenied
from .roles import UserRole


def has_roles(user, roles: Iterable[str]) -> bool:
    """Retorna True se o usuário for superuser ou possuir uma role permitida."""
    user_role = getattr(user, 'role', None)
    # Aceita comparar tanto com strings quanto com UserRole
    role_values = {r.value if isinstance(r, UserRole) else r for r in roles}
    return user_role in role_values


def require_roles(user, roles: Iterable[str]) -> None:
    """Lança PermissionDenied se o usuário não possuir uma das roles informadas."""
    if not has_roles(user, roles):
        raise PermissionDenied('Você não tem permissão para acessar este recurso.')

def require_roles_or_redirect(request, roles: Iterable[str]):
    """Valida roles; se falhar, redireciona para página de acesso negado."""
    try:
        require_roles(request.user, roles)
        return None
    except PermissionDenied:
        return redirect('front:forbidden')

def require_roles_view(roles: Iterable[str]):
    """Decorator para views Django: valida roles e redireciona para 'front:forbidden' ao falhar."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            try:
                require_roles(request.user, roles)
            except PermissionDenied:
                return redirect('front:forbidden')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


