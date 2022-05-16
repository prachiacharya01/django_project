from django.http import HttpResponse,HttpResponseRedirect
import razorpay
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from .models import Post 
from .models import comment
from django.contrib.auth.models import User
from blog.forms import CommentForm
from django.urls import reverse

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    ordering = ['-date']

class PostDetailView(DetailView):
    model = Post
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        P = Post.objects.filter(id = self.object.id).first()
        print(P)
        totallikes= P.likes.through.objects.filter(post_id = kwargs['pk']).count()
        post_set = P.likes.through.objects.filter(post_id = kwargs['pk'])
        user_set = P.likes.through.objects.filter(user_id = request.user) 
        liked = 0        
        if totallikes: 
            flag= 0
            for i in post_set:
                for j in user_set: 
                    print(i.id,j.id)              
                    if i.id == j.id :
                        liked = 1
                        flag = 1
                        break
                    else:
                        liked = 0
                if flag == 1:
                    break
        else:
            liked = 0

        context = {'object':self.object,"totallikes":totallikes,"clicked":liked}
        return self.render_to_response(context)

    def post(self,request,*args,**kwargs):

        self.object = self.get_object()
        P = Post.objects.filter(id = self.object.id).first()
        obj = P.likes.through.objects.create(user_id = request.user.id, post_id = kwargs['pk'])
        obj.save()
        totallikes= P.likes.through.objects.filter(post_id = kwargs['pk']).count()
        post_set = P.likes.through.objects.filter(post_id = kwargs['pk'])
        user_set = P.likes.through.objects.filter(user_id = request.user) 
        if totallikes: 
            flag= 0
            for i in post_set:
                for j in user_set: 
                    print(i.id,j.id)              
                    if i.id == j.id:
                        liked = 1
                        flag = 1
                        break
                    else:
                        liked = 0
                if flag == 1:
                    break
        else:
            liked = 0
        context = {'object':self.object,"totallikes":totallikes,"clicked":liked}
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
    fields = ['title','content','likes']

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
        post = Post.objects.all().filter(title__contains=search)
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
