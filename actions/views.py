from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from actions.models import Action


@login_required
def show_actions(request):
    actions = Action.objects.all()
    actions = actions.select_related('user', 'user__profile')[:10]\
        .prefetch_related('target')[:10]
    return render(request,
                  'actions/user_actions.html',
                  {'actions': actions},)
