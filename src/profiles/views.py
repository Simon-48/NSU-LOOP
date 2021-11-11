from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Relationship, Skill
from django.db.models.query import QuerySet
from django.template.defaultfilters import first, last
from .forms import ProfileModelForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import *
from posts.forms import *
import random

# Create views here.
@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }

    return render(request, 'profiles/myprofile.html', context)

@login_required
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invatations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True

    context = {
        'qs': results,
        'is_empty': is_empty,
    }

    return render(request, 'profiles/my_invites.html', context)

@login_required
def accept_invatation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:my-invites-view')

@login_required
def reject_invatation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my-invites-view')

@login_required
def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {'qs': qs}

    return render(request, 'profiles/profile_list.html', context)

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
        return context

class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    # context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context

@login_required
def send_invatation(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')
    
@login_required
def remove_from_friends(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')

    
# function for displaying friend profile
def friend_profile_view(request, userId):
    profile = Profile.objects.get(pk=userId)
    context = {
        'profile': profile
    }
    return render(request, 'profiles/myprofile.html', context)

# function for rendering  find page
def find_view(request):
    return render(request, 'profiles/myprofile.html')

# function for rendering find post page
def search_post(request):
    # getting search text from url
    search_text = request.GET.get('text', None)
    if search_text is None:
        search_text = ""

    posts = Post.objects.filter(content__contains=search_text)

    # reused from post view
    c_form = CommentModelForm()

    profile = Profile.objects.get(user=request.user)

    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()

    context = {
        'search_text': search_text,
        'qs': posts,
        'profile': profile,
        'c_form': c_form,
    }

    return render(request, 'profiles/search_posts.html', context)

# function for searching people
def search_friends(request):
    # getting input values from request
    name = request.GET.get('name', "")
    email = request.GET.get('email', "")
    phone = request.GET.get("phone", "")
    cgpa = request.GET.get("cgpa", "")
    grad_year = request.GET.get("grad_year", "")
    major = request.GET.get("major", "")

    # if we got input from the form then based on each property
    # filtering profiles
    friends = Profile.objects.none() # initially we assumes that no user found, this assumption is for OR condition
    if len(name) > 0:
        friends = friends | Profile.objects.filter(first_name__contains=name) | Profile.objects.filter(last_name__contains=name)
    if len(email) > 0:
        friends = friends | Profile.objects.filter(email=email)
    if len(phone) > 0:
        friends = friends | Profile.objects.filter(phone=phone)

    # if no friend found based on first three fields
    # then search based on the other properties
    if len(friends) == 0:
        friends = Profile.objects.all() # initially we assumes all user found, this assumption is based on AND assumption
        if len(cgpa) > 0:
            friends = friends & Profile.objects.filter(cgpa=cgpa)
        if len(grad_year) > 0:
            friends = friends & Profile.objects.filter(grad_year=grad_year)
        if len(major) > 0:
            friends = friends & Profile.objects.filter(major__contains=major)
    
    # in search default all frind name will be listed
    # so makeing the list empty here
    if len(friends) == len(Profile.objects.all()):
        friends = Profile.objects.none()

    # checking wheather the result is empty or not
    empty_result = False
    if (len(name) or len(email) or len(phone) or len(cgpa) or len(grad_year) or len(major) ) and len(friends) == 0:
        empty_result = True

    context = {
        'name': name,
        'email': email,
        'phone': phone,
        'cgpa': cgpa,
        'grad_year': grad_year,
        'major': major,
        'empty_result': empty_result,
        'friends': friends,
    }

    return (render(request, 'profiles/search_friends.html', context))

# function for talent poll rednering
def talent_poll(request):
    # retrieving all skills and select one randomly
    skills = Skill.objects.all()
    skill_index = random.sample(range(0, len(skills)), 1)[0]

    # retrieving all profiles and select 5 randomly
    friends = Profile.objects.all()
    # default choice is 5
    choice_number = 5
    # but if total friend is less than 5, the choice number becomes total friend number
    if len(friends) < 5:
        choice_number = len(friends)
    friend_indexes = random.sample(range(0, len(friends)), choice_number)
    friends = [friends[i] for i in friend_indexes]

    context = {
        'skill': skills[skill_index].name,
        'friends': friends
    }

    return render(request, 'profiles/talent_poll.html', context)

# function for saving talent poll vote
def save_talen_poll(request, skill, userId):
    # retrieving user and corresponding profile based on userId
    user = User.objects.get(pk=userId) 
    profile = Profile.objects.get(user=user)

    # updating skill
    # if no skill exists
    if profile.skills is None:
        profile.skills = {skill: 1}
    # if any skill already exists
    else:
        # updating existing skill
        if skill in profile.skills:
            profile.skills[skill] += 1
        # creating new skill
        else:
            profile.skills[skill] = 1

    # saving profile
    profile.save()

    # redirecting to post page
    return redirect("/posts")