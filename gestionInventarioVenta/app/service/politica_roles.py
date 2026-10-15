"""Quién puede crear/modificar usuarios de qué rol (misma regla del proyecto original, generalizada)."""
from app.model.rol_usuario import RolUsuario


def puede_gestionar(nombre_rol_actor: str, nombre_rol_objetivo: str) -> bool:
    if nombre_rol_actor == RolUsuario.SUPER_USUARIO:
        return nombre_rol_objetivo != RolUsuario.SUPER_USUARIO
    if nombre_rol_actor == RolUsuario.ADMINISTRADOR:
        return nombre_rol_objetivo == RolUsuario.EMPLEADO
    return False
