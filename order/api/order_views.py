from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from order import tasks
from order.models.order import Order
from order.serializers.order_serializers import GetOrderSerializer, PostOrderSerializer, PutOrderSerializer, \
    SearchOrderSerializer, ImageUploadSerializer
from common import Utils


class OrderView(APIView):
    """
    order api
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        query_params = request.query_params
        context = {'request': request}
        id = query_params.get('id', None)
        page_no = query_params.get('page_no', None)
        page_no = Utils.to_int(page_no)
        page_size = query_params.get('page_size', None)
        page_size = Utils.to_int(page_size)

        if id:
            try:
                order = Order.objects.get(id=id, user=request.user)
            except Order.DoesNotExist as e:
                return Response({'message': 'Please provide valid id'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = GetOrderSerializer(instance=order, context=context)
                return Response(serializer.data)
        else:
            if not (page_no and page_size):
                return Response({'message': 'Please provide valid page_no and page_size'}, status=status.HTTP_400_BAD_REQUEST)
            orders = Order.objects.filter(user=request.user).order_by('-modified_on')
            p = Paginator(orders, page_size)
            serializer = GetOrderSerializer(instance=p.page(page_no), context=context, many=True)
            return Response({'payload': serializer.data, 'total_count': p.count})

    def post(self, request):
        data = request.data
        context = {'request': request}
        id = data.get('id', None)
        if not id:
            serializer = PostOrderSerializer(data=data, context=context)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            order = serializer.save()
            tasks.send_sms.delay(serializer.validated_data['customer_mobile'],
                                 'Your tailoring order is successfully placed.')
            return Response({'message': 'Order added successfully', "id": order.id})
        else:
            try:
                order = Order.objects.get(id=id, user=request.user)
            except Order.DoesNotExist as e:
                return Response({'message': 'Please provide valid id'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = PutOrderSerializer(data=data, instance=order, context=context)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            order = serializer.save()
            return Response({'message': 'Order updated successfully', "id": order.id})


class SearchView(APIView):
    """
    search api
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        query_params = request.query_params
        context = {'request': request}
        text = query_params.get('text', "")
        objects = Order.objects.filter(text__search=text, user=request.user)
        serializer = SearchOrderSerializer(objects, context=context, many=True)
        return Response({'payload': serializer.data})


class ImageUploadView(APIView):
    """
    image upload api
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        context = {'request': request}
        serializer = ImageUploadSerializer(data=data, context=context)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        image_url =serializer.save()
        return Response({'image_url': image_url})
