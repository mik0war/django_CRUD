import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from items.models import Item


# Create your views here.

def index(request):
    text = 'Items app'

    return HttpResponse(text, status=200)


@csrf_exempt
@require_http_methods(['POST'])
def create(request:WSGIRequest):

    body_dict = json.loads(request.body)

    if ('count' not in body_dict or
        'price' not in body_dict or
        'discount' not in body_dict):
        return HttpResponse('count and price and discount required', status=400)

    item = Item(
        **body_dict
    )

    item.save()

    return JsonResponse(data={
        'status': 'created',
        'item': item.to_dict()
    })


@require_http_methods(['GET'])
def read(request, item_id=None, sorting='ASC'):
    if item_id is None:
        if sorting =='ASC':
            items_from_db = Item.objects.all().order_by('articul')
        elif sorting == 'DESC':
            items_from_db = Item.objects.all().order_by('-articul')

        items = list(items_from_db)

        return JsonResponse({'data': [i.to_dict() for i in items]})

    item = Item.objects.get(id=item_id)
    return JsonResponse({'data': item.to_dict()})



@csrf_exempt
@require_http_methods(['DELETE'])
def delete(request, item_id):

    try:
        item = Item.objects.get(id=item_id)

        item_dict = item.to_dict()

        item.delete()

        return JsonResponse({'status': 'deleted', 'item': item_dict})

    except Item.DoesNotExist:
        return JsonResponse({'status': 'no such record'}, status=404)


@csrf_exempt
@require_http_methods(['PATCH'])
def update(request:WSGIRequest, item_id):
    item = Item.objects.get(id=item_id)

    body = json.loads(request.body)

    if 'articul' in body:
        item.articul = body['articul']

    item.save()

    return JsonResponse({'status' : 'updated', 'item' : item.to_dict()})







