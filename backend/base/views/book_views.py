from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from base.models import Author, Book, Genre, Review
from base.serializers import BookSerializer


@api_view(["GET"])
def get_books(request):
    query = request.query_params.get("keyword")
    if query is None:
        query = ""
    books = Book.objects.filter(name__icontains=query).order_by("createdAt")
    page = request.query_params.get("page")
    paginator = Paginator(books, 4)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    if page is None:
        page = 1
    page = int(page)
    serializer = BookSerializer(books, many=True)
    return Response(
        {"books": serializer.data, "page": page, "pages": paginator.num_pages}
    )


@api_view(["GET"])
def get_top_books(request):
    books = Book.objects.filter(rating__gte=4).order_by("-rating")[0:3]
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_book(request, pk):
    book = Book.objects.get(_id=pk)
    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def add_book(request):
    user = request.user
    book = Book.objects.create(
        user=user,
        name="Sample Name",
        price=0,
        countInStock=0,
        description="",
        pagesNum=0,
        ISBN="",
    )
    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAdminUser])
def update_book(request, pk):
    data = request.data
    book = Book.objects.get(_id=pk)
    book.name = data["name"]
    book.description = data["description"]
    book.price = data["price"]
    book.countInStock = data["countInStock"]
    book.ISBN = data["ISBN"]
    book.pagesNum = data["pagesNum"]
    authors = data["author"]
    genres = data["genre"]
    if not isinstance(authors, list):
        book.author.clear()
        auths = authors.split(",")
        for auth in auths:
            auth = auth.strip()
            if auth:
                a = Author.objects.get_or_create(full_name=auth)
                book.author.add(a[0].id)
    if not isinstance(genres, list):
        book.genre.clear()
        gns = genres.split(",")
        for gn in gns:
            gn = gn.strip()
            if gn:
                g = Genre.objects.get_or_create(name=gn)
                book.genre.add(g[0].id)
    book.save()
    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_book(request, pk):
    book = Book.objects.get(_id=pk)
    book.delete()
    return Response("Book has been deleted")


@api_view(["POST"])
def upload_image(request):
    data = request.data
    book_id = data["book_id"]
    book = Book.objects.get(_id=book_id)
    book.image = request.FILES.get("image")
    book.save()
    return Response("Image was uploaded")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_book_review(request, pk):
    book = Book.objects.get(_id=pk)
    user = request.user
    data = request.data
    already_exsists = book.review_set.filter(user=user).exists()
    if already_exsists:
        content = {"detail": "Product already reviewed"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif data["rating"] == 0:
        content = {"detail": "Please select a rating"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        review = Review.objects.create(
            user=user,
            book=book,
            name=user.first_name,
            rating=data["rating"],
            comment=data["comment"],
        )
        reviews = book.review_set.all()
        book.numReviews = len(reviews)
        total = 0
        for review in reviews:
            total += review.rating
        book.rating = total / len(reviews)
        book.save()
        return Response("Review added")
