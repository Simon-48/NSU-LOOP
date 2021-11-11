from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Post, Like
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create views here.
@login_required
def post_comment_create_and_list_view(request):
    """
    This method will create a post request on two separate forms post form and comment form and upon 
    successfull insertion, it will update the form and will show in the post content or comment body.
    This method will only load this page if the user is logged in.
       
    :param name: request - used to generate responses(Http) depending on the request that it receives
    :param type: HttpResponse
    :return: returns posts page
    """
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

    # initials
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False

    profile = Profile.objects.get(user=request.user)

    if 'submit_p_form' in request.POST:
        print(request.POST)
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_added = True

    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()


    context = {
        'qs': qs,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
        'post_added': post_added,
    }

    return render(request, 'posts/main.html', context)

@login_required
def like_unlike_post(request):
    """
    This method will create a like or unlike request on posts and upon successfull insertion, it will 
    update the like or unlike. If the post status is liked will update it to unliked otherwise update 
    it to liked. If the post previouly existed and its status is liked then will update it to unliked 
    othwise will update it to liked.
    This method will only load this page if the user is logged in.
       
    :param name: request - used to generate responses(Http) depending on the request that it receives
    :param type: HttpResponse
    :return: redirect the posts page
    """
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

            post_obj.save()
            like.save()


    return redirect('posts:main-post-view')

class PostDeleteView(DeleteView):
    """
    PostDeleteView inherits from the DeleteView. These allow you to structure your views and reuse 
    code by harnessing inheritance. All views inherit from the View class, which handles linking the 
    view into the URLs, HTTP method dispatching and other common features.

    """
    model = Post
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:main-post-view')

    def get_object(self, *args, **kwargs):
        """
        This method followed a claas based view method. If the user is the owner of the post only then 
        that particular user will able to delete the post, first that particular user will able to go 
        into given template link and able to delete the post and will get back to the attached success 
        url page after deletation. However if the user is not the owner of the post then the user will 
        not be able to delete the post even if he has the url of the post. For this case it will show a 
        error message. 
       
        :param name: self - used to access the attributes and methods of the class in python
        :param type: reference
        :return: str
        :param name: *args - used to pass an arbitrary number of arguments to a function
        :param type: pass variable
        :return: returns variable number
        :param name: **kwargs - used to pass key-value parameters to the function
        :param type: pass variable
        :return: returns key-value parameters
        """
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You need to be the author of the post in order to delete it')
        return obj

class PostUpdateView(UpdateView):
    """
    PostUpdateView inherits from the UpdateView. These allow you to structure your views and 
    reuse code by harnessing inheritance. All views inherit from the View class, which handles
    linking the view into the URLs, HTTP method dispatching and other common features.

    """
    form_class = PostModelForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:main-post-view')

    def form_valid(self, form):
        """
        This method followed a claas based view method. If the user is the owner of the post only 
        then that particular user will able to update the post, first that particular user will able
        to go into given template link and able to update the post and will get back to the attached 
        success url page after updating the post. However if the user is not the owner of the post then 
        the user will not be able to update the post even if he has the url of the post. For this case 
        it will show a error message. 
       
        :param name: self - used to access the attributes and methods of the class in python
        :param type: reference
        :return: str
        :param name: form - used to take a form
        :param type: take form
        :return: returns the form
        """
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "You need to be the author of the post in order to update it")
            return super().form_invalid(form)