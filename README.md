# BD Prático - Projeto Django

Este é um projeto prático desenvolvido em **Django** para demonstrar operações fundamentais de desenvolvimento web, incluindo autenticação de usuários, operações CRUD completas e exibição de dados de forma amigável.

## 🚀 Tecnologias Utilizadas

- **Python** e **Django 6**
- **Bootstrap 5** (via `django-bootstrap5`): Para estilização e componentes responsivos (como modais).
- **Django Tables 2** (`django-tables2`): Para renderização de tabelas de dados ricas, com suporte a paginação e links interativos.
- **SQLite3**: Banco de dados relacional (configuração padrão do projeto).

## ✨ Funcionalidades

- **Autenticação de Usuários**: Sistema de login customizado na tela inicial com controle e gestão de sessão, e funcionalidade de logout.
- **Gerenciamento de Pessoas (CRUD completo)**:
  - **Criação (Create)**: Formulários de cadastro baseados em `CreateView`.
  - **Leitura (Read)**: Listagem de registros (modelo `pessoa`) utilizando `django-tables2` com paginação (5 itens por página).
  - **Atualização (Update)**: Edição de dados existentes utilizando `UpdateView`.
  - **Exclusão (Delete)**: Remoção segura de registros integrando `DeleteView` com um Modal de Confirmação do Bootstrap para uma melhor Experiência do Usuário (UX).
- **Tabelas Interativas**: Geração de tabelas de dados com colunas customizadas (links nos textos, botões de ação primária e de perigo).

## 📁 Estrutura do Projeto

- `bdpratico/`: Configurações globais do projeto (`settings.py`, roteamento principal em `urls.py`).
- `exemplo01/`: Aplicação principal (App) onde está concentrada a lógica de negócio atual.
  - `models.py`: Definição do modelo `pessoa` contendo campos como Nome, e-Mail, Fone, Função, Nascimento e Status de Atividade.
  - `views.py`: Contém a lógica de controle, combinando Views baseadas em Classes (CBV) para o CRUD e Views baseadas em Funções (FBV) para páginas estáticas e autenticação.
  - `tables.py`: Configuração da estrutura da tabela de `pessoa` utilizando o `django-tables2`.
- `exemplo02/`: Segunda aplicação (App) baseada em estrutura inicial pronta para futura expansão.
- `templates/`: Diretório base de templates HTML para a renderização das páginas.

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
