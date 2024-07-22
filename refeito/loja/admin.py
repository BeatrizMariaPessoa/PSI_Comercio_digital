from django.contrib import admin

# Register your models here.
class FabricanteAdmin(admin.ModelAdmin):
    # Cria um filtro de hierarquia com datas
    date_hierarchy = 'criado_em'
class ProdutoAdmin(admin.ModelAdmin):
    date_hierarchy = 'criado_em'
    list_display = ('Produto', 'destaque', 'promocao', 'msgPromocao','preco', 'categoria',)
    fields = ('Produto', 'destaque', 'promocao', 'msgPromocao', 'preco', 'categoria',)
    search_fields = ('Produto',)
    # exclude = ('msgPromocao',)
    # exclude ta em comentario pra n entrar em conflito com o fields
    empty_value_display = 'Vazio'

from .models import * #imporata nossos models
admin.site.register(Fabricante, FabricanteAdmin) #adiciona a interface do adm
admin.site.register(Categoria)
admin.site.register(Produto, ProdutoAdmin)