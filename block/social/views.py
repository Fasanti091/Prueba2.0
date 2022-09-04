from django.shortcuts import render,redirect,get_object_or_404
from social.models import *
from social.forms import PostForm, UserRegisterForm,UserEditForm,AvatarForm
from django.contrib import messages
from django.contrib.auth.models import User
from web.views import *
from django.contrib.auth.decorators import login_required

def feed(request):
    posts = Post.objects.all()
    
    context = {'posts':posts}
    return render(request,'social/feed.html',context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado')
            return render(request, 'web/index.html')          
    else:
        form = UserRegisterForm()        
    context = { 'form': form }    
    return render(request, 'social/register.html',context)


def post(request):
    current_user = get_object_or_404(User,pk=request.user.pk)
    if request.method =='POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            messages.success(request,'Post Creado')
            return redirect('feed')
    else:
        form=PostForm()
    return render(request,'social/post.html',{'form':form})
        
        

def profile(request,username=None):
    current_user=request.user
    if username and username != current_user.username:
        user=User.objects.get(username=username)
        posts =user.posts.all()
    else:
        posts = current_user.posts.all()
        user = current_user
    return render(request,'social/profile.html',{'user':user,'posts':posts})


@login_required
def editPerfil(request):
     if request.method == "GET":
        form = UserEditForm()
        return render(request,"social/editar_perfil.html",{"form":form})
     else:
        form = UserEditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            usuario = request.user
            usuario.email = data["email"]
            usuario.password1 = data["password1"]
            usuario.password2 = data["password2"]
            usuario.Image
            
            usuario.save()
        return redirect("inicio")
    
@login_required
def agregar_avatar(request):
    if request.method =="GET":
        form = AvatarForm()
        contexto = {"form": form}
        return render(request,"social/avatar.html",contexto)
    else:
        form = AvatarForm(request.POST,request.FILES)
        if form.is_valid():
            data=form.cleaned_data
            
            user = User.objects.filter(username=request.user.username).first()
            avatar= Avatar(user=user,imagen=data["imagen"])
            avatar.save()
        return redirect("profile")    
            
    
   