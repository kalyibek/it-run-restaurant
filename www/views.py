from django.views.generic import ListView, TemplateView, View, DetailView
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from . import models
from . import utils


class FoodListView(ListView):
    model = models.Food
    template_name = 'www/index.html'
    context_object_name = 'foods'


class OrderList(ListView):
    model = models.Order
    template_name = 'www/orders.html'
    context_object_name = 'orders'


class OrderDetailView(DetailView):
    model = models.Order
    template_name = 'www/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        order_foods = order.orderfood_set.all()
        context['order_foods'] = order_foods
        return context


class OrderTemplate(TemplateView):
    template_name = 'www/order_form.html'

    @staticmethod
    def post(request):
        request.session['fio'] = request.POST['fio']
        request.session['address'] = request.POST['address']
        return redirect('order_foods')


class OrderFoodCreateView(View):
    @staticmethod
    def get(request):
        foods = models.Food.objects.all()
        return render(request, 'www/foods_form.html', {'foods': foods})

    @staticmethod
    def post(request):
        food_ids = request.POST.getlist('foods')
        order = utils.create_order(request.session['fio'], request.session['address'], 0)

        total_price = 0
        for food_id in food_ids:
            food = get_object_or_404(models.Food, id=food_id)
            order_food = utils.create_order_food(food, order, request.POST[f'quantity{food_id}'])
            total_price += order_food.price
            order_food.save()

        order.total_price = total_price
        order.save()

        return redirect('food_list')
