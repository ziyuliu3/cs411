import django_filters
from django_filters import DateFilter, CharFilter
from .models import *

class ProductFilter(django_filters.FilterSet):
	class Meta:
		model = Product
		fields = '__all__'
		exclude = ['seller','location','filt_p']