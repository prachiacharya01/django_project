import time
from django.http import HttpResponse,HttpResponseRedirect, QueryDict
import razorpay
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from requests import request
from .models import Post 
from .models import comment
from django.contrib.auth.models import User
from blog.forms import CommentForm
from django.urls import reverse

# serializers -------------------------------------------------------------------------------------------------------------
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import PostSerializer
from rest_framework import status
# serializer views ----------------------------------------------------------------------------------------------------------
class hello(APIView):
    
    def get(self,request):
        return Response({"message":"hey"})


class PostSerialzerView(viewsets.ViewSet):
    def list(self, request):
        queryset = Post.objects.all()
        # breakpoint()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request,pk = None):
        get_obj = Post.objects.get(id = pk)
        get_obj.delete()
        return Response({"message":"Data Deleted"})
    
    def partial_update(self, request, pk = None):
        get_obj = Post.objects.get(id = pk)
        serializer = PostSerializer(get_obj, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def create(self, request):
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Data Created"},serializer.data)
        return Response(serializer.errors)

    def update(self, request, pk = None):
        get_obj = Post.objects.get(id = pk)
        serializer = PostSerializer(get_obj, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def retrieve(self, request, pk = None):
        if pk != None:
            get_obj = Post.objects.get(id = pk)
            serializer = PostSerializer(get_obj)
            return Response(serializer.data)



    

# django views----------------------------------------------------------------------------------------------------------------
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    ordering = ['-date']

    def get_queryset(self):
        queryset = Post.objects.select_related('author').all()
        return queryset

class PostDetailView(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        liked = 0
        self.object = self.get_object()
        P = Post.objects.filter(id = self.object.id).first()
        print(P)
        totallikes= P.likes.through.objects.filter(post_id = kwargs['pk']).count()
        is_liked:bool = P.likes.through.objects.filter(post_id = kwargs['pk'],user_id = request.user.id).exists()

        # start = time.time()

        # post_set = P.likes.through.objects.filter(post_id = kwargs['pk'])
        # user_set = P.likes.through.objects.filter(user_id = request.user) 
        # liked = 0      
        # likes__kwargs  
        # if totallikes: 
        #     flag= 0
        #     for i in post_set:
        #         for j in user_set: 
        #             # print(i.id,j.id)              
        #             if i.id == j.id :
        #                 liked = 1
        #                 flag = 1
        #                 break
        #             else:
        #                 liked = 0
        #         if flag == 1:
        #             break
        # else:
        #     liked = 0
        # end = time.time()
        # print(end - start)
        context = {'object':self.object,"totallikes":totallikes,"clicked":is_liked}
        return self.render_to_response(context)

    def post(self,request, *args, **kwargs):
        liked = 0
        self.object = self.get_object()
        P = Post.objects.filter(id = self.object.id).first()
        obj = P.likes.through.objects.create(user_id = request.user.id, post_id = kwargs['pk'])
        obj.save()
        totallikes= P.likes.through.objects.filter(post_id = kwargs['pk']).count()
        is_liked:bool = P.likes.through.objects.filter(post_id = kwargs['pk'],user_id = request.user.id).exists()
        # if is_liked:
        #     liked = 1
        # post_set = P.likes.through.objects.filter(post_id = kwargs['pk'])
        # user_set = P.likes.through.objects.filter(user_id = request.user) 
        # start = time.time()
        # if totallikes: 
        #     flag= 0
        #     for i in post_set:
        #         for j in user_set: 
        #             # print(i.id,j.id)              
        #             if i.id == j.id:
        #                 liked = 1
        #                 flag = 1
        #                 break
        #             else:
        #                 liked = 0
        #         if flag == 1:
        #             break
        # else:
        #     liked = 0
        # end  = time.time()
        # print(end - start)
        context = {'object':self.object,"totallikes":totallikes,"clicked":is_liked}
        return self.render_to_response(context)

# def LikeView(request,pk): 
#     post = get_object_or_404(Post, id = request.POST.get('post_id'))
#     post.likes.add(request.user)
#     return HttpResponseRedirect(reverse('blog-detail'),args=[str(pk)])

# def DisLikeView(request,pk): 
#     post = get_object_or_404(Post, id = request.POST.get('post_id'))
#     post.likes.delete(request.user)
#     return render(request,'blog/post_detail.html')

def about(request):
    return render(request,'blog/about.html',{'title' : "About"})

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title' ,'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
        
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        print(post.id)
        if self.request.user == post.author:
            print("verified")
            return True
        return False

def login(request):
    return render(request,'blog/login.html')

def search(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        post = Post.objects.filter(title__contains=search)
    return render(request,'blog/search.html',{'post':post})

def donate(request):
    if request.method == 'POST':
        client = razorpay.Client(auth=("rzp_test_fxvoAhL8OcTjKV", "4uv80tu5DF55S9z5rrrSjSvQ"))
        DATA = {    
            "amount": 100,    
            "currency": "INR",    
        }
        client.order.create(data=DATA)
    return render(request,'blog/donate.html')

class desc1(CreateView):

    def get(self,request,*args,**kwargs):
        print(kwargs['pk'])
        post_obj = Post.objects.get(id = kwargs['pk'])
        form = CommentForm              
        comment_obj = comment.objects.filter(post_id = kwargs['pk'])
        if comment_obj:

            context = {'form' : form, 'object':post_obj, 'comment_obj':comment_obj}
        else:
             context = {'form' : form, 'object':post_obj}

        return render(request,'blog/desc.html',context = context)

    def post(self,request,*args,**kwargs):
        
        form = CommentForm(request.POST)
        post_obj = Post.objects.get(id = kwargs['pk'])
        print('post_obj---------------------------------',post_obj)
        print("request.POST--------------------------",request.POST)
        current_user_blog_comment = comment.objects.create(describ = request.POST['describ'], post = post_obj, commentor = request.user)
        current_user_blog_comment.save()
        comment_obj = comment.objects.filter(post_id = kwargs['pk'])
        context = {'form' : form,'object':post_obj,"comment_obj" : comment_obj}

        return render(request,'blog/desc.html',context = context,)

# def desc(request):
#     return HttpResponse(request, 'blog/desc.html')

# def home(request):

#     context = {
#         'posts' : Post.objects.all()
#     }
#     return render(request,'blog/home.html',context)
# class home(self,View):
#     def h(request):
#         'posts' : Post.objects.all()     
#         return render(request,'blog/home.html',self.posts)
