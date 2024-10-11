from django.db.models.signals import pre_save, post_save, post_delete
from django.db.models import Sum 
from django.dispatch import receiver
from quadros.models import Pictures, PicturesInventory
from openai_api.client import get_pic_ai_bio


def pic_inventory_update():
    # Ações a serem executadas após salvar um quadro
    pic_count = Pictures.objects.all().count()  # Recebendo a quantidade de quadros registrados
    pic_value = Pictures.objects.all().aggregate(  # Da um campo rotulado, personalizado
        total_value=Sum("value")
    )['total_value'] if Pictures.objects.all().exists() else 0  # Recebendo o valor total dos quadros registrados
    PicturesInventory.objects.create(  # Criando um novo registro no inventário
        pic_count=pic_count,
        pic_value=pic_value,
    )  # Salvando o novo registro no inventário

@receiver(pre_save, sender=Pictures)
def pic_pre_save(sender, instance, **kwargs):# criar bio dos quadros automatica
    if not instance.bio:
        ai_bio = get_pic_ai_bio(instance.model, instance.artist.name, instance.factory_year)
        instance.bio = ai_bio    


@receiver(post_save, sender=Pictures)
def pic_post_save(sender, instance, **kwargs):
    # Ações a serem executadas após salvar um quadro
    pic_inventory_update()


@receiver(post_delete, sender=Pictures)
def pic_post_delete(sender, instance, **kwargs):
    # Ações a serem executadas após excluir um quadro
    pic_inventory_update()
