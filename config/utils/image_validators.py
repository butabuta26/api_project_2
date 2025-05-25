from django.core.validators import ValidationError
import PIL
from PIL import Image
from django.apps import apps

def validate_image_size(image):
    size = image.size
    limit = 5
    if size > limit * 1024 * 1024:
        raise ValidationError(f'ფაილი არ უნდა აღემატებოდეს {limit}MB')
    
def validate_image_resolution(image):
    image = Image.open(image)
    width, height = image.size
    min_width, min_height = 300, 300
    max_width, max_height = 4000, 4000
    if width >= max_width or height >= max_height:
        raise ValidationError(f'სურათის გაფართოება არ უნდა აღემატებოდეს 4000*4000 პიქსელს')
    if width <= min_width or height <= min_height:
        raise ValidationError(f'სურათის გარართოება არ უნდა იყოს 300*300 პიქსელზე ნაკლები')
    
def validate_image_count(product_id):
    ProductImage = apps.get_model('products', 'ProductImage')
    limit = 5
    count = ProductImage.objects.filter(product_id=product_id).count()
    if count >= limit:
        raise ValidationError(f'1 პროდუცტზე, მაქსიმუმ შეგვიძლია {limit} სურათის შენახვა')