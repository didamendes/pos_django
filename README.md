# BD Prático - Projeto Django

Este é um projeto prático desenvolvido em **Django** para demonstrar operações fundamentais de desenvolvimento web, incluindo autenticação de usuários, operações CRUD completas e exibição de dados de forma amigável.

## 🚀 Tecnologias Utilizadas

- **Python** e **Django 6**
- **Bootstrap 5** (via `django-bootstrap5`): Para estilização e componentes responsivos (como modais).
- **Django Tables 2** (`django-tables2`): Para renderização de tabelas de dados ricas, com suporte a paginação e links interativos.
- **SQLite3**: Banco de dados relacional (configuração padrão do projeto).

## ✨ Funcionalidades

- **Autenticação de Usuários**: Sistema de login customizado na tela inicial com controle e gestão de sessão, e funcionalidade de logout.
- **Controle de Permissões (Mixin Genérico)**: Mixin reutilizável (`PermissionRequiredGenericMixin`) para verificação de permissões em Class-Based Views, permitindo restringir o acesso com mensagens personalizadas de forma prática e DRY.
- **Gerenciamento de Pessoas (CRUD completo)**:
  - **Criação (Create)**: Formulários de cadastro baseados em `CreateView` e também via `ModelForm` customizado (`PessoaForm`) com persistência direta no banco de dados.
  - **Leitura (Read)**: Listagem de registros (modelo `pessoa`) utilizando `django-tables2` com paginação (5 itens por página) e listagem estilizada com tabela Bootstrap (destaque em negrito para registros ativos).
  - **Atualização (Update)**: Edição de dados existentes utilizando `UpdateView`.
  - **Exclusão (Delete)**: Remoção segura de registros integrando `DeleteView` com um Modal de Confirmação do Bootstrap para uma melhor Experiência do Usuário (UX).
- **Tabelas Interativas**: Geração de tabelas de dados com colunas customizadas (links nos textos, botões de ação primária e de perigo).
- **Modelos Relacionais**:
  - `procedimento`: Cadastro de procedimentos com Descrição, CID e Valor.
  - `procedimento_executado`: Registro de procedimentos executados por pessoa, com relacionamento via `ForeignKey`, campo de Observação e Quantidade.
- **Herança de Templates**: Utilização de um template `base.html` centralizado que carrega Bootstrap e define blocos (`title`, `content`, `extra_head`, `extra_js`) para eliminar repetição de código HTML entre as páginas.
- **Django Admin Customizado**:
  - Listagem personalizada com campo calculado de Idade.
  - Actions customizadas para habilitar/desabilitar registros em massa.
  - Registro dos modelos `procedimento` e `procedimento_executado` no admin.

## 📁 Estrutura do Projeto

- `bdpratico/`: Configurações globais do projeto (`settings.py`, roteamento principal em `urls.py`).
- `exemplo01/`: Aplicação principal (App) onde está concentrada a lógica de negócio atual.
  - `models.py`: Definição dos modelos `pessoa`, `procedimento` e `procedimento_executado` com relacionamentos entre eles.
  - `views.py`: Contém a lógica de controle, combinando Views baseadas em Classes (CBV) para o CRUD, Views baseadas em Funções (FBV) para páginas estáticas e autenticação, e o `PermissionRequiredGenericMixin` para controle de acesso.
  - `forms.py`: Formulário `PessoaForm` baseado em `ModelForm` com widget de data customizado.
  - `tables.py`: Configuração da estrutura da tabela de `pessoa` utilizando o `django-tables2`.
  - `admin.py`: Customizações do Django Admin, incluindo actions em massa e campo calculado de idade.
- `exemplo02/`: Segunda aplicação (App) baseada em estrutura inicial pronta para futura expansão.
- `templates/`: Diretório base contendo o template `base.html` para herança de templates.

## 📄 Páginas do Projeto

| Rota | Template | Descrição |
|------|----------|-----------|
| `/` | `index.html` | Tela de Login (autenticação de usuários) |
| `/pagina0/` | `pagina0.html` | Página estática de exemplo |
| `/pagina1/` | `pagina1.html` | Hello World com imagem estática |
| `/pagina2/` | `pagina2.html` | Listagem simples de pessoas (loop `for`) |
| `/pagina3/` | `pagina3.html` | Página com estilos Bootstrap e tabela com cards |
| `/pagina4/` | `pagina4.html` | Formulário POST manual (sem ModelForm) |
| `/pagina5/` | `pagina5.html` | Formulário com `ModelForm` e persistência no banco |
| `/pagina6/` | `pagina6.html` | Listagem estilizada com tabela Bootstrap (negrito para ativos) |
| `/menu/` | `pessoa_menu.html` | Menu principal com tabela paginada e ações CRUD |
| `/pessoa_create/` | `pessoa_form.html` | Cadastro de pessoa via `CreateView` |
| `/pessoa_list/` | `pessoa_list.html` | Listagem de pessoas ativas (com verificação de permissão) |
| `/pessoa_update/<id>/` | `pessoa_form.html` | Edição de pessoa via `UpdateView` |
| `/pessoa_delete/<id>/` | `pessoa_delete.html` | Exclusão de pessoa com modal de confirmação |

## ⚙️ Como Executar o Projeto Localmente

1. **Acesse a pasta do projeto**:
   ```bash
   cd bdpratico
   ```

2. **Crie e ative um ambiente virtual (Altamente Recomendado)**:
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências da aplicação**:
   Instale os pacotes principais utilizados no projeto. 
   ```bash
   pip install django django-bootstrap5 django-tables2
   ```

4. **Realize as migrações do banco de dados**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crie um superusuário**:
   Você precisará de um usuário para realizar o login no sistema.
   ```bash
   python manage.py createsuperuser
   ```

6. **Inicie o servidor local de desenvolvimento**:
   ```bash
   python manage.py runserver
   ```

7. **Acesse no navegador**:
   Abra `http://127.0.0.1:8000/` para visualizar o sistema em funcionamento e insira as credenciais do superusuário criado para acessar.

---
