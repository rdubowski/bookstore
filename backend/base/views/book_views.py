from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from base.models import Book, Genre, Author
from base.serializers import BookSerializer


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

@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_book(request):
    user = request.user
    book = Book.objects.create(
        user=user,
        name='Sample Name',
        price=0,
        countInStock=0,
        description='',
    )
    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_product(request, pk):
    data = request.data
    book = Book.objects.get(_id=pk)
    book.name = data['name']
    book.description = data['description']
    book.price = data['price']
    book.countInStock = data['countInStock']
    book.author = Author.objects.get_or_create(full_name=data['author'])
    book.genre = Genre.objects.get_or_create(name=data['genre'])
    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_book(request, pk):
    book = Book.objects.get(_id=pk)
    book.delete()
    return Response('Book has been deleted')