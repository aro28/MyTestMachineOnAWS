from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import views #для класс APIView
from .models import Category, Item
from .serializers import CategorySerializer, ItemSerializer
from .my_generic_view import MyGenericListCreateView, MyGenericRetrieveUpdatDestroy
from rest_framework import viewsets
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    #below comment goes to http://127.0.0.1:8000/swagger/
    """
    Category Create and List View
    :params limit: int
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer # Это даст

# @csrf_exempt
@api_view(http_method_names=['GET', 'POST'])
def item_list_create_api_view(request):
    # print(request.GET) #отправил то что в параметре запроса.если в запросе указале ?. ты можешь получить в объекте request в атрибуте GET?
    # print(request.POST) #отправил то что в теле, приниммет только form-data, JSON данные не принимает
    # print(request.query_params) #то что в url параметрах <QueryDict: {'value1': ['param1']}>
    # print(request.data) #десрализованные данниз из JSON в Python формат {'post_value': 'param_post'}
    # data = [
    #     {
    #         "name":"Codify",
    #         "address": "7mkr"
    #     }
    #  ]
    # return HttpResponse(data) # возрващает и получает пайтоновский формат: {'name': 'Codify', 'address': '7mkr'} отрисованое в HTML
    if request.method == 'GET':
        queryset = Item.objects.all()
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    return Response(serializer.data) # ,берет патоновский и возвращает JSON
# FUNCTION-BASED VIEW
@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def item_retrieve_update_destroy_api_view(request, pk):
    item = get_object_or_404(Item, pk=pk)
    # строка выше тоже самое что внизу:
    # try:
    #     data = Item.objects.get(pk=pk)
    # except Item.DoesNotExist:
    #     return Response({'detail':'Not found'},status=404)

    if request.method == 'GET':
        serializer= ItemSerializer(instance=item)
        return Response(serializer.data) #из пайтона в JSON
    elif request.method == 'PUT':
        serializer = ItemSerializer(instance=item,data=request.data) #вызовится метод UPDATE и запишет
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
    elif request.method == "DELETE":
        item.delete()
        return Response(status=204)

# CLASS-BASED VIEW inheritated from my generic view. Дает возможность добавлять чреез HTML Form
class ItemListCreateView(MyGenericListCreateView): #мы наследуемся от универсального класса(my_generic_view) где находятся POST,GET,DELETE
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemRetrieveUpdatDestroy(MyGenericRetrieveUpdatDestroy): #в APIVIew есть as_view которые отвечает в какую функции передавать
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
