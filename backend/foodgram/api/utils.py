from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def get_shopping_cart(data):
    """Функция для создания pdf файла ингредиентов для покупки."""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="recipe.pdf"'
    
    file = canvas.Canvas(response)

    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    file.setFont('Arial', 14)

    file.drawImage('static\download.jpg', 0, -400)

    file.drawString(50, 780, 'Наименование')
    file.drawString(300, 780, 'Еденицы')
    file.drawString(500, 780, 'Количество')

    for i, obj in enumerate(data):
        file.drawString(50, 750-i*20, obj['name'])
        file.drawString(300, 750-i*20, obj['measurement_unit'])
        file.drawString(500, 750-i*20, str(obj['amountingredient__amount']))

    file.showPage()
    file.save()
    return response