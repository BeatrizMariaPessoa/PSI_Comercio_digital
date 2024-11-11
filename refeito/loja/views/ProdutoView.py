from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from loja.models import *
from datetime import timedelta, datetime
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from loja.forms.ProdutoForm import ProdutoCreateForm


# adicione a função que chama a interface de criar produto
# no final do arquivo

def create_produto_view(request, id=None):

    if request.method == 'POST':
        print("postback-create")
   

        form = ProdutoCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/produto")
        else:
            print("FORM INVALIDO!!!!!!!!!!!")
            print(form.errors)
    else:

        form = ProdutoCreateForm()
    
    categorias = Categoria.objects.all()
    fabricantes = Fabricante.objects.all()

    # print(form)
    print(categorias)
    print(fabricantes)
    return render(request, 'produto/produto-create.html', {'categorias': categorias, 'fabricantes': fabricantes, 'form': form}, status=200)
    # Processa o post back gerado pela action
    # if request.method == 'POST':
    #     produto = request.POST.get("Produto")
    #     destaque = request.POST.get("destaque")
    #     promocao = request.POST.get("promocao")
    #     msgPromocao = request.POST.get("msgPromocao")
    #     preco = request.POST.get("preco")
    #     categoria_id = request.POST.get("CategoriaFk")
    #     fabricante_id = request.POST.get("FabricanteFk")
    #     image = request.POST.get("image")
    #     print("postback-create")
    #     print(produto)
    #     print(destaque)
    #     print(promocao)
    #     print(msgPromocao)
    #     print(preco)
    #     print(categoria_id)
    #     print(fabricante_id)
    #     print(image)
    #     try:
    #         obj_produto = Produto()
    #         obj_produto.Produto = produto
    #         obj_produto.destaque = (destaque is not None)
    #         obj_produto.promocao = (promocao is not None)
    #         if msgPromocao is not None:
    #             obj_produto.msgPromocao = msgPromocao
    #         obj_produto.preco = 0
    #         if (preco is not None) and ( preco != ""):
    #             obj_produto.preco = preco
    #             obj_produto.criado_em = timezone.now()
    #             obj_produto.alterado_em = obj_produto.criado_em
    #         # Se for anexado arquivo, salva na pasta e guarda nome no objeto
    #         if request.FILES is not None:
    #             num_files = len(request.FILES.getlist('image'))
    #             if num_files > 0:
    #                 imagefile = request.FILES['image']
    #                 print(imagefile)
    #                 fs = FileSystemStorage()
    #                 filename = fs.save(imagefile.name, imagefile)
    #             if (filename is not None) and (filename != ""):
    #                 obj_produto.image = filename
    #         if categoria_id is not None:
    #             obj_produto.categoria = Categoria.objects.filter(id=categoria_id).first()
    #         if fabricante_id is not None:
    #             obj_produto.fabricante = Fabricante.objects.filter(id=fabricante_id).first()
    #         obj_produto.save()
    #         print("Produto %s salvo com sucesso" % produto)
    #     except Exception as e:
    #         print("Erro inserindo produto: %s" % e)
    #     return redirect("/produto")
    

def details_produto_view(request, id=None):
    # Processa o evento GET gerado pela action
    produtos = Produto.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    print(produto)
    #adicione a lista de fabricantes e categorias no context
    Fabricantes = Fabricante.objects.all()
    Categorias = Categoria.objects.all()
    context = {'produto': produto, 'fabricantes' : Fabricantes, 'categorias' : Categorias}
    return render(request, template_name='produto/produto-details.html', context=context, status=200)

@login_required

def edit_produto_view(request, id=None):
    produtos = Produto.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    Fabricantes = Fabricante.objects.all()
    Categorias = Categoria.objects.all()
    produto = produtos.first()
    print(produto)
    context = {'produto': produto, 'fabricantes' : Fabricantes, 'categorias' : Categorias}
    return render(request, template_name='produto/produto-edit.html', context=context,status=200)


def edit_produto_postback(request, id=None):
    # Processa o post back gerado pela action
    if request.method == 'POST':
        # Salva dados editados
        id = request.POST.get("id")
        produto = request.POST.get("Produto")
        destaque = request.POST.get("destaque")
        promocao = request.POST.get("promocao")
        preco = request.POST.get("preco")
        msgPromocao = request.POST.get("msgPromocao")
        categoria = request.POST.get("CategoriaFk")
        fabricante = request.POST.get("FabricanteFk")
        print("postback")
        print(id)
        print(produto)
        print(destaque)
        print(promocao)
        print(preco)
        print(msgPromocao)
        try:
            obj_produto = Produto.objects.filter(id=id).first()
            obj_produto.Produto = produto
            obj_produto.destaque = (destaque is not None)
            obj_produto.promocao = (promocao is not None)
            obj_produto.fabricante = Fabricante.objects.filter(id=fabricante).first()
            obj_produto.categoria = Categoria.objects.filter(id=categoria).first()
            if msgPromocao is not None:
                obj_produto.msgPromocao = msgPromocao
                obj_produto.save()
                print("Produto %s salvo com sucesso" % produto)
        except Exception as e:
            print("Erro salvando edição de produto: %s" % e)
    return redirect("/produto")

def list_produto_view(request, id=None):
    from loja.models import Produto
    produto = request.GET.get("produto")
    destaque = request.GET.get("destaque")
    promocao = request.GET.get("promocao")
    categoria = request.GET.get("categoria")
    fabricante = request.GET.get("fabricante")
    dias = request.GET.get("dias")
    produtos = Produto.objects.all()
    print(produtos)
    if dias is not None:
        now = timezone.now()
        now = now - timedelta(days = int(dias))
        produtos = produtos.filter(criado_em__gte=now)
    # Adicione para definir o contexto e carregar o template
    context = {'produtos': produtos}
    return render(request, template_name='produto/produto.html',context=context, status=200)

def delete_produto_view(request, id=None):
    # Processa o evento GET gerado pela action
    produtos = Produto.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    print(produto)
    context = {'produto': produto}
    return render(request, template_name='produto/produto-delete.html', context=context, status=200)

# adicione a função que trata o postback da interface de exclusão
def delete_produto_postback(request, id=None):
    # Processa o post back gerado pela action
    if request.method == 'POST':
        # Salva dados editados
        id = request.POST.get("id")
    produto = request.POST.get("Produto")
    print("postback-delete")
    print(id)    
    try:
        Produto.objects.filter(id=id).delete()
        print("Produto %s excluido com sucesso" % produto)
    except Exception as e:
        print("Erro salvando edição de produto: %s" % e)
    return redirect("/produto")