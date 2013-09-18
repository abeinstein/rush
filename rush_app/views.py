from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Frat, User, Rush, Comment, CommentForm, UserProfile
from .forms import RushCreateForm


# class RushListView(ListView):
#     ''' Main view (list of rushes) '''
#     model = Rush
#     template_name="rush_list.html"

#     def get_context_data(self, **kwargs):
#         context = super(RushListView, self).get_context_data(**kwargs)
#         context["frat"] = self.request.user.userprofile.frat
#         return context

#     def get_queryset(self):
#         queryset = super(RushListView, self).get_queryset()
#         my_frat = self.request.user.userprofile.frat
#         return queryset.filter(frat__pk=my_frat.pk)


# Class based views
class RushCreateView(CreateView):
    model = Rush
    template_name = "rush_app/add_rush.html"

    def form_valid(self, form):
        form.instance.frat = self.request.user.userprofile.frat
        import pdb; pdb.set_trace()
        # form. = Rush(picture=self.request.FILES['picture'])

        # picture.save()
        return super(RushCreateView, self).form_valid(form)

    def get_form_class(self):
        return RushCreateForm

    # TODO: Figure out if this was actually necessary
    def get_form_kwargs(self):
        kwargs = {'initial': self.get_initial()}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
                })
        return kwargs

    def get_success_url(self):
        return reverse(show_frat, args=[self.request.user.userprofile.frat.pk])

class RushUpdateView(UpdateView):
    model = Rush
    template_name = "rush_app/edit_rush.html"

    def get_form_class(self):
        return RushCreateForm

    def get_form_kwargs(self):
        kwargs = super(RushUpdateView, self).get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
                })
        return kwargs

    def get_success_url(self):
        return reverse(show_frat, args=[self.request.user.userprofile.frat.pk])

class RushDeleteView(DeleteView):
    model = Rush

    def get_success_url(self):
        return reverse(show_frat, args=[self.request.user.userprofile.frat.pk])





# Function based views TODO: Rewrite into class-based views

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

def show_frat(request, frat_id, active_rush=''):
    if (request.user.is_authenticated() and 
            request.user.userprofile.frat.id == int(frat_id)):
        frat = Frat.objects.get(pk=frat_id)
        # Generate a form for each rush
        form = CommentForm()
        # for r in frat.rush_set.all():
        #     print r.id
        #     forms[r.id] = CommentForm()
        rushes = frat.rush_set.all()
        if not active_rush:
            active_rush = rushes[0]

        params = {'frat': frat, 'form': form, 'rushes': rushes, 'active_rush': active_rush}

        return render(request, 'frat_page.html', params)
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
    return show_frat(request, request.user.userprofile.frat.id, active_rush=rush)
    # return HttpResponseRedirect(reverse('rush_app.views.show_frat', 
    #     args=(request.user.userprofile.frat.id, rush)))



