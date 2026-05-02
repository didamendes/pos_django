import logging
import os
import random

import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from sklearn.metrics import (
    accuracy_score,
    auc,
    confusion_matrix,
    precision_recall_curve,
    roc_curve,
)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier

from .models import dados

logger = logging.getLogger(__name__)

# Constantes
MODEL_FILENAME = 'knn_model.pkl'  # Caminho do arquivo onde o modelo será salvo
GRUPO_MAP = {'Controle': -1, 'Experimental': 1}  # Mapeamento da variável alvo

# Lista de campos das características (features) do dataset
FEATURE_FIELDS = [
    'mdw', 'latw', 'tmcw', 'racw', 'araw', 'mcw', 'psdsw', 's6w',
    'mdr', 'latr', 'tmcr', 'racr', 'arar', 'mcr', 'psdsr', 's6r',
    'mdg', 'latg', 'tmcg', 'racg', 'arag', 'mcg', 'psdsg', 's6g',
    'mdwb', 'latb', 'tmcb', 'racb', 'arab', 'mcb', 'psdsb', 's6b',
]


# =============================================================================
# Funções auxiliares
# =============================================================================

def _carregar_dados_do_banco():
    """Carrega os dados do banco e retorna um DataFrame."""
    queryset = dados.objects.all()
    return pd.DataFrame(list(queryset.values()))


def _separar_features_target(df, mapear_grupo=False):
    """Separa features (X) e target (y) do DataFrame.

    'grupo' é a variável alvo e o restante são as características (features).
    """
    X = df.drop(columns=['grupo', 'id'])  # Variáveis independentes
    y = df['grupo']  # Variável dependente (target)
    if mapear_grupo:
        y = y.map(GRUPO_MAP)
    return X, y


def _carregar_modelo():
    """Carrega o modelo KNN salvo em disco."""
    return joblib.load(MODEL_FILENAME)


def _to_float(valor):
    """Converte um valor para float de forma segura."""
    if valor is None:
        return 0.0
    valor = str(valor).strip()
    if valor == '':
        return 0.0
    valor = valor.replace(',', '.')
    try:
        return float(valor)
    except ValueError:
        return 0.0


# =============================================================================
# Views
# =============================================================================

def index(request):
    return HttpResponse("AGORA EH EXEMPLO 02.")


def ia_import(request):
    return render(request, 'ia_import.html')


def ia_import_save(request):
    if request.method != 'POST' or not request.FILES.get('arq_upload'):
        return redirect('ia_import')

    fss = FileSystemStorage()
    upload = request.FILES['arq_upload']
    file1 = fss.save(upload.name, upload)
    file_url = fss.url(file1)

    dados.objects.all().delete()

    with open(file1, 'r') as file2:
        for i, row in enumerate(file2):
            if i == 0:
                continue  # Pular cabeçalho
            row = row.replace(',', '.')
            cols = row.split(';')
            dados.objects.create(
                grupo=cols[0],
                mdw=float(cols[1]), latw=float(cols[2]),
                tmcw=float(cols[3]), racw=float(cols[4]), araw=float(cols[5]),
                mcw=float(cols[6]), psdsw=float(cols[7]), s6w=float(cols[8]),
                mdr=float(cols[9]), latr=float(cols[10]), tmcr=float(cols[11]),
                racr=float(cols[12]), arar=float(cols[13]), mcr=float(cols[14]),
                psdsr=float(cols[15]), s6r=float(cols[16]),
                mdg=float(cols[17]), latg=float(cols[18]), tmcg=float(cols[19]),
                racg=float(cols[20]), arag=float(cols[21]), mcg=float(cols[22]),
                psdsg=float(cols[23]), s6g=float(cols[24]),
                mdwb=float(cols[25]), latb=float(cols[26]), tmcb=float(cols[27]),
                racb=float(cols[28]), arab=float(cols[29]), mcb=float(cols[30]),
                psdsb=float(cols[31]), s6b=float(cols[32]),
            )

    os.remove(file_url.replace("/", ""))
    return redirect('ia_import_list')


def ia_import_list(request):
    data = {
        'dados': dados.objects.all(),
    }
    return render(request, 'ia_import_list.html', data)


