from django.shortcuts import render
from .models import Category,SubCategory
import json 
from django.shortcuts import HttpResponse

# Create your views here.
def category(request):
  categories = Category.objects.all()

  context = {
    categories: categories
  }

  return render(request,)

def get_sub_category(request):
  id = request.GET.get('id','10')
  id = int(id)
  result = list(SubCategory.objects.filter(category__id=id).values('id','name'))
  return HttpResponse(json.dumps(result),content_type='application/json')
  