# BD Prático - Projeto Django

Este é um projeto prático desenvolvido em **Django** para demonstrar operações fundamentais de desenvolvimento web, incluindo autenticação de usuários, operações CRUD completas, exibição de dados de forma amigável e um módulo de **Machine Learning** com o algoritmo KNN.

## 🚀 Tecnologias Utilizadas

- **Python** e **Django 6**
- **Bootstrap 5** (via `django-bootstrap5`): Para estilização e componentes responsivos (como modais).
- **Django Tables 2** (`django-tables2`): Para renderização de tabelas de dados ricas, com suporte a paginação e links interativos.
- **Scikit-learn**: Biblioteca de Machine Learning utilizada para o algoritmo KNN (`KNeighborsClassifier`), `GridSearchCV`, e métricas de avaliação.
- **Pandas** e **NumPy**: Manipulação e processamento de dados tabulares.
- **Plotly**: Geração de gráficos interativos (Curva ROC e Precision-Recall).
- **Joblib**: Serialização e persistência do modelo treinado em disco.
- **SQLite3**: Banco de dados relacional (configuração padrão do projeto).

## ✨ Funcionalidades

### 📋 Módulo Web (exemplo01)

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

### 🤖 Módulo de Machine Learning — KNN (exemplo02)

- **Importação de Dataset**: Upload de arquivos CSV (`;` como delimitador) com persistência dos dados no modelo `dados` do banco de dados.
- **Treinamento do Modelo KNN**:
  - Divisão dos dados em **Treino (70%)**, **Teste (15%)** e **Validação (15%)**.
  - Otimização automática de hiperparâmetros via `GridSearchCV` (nº de vizinhos, tipo de peso, métrica de distância).
  - Exibição dos melhores parâmetros encontrados e acurácia nos conjuntos de validação e teste.
  - Persistência do modelo treinado em disco com `joblib` (`knn_model.pkl`).
- **Métricas de Avaliação**:
  - **Matriz de Confusão**: Visualização da performance do modelo com tabela de classificação.
  - **Curva ROC**: Gráfico interativo (Plotly) da Taxa de Verdadeiros Positivos vs. Falsos Positivos, com cálculo da AUC.
  - **Curva Precision-Recall**: Gráfico interativo (Plotly) de Precisão vs. Recall, com cálculo da AUC.
- **Inferência (Predição)**: Formulário com 32 features para realizar predições em tempo real com o modelo treinado, com valores aleatórios pré-preenchidos no GET para facilitar testes.
- **Código Limpo e Organizado**: Funções auxiliares extraídas (`_carregar_dados_do_banco`, `_separar_features_target`, `_carregar_modelo`, `_to_float`), constantes centralizadas e logging configurado.

## 📁 Estrutura do Projeto

- `bdpratico/`: Configurações globais do projeto (`settings.py`, roteamento principal em `urls.py`).
- `exemplo01/`: Aplicação principal (App) — módulo Web com CRUD e autenticação.
  - `models.py`: Definição dos modelos `pessoa`, `procedimento` e `procedimento_executado` com relacionamentos entre eles.
  - `views.py`: Contém a lógica de controle, combinando Views baseadas em Classes (CBV) para o CRUD, Views baseadas em Funções (FBV) para páginas estáticas e autenticação, e o `PermissionRequiredGenericMixin` para controle de acesso.
  - `forms.py`: Formulário `PessoaForm` baseado em `ModelForm` com widget de data customizado.
  - `tables.py`: Configuração da estrutura da tabela de `pessoa` utilizando o `django-tables2`.
  - `admin.py`: Customizações do Django Admin, incluindo actions em massa e campo calculado de idade.
- `exemplo02/`: Aplicação de **Machine Learning** (KNN) — importação de dados, treinamento, métricas e inferência.
  - `models.py`: Modelo `dados` com 32 features numéricas (Float) e campo `grupo` (variável alvo: Controle/Experimental).
  - `views.py`: Views para importação de CSV, treinamento KNN com `GridSearchCV`, geração de Matriz de Confusão, Curva ROC, Curva Precision-Recall e inferência em tempo real.
  - `urls.py`: Roteamento das 8 views do módulo de IA.
  - `templates/`: 7 templates específicos para o fluxo de Machine Learning.
- `templates/`: Diretório base contendo o template `base.html` para herança de templates.
- `knn_model.pkl`: Arquivo do modelo KNN treinado, serializado com `joblib`.
- `Framework-aula-5-ml.csv`: Dataset de exemplo para importação no módulo de IA.

## 📄 Páginas do Projeto

### Módulo Web (exemplo01)

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

### Módulo de Machine Learning (exemplo02)

| Rota | Template | Descrição |
|------|----------|-----------|
| `/exemplo02/` | — | Página inicial do módulo (resposta HTTP simples) |
| `/exemplo02/ia_import` | `ia_import.html` | Upload de arquivo CSV com o dataset |
| `/exemplo02/ia_import_save` | — | Processamento e persistência do CSV no banco |
| `/exemplo02/ia_import_list` | `ia_import_list.html` | Listagem dos dados importados |
| `/exemplo02/ia_knn_treino` | `ia_knn_treino.html` | Treinamento do KNN com GridSearchCV e exibição de resultados |
| `/exemplo02/ia_knn_matriz` | `ia_knn_matriz.html` | Matriz de Confusão do modelo treinado |
| `/exemplo02/ia_knn_roc` | `ia_knn_roc.html` | Gráfico interativo da Curva ROC (Plotly) |
| `/exemplo02/ia_knn_recall` | `ia_knn_recall.html` | Gráfico interativo da Curva Precision-Recall (Plotly) |
| `/exemplo02/ia_knn_inferencia` | `ia_knn_inferencia.html` | Formulário de inferência com 32 features e predição em tempo real |

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
   pip install django django-bootstrap5 django-tables2 scikit-learn pandas numpy plotly joblib
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
   - `http://127.0.0.1:8000/` — Sistema principal (login e CRUD)
   - `http://127.0.0.1:8000/exemplo02/ia_import` — Módulo de Machine Learning

---
