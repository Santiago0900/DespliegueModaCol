from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from clientes_app.models import CategoriaModel
import json


from core.use_cases.categorias.crear_categoria import CrearCategoriaUseCase
from core.use_cases.categorias.listar_categorias import ListarCategoriasUseCase
from core.use_cases.categorias.filtrar_categorias import FiltrarCategoriasUseCase
from core.use_cases.categorias.obtener_categoria import ObtenerCategoriaUseCase
from core.use_cases.categorias.actualizar_categoria import ActualizarCategoriaUseCase
from core.use_cases.categorias.eliminar_categoria import EliminarCategoriaUseCase
from core.use_cases.categorias.activar_categoria import ActivarCategoriaUseCase
from infrastructure.api.forms.categoria_form import CategoriaForm
from infrastructure.persistence.repositories.django_categoria_repository import DjangoCategoriaRepository
from infrastructure.api.utils.context import base_context




def categoria_to_dict(categoria):
    return {
        "id": categoria.id,
        "tipoCategoria": categoria.tipo_categoria,
        "activo": categoria.activo,
    }


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_categorias(request):
    repo = DjangoCategoriaRepository()

    if request.method == "GET":
        categorias = ListarCategoriasUseCase(repo).execute()
        return JsonResponse([categoria_to_dict(c) for c in categorias], safe=False)

    try:
        data = json.loads(request.body)
        categoria = CrearCategoriaUseCase(repo).execute({
            "tipo_categoria": data.get("tipoCategoria"),
            "activo": data.get("activo", True),
        })
        return JsonResponse(categoria_to_dict(categoria), status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_categoria_detalle(request, id):
    repo = DjangoCategoriaRepository()

    try:
        if request.method == "GET":
            categoria = ObtenerCategoriaUseCase(repo).execute(id)
            return JsonResponse(categoria_to_dict(categoria))

        if request.method == "PUT":
            data = json.loads(request.body)
            categoria = ActualizarCategoriaUseCase(repo).execute(id, {
                "tipo_categoria": data.get("tipoCategoria"),
                "activo": data.get("activo", True),
            })
            return JsonResponse(categoria_to_dict(categoria))

        if request.method == "DELETE":
            EliminarCategoriaUseCase(repo).execute(id)
            return JsonResponse({}, status=204)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def listar_categorias_view(request):
    repo = DjangoCategoriaRepository()
    tipo_categoria = request.GET.get("tipoCategoria")

    if tipo_categoria:
        categorias = FiltrarCategoriasUseCase(repo).execute(tipo_categoria=tipo_categoria)
    else:
        categorias = ListarCategoriasUseCase(repo).execute()

    return render(request, "categorias/list.html", {
        "categoriasList": categorias,
        **base_context(request),
    })


def crear_categoria_view(request):
    form = CategoriaForm(initial={"activo": True})
    return render(request, "categorias/form.html", {
        "form": form,
        "categoria_id": None,
        **base_context(request),
    })


def editar_categoria_view(request, id):
    try:
        obj = CategoriaModel.objects.get(id=id)
    except CategoriaModel.DoesNotExist:
        raise RuntimeError("Categoría no encontrada")

    form = CategoriaForm(
        instance=obj,
        initial={"id": obj.id, "activo": obj.activo}
    )

    return render(request, "categorias/form.html", {
        "form": form,
        "categoria_id": id,
        **base_context(request),
    })

def guardar_categoria_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    repo = DjangoCategoriaRepository()
    categoria_id = request.POST.get("id") or None
    instance = None

    if categoria_id:
        try:
            instance = CategoriaModel.objects.get(id=categoria_id)
        except CategoriaModel.DoesNotExist:
            instance = None

    form = CategoriaForm(request.POST, instance=instance)

    if not form.is_valid():
        return render(request, "categorias/form.html", {
            "form": form,
            "categoria_id": categoria_id,
            **base_context(request),
        })

    data = {
        "tipo_categoria": form.cleaned_data["tipo_categoria"],
        "activo": form.cleaned_data.get("activo", True),
    }

    try:
        if categoria_id:
            ActualizarCategoriaUseCase(repo).execute(int(categoria_id), data)
        else:
            CrearCategoriaUseCase(repo).execute(data)

        return redirect("categorias_list")

    except Exception as e:
        form.add_error(None, str(e))
        return render(request, "categorias/form.html", {
            "form": form,
            "categoria_id": categoria_id,
            **base_context(request),
        })


def eliminar_categoria_view(request, id):
    repo = DjangoCategoriaRepository()
    EliminarCategoriaUseCase(repo).execute(id)
    return redirect("categorias_list")


def activar_categoria_view(request, id):
    repo = DjangoCategoriaRepository()
    ActivarCategoriaUseCase(repo).execute(id)
    return redirect("categorias_list")