def ia_knn_treino(request):
    logger.info("Iniciando treinamento KNN...")

    # Carregar dados do banco
    df = _carregar_dados_do_banco()
    X, y = _separar_features_target(df)
    logger.info("Dados carregados: %s registros", len(df))

    # Dividir em treino (70%), teste (15%) e validação (15%)
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, random_state=42,
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=42,
    )

    logger.info(
        "Split: treino=%d, teste=%d, validação=%d",
        X_train.shape[0], X_test.shape[0], X_val.shape[0],
    )

    # Instanciando o KNN e definindo o grid de parâmetros
    param_grid = {
        'n_neighbors': [3, 5, 7, 9],  # Exemplos de valores possíveis
        'weights': ['uniform', 'distance'],  # Tipos de pesos
        'metric': ['euclidean', 'manhattan'],  # Tipos de distância
    }

    # Usando o GridSearchCV para encontrar os melhores parâmetros
    grid_search = GridSearchCV(
        estimator=KNeighborsClassifier(),
        param_grid=param_grid,
        cv=5, verbose=2, n_jobs=-1,
    )
    # Treinando o modelo com os dados de treino
    grid_search.fit(X_train, y_train)

    # Melhor conjunto de parâmetros
    best_knn = grid_search.best_estimator_
    logger.info("Melhores parâmetros encontrados: %s", grid_search.best_params_)

    # Previsões e avaliação do modelo (Accuracy)
    # Acurácia no conjunto de validação
    val_accuracy = accuracy_score(y_val, best_knn.predict(X_val))
    # Acurácia no conjunto de teste
    test_accuracy = accuracy_score(y_test, best_knn.predict(X_test))

    # Salvar o modelo treinado com o joblib
    joblib.dump(best_knn, MODEL_FILENAME)
    logger.info("Modelo salvo em: %s", MODEL_FILENAME)

    data = {
        'dataset': X_train.shape,
        'treino': X_train.shape[0],
        'teste': X_test.shape[0],
        'validacao': X_val.shape[0],
        'best': grid_search.best_params_,
        'acc_validacao': round(val_accuracy * 100, 2),
        'acc_teste': round(test_accuracy * 100, 2),
        'file': MODEL_FILENAME,
    }
    return render(request, 'ia_knn_treino.html', data)


def ia_knn_matriz(request):
    # Carregar dados do banco
    df = _carregar_dados_do_banco()
    X, y = _separar_features_target(df)

    # Carregar o modelo treinado
    best_knn = _carregar_modelo()

    # Gerar previsões e matriz de confusão
    y_pred = best_knn.predict(X)
    cm = confusion_matrix(y, y_pred)

    data = {
        'matrix': cm.tolist(),
        'labels': np.unique(y).tolist(),
    }
    return render(request, 'ia_knn_matriz.html', data)


def ia_knn_roc(request):
    # Carregar dados do banco
    df = _carregar_dados_do_banco()
    X, y = _separar_features_target(df, mapear_grupo=True)

    # Carregar o modelo treinado
    best_knn = _carregar_modelo()

    # Gerar probabilidades e curva ROC
    y_pred_prob = best_knn.predict_proba(X)[:, 1]
    fpr, tpr, _ = roc_curve(y, y_pred_prob)
    roc_auc = auc(fpr, tpr)

    # Criar gráfico com Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr, mode='lines',
        name=f'ROC Curve (AUC = {roc_auc:.2f})',
        line=dict(color='blue'),
    ))
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1], mode='lines',
        name='Random Classifier',
        line=dict(dash='dash', color='gray'),
    ))
    fig.update_layout(
        title='Curva ROC',
        xaxis_title='Taxa de Falsos Positivos (FPR)',
        yaxis_title='Taxa de Verdadeiros Positivos (TPR)',
        showlegend=True,
    )

    graph = fig.to_html(full_html=False)
    return render(request, 'ia_knn_roc.html', {'graph': graph})


def ia_knn_recall(request):
    # Carregar dados do banco
    df = _carregar_dados_do_banco()
    X, y = _separar_features_target(df, mapear_grupo=True)

    # Carregar o modelo treinado
    best_knn = _carregar_modelo()

    # Gerar probabilidades e curva Precision-Recall
    y_pred_prob = best_knn.predict_proba(X)[:, 1]
    precision, recall, _ = precision_recall_curve(y, y_pred_prob)
    pr_auc = auc(recall, precision)

    # Criar gráfico com Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=recall, y=precision, mode='lines',
        name=f'Precision-Recall Curve (AUC = {pr_auc:.2f})',
        line=dict(color='blue'),
    ))
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 0], mode='lines',
        name='Random Classifier',
        line=dict(dash='dash', color='gray'),
    ))
    fig.update_layout(
        title='Curva Precision-Recall',
        xaxis_title='Recall',
        yaxis_title='Precision',
        showlegend=True,
    )

    graph = fig.to_html(full_html=False)
    return render(request, 'ia_knn_recall.html', {'graph': graph})


def ia_knn_inferencia(request):
    # Preencher valores conforme o método da requisição
    valores = {}
    if request.method == 'GET':
        for campo in FEATURE_FIELDS:
            valores[campo] = round(random.uniform(0, 100), 2)
    else:
        for campo in FEATURE_FIELDS:
            valores[campo] = _to_float(request.POST.get(campo))

    # Realizar inferência no POST
    resultado = None
    erro = None
    if request.method == 'POST':
        df = pd.DataFrame([valores])
        if not os.path.exists(MODEL_FILENAME):
            erro = 'Modelo não encontrado. Execute o treino primeiro.'
        else:
            modelo = _carregar_modelo()
            resultado = modelo.predict(df)[0]

    return render(request, 'ia_knn_inferencia.html', {
        'valores': valores,
        'resultado': resultado,
        'erro': erro,
    })