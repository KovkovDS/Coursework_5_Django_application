from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from django.urls import reverse
from users.models import User


@permission_required("users.view_user")
def block_user(self, pk):
    user = User.objects.get(pk=pk)
    user.is_active = {user.is_active: False, not user.is_active: True}[True]
    user.save()
    return redirect(reverse("users:profiles"))

