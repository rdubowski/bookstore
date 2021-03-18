from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from base.models import Book, Review
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
        pagesNum=0,
        ISBN='',
    )
    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_book(request, pk):
    data = request.data
    book = Book.objects.get(_id=pk)
    book.name = data['name']
    book.description = data['description']
    book.price = data['price']
    book.countInStock = data['countInStock']
    book.ISBN = data['ISBN']
    book.pagesNum = data['pagesNum']
    book.author = data['author']
    book.genre = data['genre']
    book.save()
    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_book(request, pk):
    book = Book.objects.get(_id=pk)
    book.delete()
    return Response('Book has been deleted')


@api_view(['POST'])
def upload_image(request):
    data = request.data
    book_id = data['book_id']
    book = Book.objects.get(_id=book_id)
    book.image = request.FILES.get('image')
    book.save()
    return Response('Image was uploaded')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_book_review(request, pk):
    book = Book.objects.get(_id=pk)
    user = request.user
    data = request.data
    already_exsists = book.review_set.filter(user=user).exists()
    if already_exsists:
        content = {'details': 'Product already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif data['rating'] == 0:
        content = {'details': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        review = Review.objects.create(
            user=user,
            book=book,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment']
        )
        reviews = book.review_set.all()
        book.numReviews = len(reviews)
        total = 0
        for review in reviews:
            total += review.rating
        book.rating = total / len(reviews)
        book.save()
        return Response('Review added')