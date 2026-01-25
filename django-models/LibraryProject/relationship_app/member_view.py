from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'member'

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')