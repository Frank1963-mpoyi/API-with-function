from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Article
from resto.serializers import ArticleSerializer

@csrf_exempt
def article_list(request):
    # RETRIEVE QUERY SET
    if request.method == 'GET':
        articles = Article.objects.all()
        # here we can serialize the article
        serializer = ArticleSerializer(articles, many = True) # many =True because we serialize the queryset 
        return JsonResponse(serializer.data, safe=False) #By default, the JsonResponse’s first parameter, data, should be a dict instance. To pass any other JSON-serializable object you must set the safe parameter to False.
        
        # POST METHOD
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status = 400)



@csrf_exempt
def article_detail(request, pk=None):
    # GET METHOD 
    #article = get_object_or_404(Article, pk = pk)
    article = Article.objects.get(id=pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data)

    # UPDATE METHOD
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status = 400)

        # DELETE METHOD
    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status = 204)