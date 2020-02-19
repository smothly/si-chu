from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from allauth.account.views import EmailView as BaseEmailView
from search.models import Lecture
from .forms import majors, EmailUpdateForm, ProfileUpdateForm

User = get_user_model()


# Create your views here.
@login_required
def add_favorite_lecture(request):
    button_text = ('<i class="far fa-heart is-large"></i>', '<i class ="fas fa-heart"> </i>')
    message = ("해당 강의를 찜취소 했습니다.", "해당 강의를 찜했습니다. 마이페이지에서 확인하실 수 있습니다.")

    ctx = dict()
    if request.method == "POST":
        pk = request.POST.get("id")
        favorite = request.user.toggle_favorite_lecture(pk)
        messages.info(request, message[favorite])
        msg = render_to_string("includes/message.html", {"messages": messages.get_messages(request)})
        ctx = {
            "target": f"#favorite-{pk}",
            "data": button_text[favorite],
            "msg": msg
        }
    return JsonResponse(ctx)


@login_required
def my_page(request):
    users = User.objects.prefetch_related('favorite_lectures')
    user = users.get(pk=request.user.pk)
    try:
        major = majors[user.major][1]
    except:
        major = "정보없음"
    ctx = {'user': user}
    return render(request, 'mypage.html', ctx)


@login_required
def profile_update(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, "프로필을 성공적으로 수정하였습니다.")
            return redirect('account_mypage')
        else:
            messages.error(request, "프로필을 수정에 실패하였습니다.")
    else:
        form = ProfileUpdateForm(instance=request.user)
    ctx = {'form': form}
    return render(request, 'profile_update_form.html', ctx)


@login_required
def email_update(request):
    form = EmailUpdateForm()
    ctx = {'form': form}
    return render(request, 'email_update_form.html', ctx)


class EmailView(LoginRequiredMixin, BaseEmailView):
    success_url = reverse_lazy('email_update')
    template_name = "email_update_form.html"
    form_class = EmailUpdateForm
