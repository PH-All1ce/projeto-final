# AutoCenter, uma loja de carros

Projeto que utiliza o framework django para dar origem a uma loja de veículos. A loja possui um estoque pré-definido, que pode ser consumido pelos clientes (usuários comuns), e editado pelos vendedores (usuário responsável pelo gerenciamento da loja). As permissões de vendedor são transferidas para o usuário através do painel admin do django.

# Instruções de instalação e configuração

## Pré-requisitos

- Windows 10/11
- [Python 3.11+](https://www.python.org/downloads/) (marque a opção “Add Python to PATH” ao instalar)
- Git (necessário para clonar o repositório)

## Passo a passo (Windows)

1. **Clonar o projeto**
   ```powershell
   git clone https://github.com/PH-All1ce/projeto-final
   
   
2. **Criar o ambiente virtual**
   ```powershell
   python -m venv venv
   ```

3. **Ativar o ambiente virtual**
   ```powershell
   .\venv\Scripts\Activate
   ```

4. **Instalar dependências**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Aplicar migrações**
   ```powershell
   python manage.py migrate
   ```

6. **Criar superusuário (necessário para utilizar /admin e habilitar as permissões de vendedor para o usuário)**
   ```powershell
   python manage.py createsuperuser
   ```

7. **Executar o servidor**
   ```powershell
   python manage.py runserver
   ```

8. **Abrir o app**
   - Interface principal: http://127.0.0.1:8000/
   - Admin Django: http://127.0.0.1:8000/admin/

## Variáveis úteis

- Parar o servidor: `Ctrl + C` no terminal.
- Desativar o ambiente virtual: `deactivate`.


# Manual do usuário

 **Para o usuário cliente:**
Assim que o projeto for carregado, o usuário terá acesso a listagem de todos os veículos disponíveis, podendo navegar por todas as páginas e realizar a filtragem de acordo com os parâmetros disponíveis (nome do veículo, ano mínimo de lançamento, preço máximo e quilometragem máxima).
O detalhamento e compra dos veículos só poderão ser realizadas após o usuário criar uma conta e estar logado nela (utilize os campos do canto superior direito da tela).
Após a criação da conta o cliente poderá: 
- Adquirir os veículos disponíveis (dependendo do saldo);
- Consultar a lista de veículos comprados;
- Ter acesso aos seus dados anteriormente cadastrados;
- Realizar a edição de parte desses dados (e-mail e endereço);
- Deletar a sua própria conta.

 **Para o usuário vendedor:**
O vendedor deve criar a sua conta normalmente, como um cliente, e em seguida solicitar a promoção ao posto de vendedor para um dos donos da loja.
No painel de administrador do Django, o dono, com o seu superusuário devidamente logado, poderá promover aqueles que desejar para o cargo de "Vendedor".
Após receber os privilégios de vendedor, o usuário, além de contar com todas as permissões de cliente, receberá também o acesso ao "Painel Vendedor", localizado no canto superior direito da tela; lá, o vendedor terá acesso a gerencia da loja, podendo: 
- Adicionar veículos; 
- Editar informações que estiverem incorretas;
- Remover os veículos da loja que estiverem com algum problema.
(Os mesmos elementos de busca e paginação disponíveis para o cliente também estão disponíveis para o vendedor no "Painel Vendedor", facilitando o gerenciamento.)