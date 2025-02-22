from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from .models import Product
from .serializers import ProductSerializer
from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer
from django.db.models import Sum, Count
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Sum, Count
from rest_framework.decorators import api_view, permission_classes
from .models import Order, OrderItem, Product  # ✅ استيراد OrderItem
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter  # ✅ استيراد الفلتر
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]  # ✅ إضافة فلترة
    filterset_class = ProductFilter  # ✅ تحديد الفلتر
    
    @method_decorator(cache_page(60 * 15))  # ✅ التخزين لمدة 15 دقيقة
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_permissions(self):
        """تحديد الصلاحيات بناءً على نوع العملية"""
        if self.action in ['list', 'retrieve']:  
            return [AllowAny()]  # الجميع يمكنهم رؤية المنتجات
        return [IsAdminUser()]  # الإدارة فقط يمكنهم الإضافة والتعديل والحذف

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()  # ✅ أضفنا queryset هنا
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.select_related('user').prefetch_related('products')
        
        if user.is_staff:
            return queryset
        return queryset.filter(user=user)
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
@api_view(['GET'])
@permission_classes([IsAdminUser])
def sales_report(request):
    """تقرير المبيعات اليومي"""

    # إجمالي المبيعات
    total_sales = Order.objects.filter(status='COMPLETED').aggregate(Sum('total_price'))['total_price__sum'] or 0

    # أكثر المنتجات مبيعًا
    top_products = OrderItem.objects.values('product__name').annotate(
        total_sold=Sum('quantity')
    ).order_by('-total_sold')[:5]

    # الإيرادات حسب الفئة
    revenue_by_category = OrderItem.objects.values('product__category').annotate(
        total_revenue=Sum('quantity') * Sum('product__price')
    )

    return Response({
        'total_sales': total_sales,
        'top_products': list(top_products),
        'revenue_by_category': list(revenue_by_category)
    })