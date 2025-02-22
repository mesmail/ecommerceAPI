import django_filters
from .models import Product
import django_filters
from django.core.exceptions import ValidationError
from .models import Product
import re

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='sanitize_name')
    category = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Product
        fields = ['name', 'category']

    def sanitize_name(self, queryset, name, value):
        """🔒 تنظيف مدخلات البحث لمنع SQL Injection"""
        forbidden_patterns = [
            r";",           # منع الفاصلة المنقوطة
            r"--",          # منع التعليقات في SQL
            r"'",           # منع الفاصلة الفردية
            r"\"",          # منع الفاصلة المزدوجة
            r" OR ",        # منع استخدام OR في SQL
            r" AND ",       # منع استخدام AND في SQL
            r"SELECT ",     # منع استخدام SELECT
            r"INSERT ",     # منع استخدام INSERT
            r"UPDATE ",     # منع استخدام UPDATE
            r"DELETE ",     # منع استخدام DELETE
            r"DROP ",       # منع حذف الجداول
            r"UNION ",      # منع الهجمات باستخدام UNION
            r"EXEC ",       # منع تنفيذ أوامر SQL
            r"WAITFOR "     # منع هجمات تأخير التنفيذ
        ]

        for pattern in forbidden_patterns:
            if re.search(pattern, value, re.IGNORECASE):
                raise ValidationError("Invalid search input: Possible SQL Injection detected.")

        return queryset.filter(name__icontains=value)
