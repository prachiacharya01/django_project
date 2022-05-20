from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from requests import request
from .forms import UserRegistrationFrom, UserUpdateForm, ProfileUpdateForm
from blog.models import Post

# serializer
from rest_framework.response import Response
from rest_framework.views import APIView 
from .serializers import ProfileSerializer
from rest_framework.generics import ListAPIView, CreateAPIView
# serializer views --cbv

class ProfileSerializerView(CreateAPIView):
    serializer_class = ProfileSerializer
    # queryset = 
    def post(self,request):
        return self.create(request)
    def get(self,request):
        return 




# django views
def register(request):
    if request.method == 'POST':
        form = UserRegistrationFrom(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request,f'Account created for {username}!')
            return redirect('blog-login')

    else:
        form = UserRegistrationFrom()
        return render(request,'user/register.html', {'form':form})
        
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        # print(instance=request.user)
        p_form  = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your account has been updated')
            return redirect('profile')
            
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)
    
    post_ids = Post.objects.all().filter(author_id = request.user.id)
    print(post_ids)
    context = {
        'u_form' : u_form,
        'p_form' : p_form,
        'post_ids' : post_ids
    }

    return render(request,'user/profile.html',context)


