# quadros/views.py

from quadros.models import Pictures
from quadros.forms import PicturesForm
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages

import google.generativeai as genai
from django.conf import settings
from .signals import get_pic_ai_bio  # Assegure-se de que a função está importada corretamente

# Configure o Generative AI com a chave de API segura
genai.configure(api_key=settings.API_KEY)

# Classe para listar os quadros com funcionalidade de busca e paginação
class PicturesListView(ListView):
    model = Pictures
    template_name = "pictures.html"
    context_object_name = "pictures"
    paginate_by = 10  # Número de itens por página

    def get_queryset(self):
        queryset = super().get_queryset().order_by("model")
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(artist__name__icontains=search)
        return queryset

class PicDetailView(DetailView):
    model = Pictures
    template_name = "pictures_detail.html"
    context_object_name = "picture"  # Opcional: facilita o uso no template

@method_decorator(login_required(login_url="login"), name="dispatch")
class NewPictureView(CreateView):
    model = Pictures
    form_class = PicturesForm
    template_name = "new_picture.html"
    success_url = reverse_lazy("pictures_list")

    def form_valid(self, form):
        # Salva o objeto sem commit para adicionar a bio se necessário
        self.object = form.save(commit=False)

        # Verifica se o campo 'bio' está vazio
        if not self.object.bio:
            # Gera a bio usando a IA
            bio = get_pic_ai_bio(
                model_name=self.object.model,
                brand=self.object.artist.name,
                year=self.object.factory_year
            )
            if bio:
                self.object.bio = bio
                messages.success(self.request, "Descrição gerada automaticamente com sucesso!")
            else:
                # Caso a IA não gere a bio, define uma descrição padrão
                self.object.bio = "Descrição padrão do quadro."
                messages.warning(self.request, "Não foi possível gerar a descrição automaticamente. Uma descrição padrão foi atribuída.")

        # Salva o objeto com a bio preenchida
        self.object.save()

        messages.success(self.request, "Quadro cadastrado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Por favor, corrija os erros abaixo.")
        return super().form_invalid(form)

@method_decorator(login_required(login_url="login"), name="dispatch")
class PicUpdateView(UpdateView):
    model = Pictures
    form_class = PicturesForm
    template_name = "pic_update.html"
    success_url = reverse_lazy("pictures_list")
    context_object_name = "picture"  # Adicione esta linha

@method_decorator(login_required(login_url="login"), name="dispatch")
class PicDeleteView(DeleteView):
    model = Pictures
    template_name = "pic_delete.html"  # Você precisará criar este template
    success_url = reverse_lazy("pictures_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Quadro deletado com sucesso!")
        return super().delete(request, *args, **kwargs)
