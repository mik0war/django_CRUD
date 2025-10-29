import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from items.models import Item


# Create your views here.

@csrf_exempt
@require_http_methods(['POST', 'GET', 'DELETE', 'PATCH'])
def item_view(request:WSGIRequest, item_id:int=None):

    if request.method == 'GET':
        sorting = request.GET.get('sorting', 'ASC')

        if item_id is None:
            if sorting == 'ASC':
                items_from_db = Item.objects.all().order_by('articul')
            elif sorting == 'DESC':
                items_from_db = Item.objects.all().order_by('-articul')
            else:
                return HttpResponse('Wrong value in sorting param', status=404)

            items = list(items_from_db)

            return JsonResponse({'data': [i.to_dict() for i in items]})

        try:
            item = Item.objects.get(id=item_id)
            return JsonResponse({'data': item.to_dict()})
        except Item.DoesNotExist:
            return JsonResponse({'status': 'no such record'}, status=404)

    elif request.method == 'POST':
        try:
            body_dict = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return HttpResponse('Wrong json', status=400)

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

    elif request.method == 'DELETE':
        try:
            item = Item.objects.get(id=item_id)

            item_dict = item.to_dict()

            item.delete()

            return JsonResponse({'status': 'deleted', 'item': item_dict})

        except Item.DoesNotExist:
            return JsonResponse({'status': 'no such record'}, status=404)

    elif request.method == 'PATCH':
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return JsonResponse({'status': 'no such record'}, status=404)

        try:
            body = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return HttpResponse('Wrong json', status=400)

        if 'articul' in body:
            item.articul = body['articul']

        if 'name' in body:
            item.name = body['name']

        item.save()

        return JsonResponse({'status': 'updated', 'item': item.to_dict()})
