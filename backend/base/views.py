
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from.serializer import BookSerializer

@api_view(['GET'])
def getRouter(request):
    return Response('Hello')


@api_view(['GET'])
def getBooks(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getBook(request, pk):
    book = Book.objects.get(_id=pk)
    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)
