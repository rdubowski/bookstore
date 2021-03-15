from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import Book, Order, OrderItem, ShippingAddress
from base.serializers import BookSerializer, OrderSerializer
from rest_framework import status


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data
    orderItems = data['orderItems']
    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice']
        )
        shipping = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country'],
        )
        for i in orderItems:
            book = Book.objects.get(_id=i['book'])
            item = OrderItem.objects.create(
                book=book,
                order=order,
                name=book.name,
                quantity=i['qty'],
                price=i['price'],
                image=book.image.url
            )
            book.countInStock -= item.quantity
            book.save()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    user = request.user
    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response({'detail': 'Not authorized to view this order'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Order does not exists'}, statu=status.HTTP_400_BAD_REQUEST)