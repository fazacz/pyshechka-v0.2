from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
# from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from .models import AdvUser, Product, Portion
from .forms import ChangeUserInfoForm, RegisterUserForm, ChangeProductForm, CreateProductForm, PortionForm, PortionFormSet
from .utilities import signer


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удалён')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')


class PyPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'main/password_reset_confirm.html'
    success_url = reverse_lazy('main:login')
    success_message = 'Пароля успешно изменён. Используйте новый пароль'


class PyPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'main/password_reset.html'
    subject_template_name = 'email/password_reset_subject.txt'
    email_template_name = 'email/password_reset_body.txt'
    success_message = 'Электронное письмо для сброса пароля отправлено'
    success_url = reverse_lazy('main:login')


class PyPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin,
                           PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменён'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def index(request):
    return render(request, 'main/index.html')


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


class PyLoginView(LoginView):
    template_name = 'main/login.html'


class PyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


@login_required
def profile(request):
    return render(request, 'main/profile.html')


###############################################################################
###############################################################################

class ProductList(ListView):
    template_name = 'main/product_list.html'
    context_object_name = 'products'
    # products = Product.objects.all()

    def get_queryset(self):
        return Product.objects.all().order_by('-update_date')


class ProductDetailView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'main/product_detail.html'
    form_class = ChangeProductForm
    success_url = reverse_lazy('main:product_list')
    success_message = 'Продукт изменён'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = super().get_object()
        portions = Portion.objects.filter(dish_id=obj.pk)
        # portions = Portion.objects.all()
        context["portions"] = portions
        return context


class ProductCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'main/product_create.html'
    form_class = CreateProductForm
    success_url = reverse_lazy('main:product_list')
    success_message = 'Продукт создан'


class ProductDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'main/product_delete.html'
    success_url = reverse_lazy('main:product_list')
    success_message = 'Продукт удалён'


class PortionCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Portion
    template_name = 'main/portion_create.html'
    form_class = PortionFormSet
    success_url = reverse_lazy('main:product_list')
    success_message = 'Порция создана'

