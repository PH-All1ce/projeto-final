Loja de carros, Douglas Paulino e Pedro Henrique

requirements:
Python 3.11, Django 5.0
SQLite3 (para desenvolvimento)
HTML5, CSS3, JavaScript (se aplicável)
Git, GitHub

#Para Executar o Projeto


Clone o repositório:
    git clone https://github.com/PH-All1ce/projeto-fin

Crie e ative um ambiente virtual:
    python -m venv venv
    .\venv\Scripts\activate

Instale as dependências:
    pip install -r requirements.txt

Aplique as migrações do banco de dados:
    python manage.py migrate

Crie um superusuário para acessar o painel de admin:
    python manage.py createsuperuser

Execute o servidor de desenvolvimento:
    python manage.py runserver

Execute `http://127.0.0.1:8000/`

Sobre a insersão do usuário customizado:

Para deixar a modelagem dos tipos de usuário mais fácil, criamos um app chamado "users", que foi devidamente inserido nas configurações do projeto (settings.py);

Utilizamos o AbstracUser como modelo de usuário customizado em users/models.py (informamos ao Django para utilizar esse modelo customizado em settings.py);

Adicionamos novos campos ao modelo de usuário customizado (CPF, email e outros);

Implementamos as letas de login e logout através de modelos fornecidos pelo próprio django;

As URLs foram devidamente configuradas (em urls.py, utilizando include);

As redirects também foram alteradas no settings.py (LOGIN_REDIRECT_URL e LOGOUT_REDIRECT_URL);

Criamos os grupos de usuários com suas devidas permissões. Até o presente momento, pensamos em apenas 2 grupos: Cliente e Vendedor (O cliente pode fazer apenas ações básicas de interação, enquanto o Vendedor pode fazer tudo relacionado a administração);

Alteramos as views para garantir que os usuários comuns (Clientes) não tenham acesso a determinadas funções dentro da aplicação (funções de administração).