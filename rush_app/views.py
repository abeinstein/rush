from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect
from rush_app.models import Frat, User, Rush, Comment, CommentForm, UserProfile

def index(request):
    return render(request, 'index.html')

def home(request):
    if not request.user.is_authenticated():
        return render(request, 'index.html')
    else:
        return show_frat(request, request.user.userprofile.frat.id)


def all_frats(request):
    if not request.user.is_authenticated():
    	all_frats = Frat.objects.all()
    	return render(request, 'frats.html', 
    		{'frats': all_frats})
    else:
        frat_id = request.user.userprofile.frat.id
        return show_frat(request, frat_id)

def show_frat(request, frat_id):
    if (request.user.is_authenticated() and 
            request.user.userprofile.frat.id == int(frat_id)):
        frat = Frat.objects.get(pk=frat_id)
        # Generate a form for each rush
        form = CommentForm()
        # for r in frat.rush_set.all():
        #     print r.id
        #     forms[r.id] = CommentForm()

        return render(request, 'frat_page.html', {'frat': frat, 'form': form})
    else:
        return redirect_to_login(request.path)

@login_required
def thumbs(request, is_up, user_id, rush_id):
    user = User.objects.get(id=user_id)
    rush = Rush.objects.get(id=rush_id)
    is_up = int(is_up)

    if user and rush:
        if is_up:
            rush.reputation.thumbsup_users.add(user.userprofile)
        else:
            rush.reputation.thumbsdown_users.add(user.userprofile)
        rush.reputation.save()

    return all_frats(request)

@login_required
def add_comment(request, rush_pk, user_pk):
    p = request.POST

    if p.has_key("body") and p["body"]:
        rush = Rush.objects.get(pk=rush_pk)
        prof = UserProfile.objects.get(pk=user_pk)
        comment = Comment(rush=rush, userprofile=prof)
        cf = CommentForm(p, instance=comment)
        cf.save()
    return HttpResponseRedirect(reverse('rush_app.views.show_frat', 
        args=[request.user.userprofile.frat.id]))



