from rolepermissions.roles import AbstractUserRole

class Gerente(AbstractUserRole):
    available_permissions = {
        'adicionar_veiculo': True,
        'editar_veiculo': True,
        'remover_veiculo': True,
        'visualizar_veiculo': True,
        'adicionar_usuario': True,
        'remover_usuario': True,
        'editar_usuario': True,
    }

class UsuarioComum(AbstractUserRole):
    available_permissions = {
        'visualizar_veiculo': True,
    }