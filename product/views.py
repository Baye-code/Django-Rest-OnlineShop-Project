from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer
from .filters import ProductsFilter

# Create your views here.

@api_view(['GET'])
def get_products(request):

    products = Product.objects.all()
    ordered_products = Product.objects.all().order_by('id')

    filterset = ProductsFilter(request.GET, queryset=ordered_products)
    count = filterset.qs.count()

    # Pagination
    resPerPage = 1
    paginator = PageNumberPagination()
    paginator.page_size = resPerPage
    query_set = paginator.paginate_queryset(filterset.qs, request)

    # serializer = ProductSerializer(products, many=True)
    # serializer = ProductSerializer(filterset.qs, many=True)
    serializer = ProductSerializer(query_set, many=True)

    return Response(
        {
            "products": serializer.data,
            "count": count,
            "resPerPage": resPerPage
            }
        )


@api_view(['GET'])
def get_product(request, pk):

    product = get_object_or_404(Product, id=pk)

    serializer = ProductSerializer(product, many=False)

    return Response(
        {
            "product": serializer.data,
            }
        )