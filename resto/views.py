from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
#from rest_framework.parsers import JSONParser
from .models import Article
from resto.serializers import ArticleSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response # here not Json response
from rest_framework import status





# DJANGO BROWSER API

#@csrf_exempt
@api_view(['GET','POST'])
def article_list(request):
    # RETRIEVE QUERY SET
    if request.method == 'GET':
        articles = Article.objects.all()
        # here we can serialize the article
        serializer = ArticleSerializer(articles, many = True) # many =True because we serialize the queryset 
        #return JsonResponse(serializer.data, safe=False) #By default, the JsonResponse’s first parameter, data, should be a dict instance. To pass any other JSON-serializable object you must set the safe parameter to False.
        return Response(serializer.data)
        # POST METHOD
    elif request.method == 'POST':
        #data = JSONParser().parse(request)
        #serializer = ArticleSerializer(data = data)
        serializer = ArticleSerializer(data = request.data) # we need to get the data from request

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) # you must import this status
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



#@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def article_detail(request, pk=None):
    # GET METHOD 
    article = get_object_or_404(Article, pk = pk)
    #article = Article.objects.get(id=pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    # UPDATE METHOD
    elif request.method == 'PUT':
        #data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        # DELETE METHOD
    elif request.method == 'DELETE':
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)