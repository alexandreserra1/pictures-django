from django.contrib import admin
from quadros.models import Pictures, Artist # da pasta car, importe o arquivo models


# Register your models here.

class PicAdmin(admin.ModelAdmin):
    list_display = ('model', 'artist', 'factory_year', 'value') #lista de campos q aparece na grid do admin
    search_fields = ('model', 'artist') #campo de busca
    list_filter = ('artistic_style', 'artist', 'factory_year')
    
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Pictures, PicAdmin) #serve para salvar