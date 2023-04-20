import os

from django.http import HttpResponse

from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def get_shopping_cart(queryset):
    """
    Функция для создания pdf файла ингредиентов для покупки.
        - Создаем список data со всеми ингредиентами.
        - Затем создаем pdf file используя Canvas
        - В словаре result_cart объединяем одинаковые ингредиенты
        - Записываем их в pdf file 
    """
    data = [queryset[i].recipe.ingredients.all().values(
            'name', 'measurement_unit', 'amountingredient__amount') 
            for i, _ in enumerate(queryset)]
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="recipe.pdf"'
    
    file = Canvas(response)

    path_to_font = os.path.join('static/download_cart', 'arial.ttf')
    pdfmetrics.registerFont(TTFont('Arial', path_to_font))
    file.setFont('Arial', 18)

    path_to_image = os.path.join('static/download_cart', 'download.jpg')
    file.drawImage(path_to_image, 0, -400)

    file.drawString(50, 780, 'Наименование')
    file.drawString(400, 780, 'Количество')

    result_cart = {}
    for element in data:
        for ingredient in element:
            if ingredient['name'] in result_cart:
                result_cart[ingredient['name']]['amountingredient__amount'] +=\
                ingredient['amountingredient__amount']
            else:
                result_cart[ingredient['name']] = ingredient

    for i, obj in enumerate(result_cart.values()):
        file.drawString(50, 750-i*20, obj['name'])
        file.drawString(400, 750-i*20, 
        f'{obj["amountingredient__amount"]} {obj["measurement_unit"]}')

    file.showPage()
    file.save()
    return response