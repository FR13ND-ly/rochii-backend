from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponseBadRequest
from .models import Image
from django.conf import settings
from rest_framework import status
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .serializers import getImage
from PIL import Image as PILImage
from io import BytesIO

@csrf_exempt
def uploadImage(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            file = request.FILES['file']
            if not file.content_type.startswith('image/'):
                raise ValidationError('Fișierul nu e imagine')

            original_img = PILImage.open(file)
            
            resized_img = original_img.copy()
            resized_img.thumbnail((800, 800)) 
            
            output = BytesIO()
            resized_img.save(output, format='webp', quality=85)
            
            while output.tell() > 100 * 1024:
                output = BytesIO()
                resized_img.save(output, format='webp', quality=70)
            
            img = Image.objects.create(
                name=file.name,
                contentType=file.content_type,
                data=output.getvalue()
            )
            img.save()
            
            res = getImage(img)
            return JsonResponse(res, status=status.HTTP_200_OK)       
        except ValidationError as e:
            return JsonResponse({'error': e.message}, status=400)
        except Exception as e:
            return HttpResponseBadRequest({'error': 'Ceva a mers greșit.'})
    else:
        return JsonResponse({'error': 'Nu ai încărcat un file.'}, status=400)
    

def serveImage(request, imageId):
    try:
        image = Image.objects.get(id=imageId)
        image_data = image.data
        
        response = HttpResponse(image_data, content_type=image.contentType)
        response['Content-Disposition'] = f'attachment; filename="{image.name}"'
        return response
    except Image.DoesNotExist:
        return JsonResponse({'error': 'Image not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

