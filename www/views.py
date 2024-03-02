from django.views.generic import ListView, TemplateView, View, DetailView
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from . import models
from . import utils


class FoodListView(ListView):
    model = models.Food
    template_name = 'www/index.html'
    context_object_name = 'foods'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drinks'] = models.Drink.objects.all()
        return context


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
        order_drinks = order.orderdrink_set.all()
        context['order_foods'] = order_foods
        context['order_drinks'] = order_drinks
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
        drinks = models.Drink.objects.all()
        return render(request, 'www/foods_form.html', {'foods': foods, 'drinks': drinks})

    @staticmethod
    def post(request):
        food_ids = request.POST.getlist('foods')
        drink_ids = request.POST.getlist('drinks')
        order = utils.create_order(request.session['fio'], request.session['address'], 0)

        total_price = 0
        for food_id in food_ids:
            food = get_object_or_404(models.Food, id=food_id)
            order_food = utils.create_order_food(food, order, request.POST[f'quantity{food_id}'])
            total_price += order_food.price
            order_food.save()

        for drink_id in drink_ids:
            drink = get_object_or_404(models.Drink, id=drink_id)
            order_drink = utils.create_order_drink(drink, order, request.POST[f'quantity{drink_id}'])
            total_price += order_drink.price
            order_drink.save()

        order.total_price = total_price
        order.save()

        return redirect('food_list')
