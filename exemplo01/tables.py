import django_tables2 as tables
from django_tables2.utils import A

from .models import pessoa


class pessoa_table(tables.Table):
    nome = tables.LinkColumn("pessoa_update_alias", args=[A("pk")])
    email = tables.LinkColumn("pessoa_update_alias", args=[A("pk")])
    fone = tables.LinkColumn("pessoa_update_alias", args=[A("pk")])
    funcao = tables.LinkColumn("pessoa_update_alias", args=[A("pk")])
    nascimento = tables.LinkColumn("pessoa_update_alias", args=[A("pk")])
    ativo = tables.Column()
    editar = tables.TemplateColumn(
        template_code='<a href="{% url \'pessoa_update_alias\' record.pk %}" class="btn btn-primary btn-sm">Editar</a>',
        verbose_name="Editar"
    )
    excluir = tables.TemplateColumn(
        template_code='<button class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#deleteModal" data-bs-id="{{ record.pk }}" data-bs-nome="{{ record.nome }}">Excluir</button>',
        verbose_name="Excluir"
    )
    class Meta:
        model = pessoa
        attrs = {"class": "table thead-light table-striped table-hover"}
        template_name = "django_tables2/bootstrap4.html"
        fields = ('nome', 'email', 'fone', 'funcao', 'nascimento', 'ativo', 'editar', 'excluir')