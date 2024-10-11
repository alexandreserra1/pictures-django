# quadros/forms.py

from django import forms
from quadros.models import Pictures, Artist

class PicturesForm(forms.ModelForm):
    artist_name = forms.CharField(
        max_length=200,
        label='Artista',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome do Artista',
            'class': 'form-control',
        })
    )
    bio = forms.CharField(
        label='Descrição',
        required=False,  # Campo opcional
        widget=forms.Textarea(attrs={
            'placeholder': 'Descrição do Quadro',
            'class': 'form-control',
            'rows': 4,
        })
    )

    class Meta:
        model = Pictures
        exclude = ['artist']  # Excluímos o campo 'artist' do formulário
        widgets = {
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'placeholder': 'Selecione uma imagem'
            }),
            'model': forms.TextInput(attrs={
                'placeholder': 'Modelo do Quadro',
                'class': 'form-control'
            }),
            'factory_year': forms.NumberInput(attrs={
                'placeholder': 'Ano de Fabricação',
                'class': 'form-control'
            }),
            'value': forms.NumberInput(attrs={
                'placeholder': 'Preço do Quadro',
                'class': 'form-control'
            }),
            'artistic_style': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def save(self, commit=True):
        """
        Método para salvar os dados do formulário no banco de dados,
        criando ou obtendo o artista com base no nome fornecido.
        """
        instance = super().save(commit=False)
        artist_name = self.cleaned_data.get('artist_name').strip()

        # Normaliza o nome do artista
        artist_name = artist_name.title()

        # Obtém ou cria o artista com base no nome fornecido
        artist, created = Artist.objects.get_or_create(name__iexact=artist_name, defaults={'name': artist_name})

        instance.artist = artist

        if commit:
            instance.save()
        return instance
