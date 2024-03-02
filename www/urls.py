from django.urls import path
from . import views


urlpatterns = [
    path('', views.FoodListView.as_view(), name='food_list'),
    path('order', views.OrderTemplate.as_view(), name='order_form'),
    path('order/foods', views.OrderFoodCreateView.as_view(), name='order_foods'),
    path('orders/', views.OrderList.as_view(), name='order_list'),
    path('order_detail/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail')
]
