from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer
from sqlalchemy import python


# GET ALL + POST
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def customer_list_create(request):

    if request.method == "GET":
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("new data added")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET SINGLE + PATCH + DELETE
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def customer_detail(request, id):

    try:
        customer = Customer.objects.get(id=id)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    elif request.method == "PATCH":
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("new data update successful")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        customer.delete()
        return Response({"message": "Customer deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
