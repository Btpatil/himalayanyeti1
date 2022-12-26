from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth  import authenticate, login, logout
from django.contrib.auth.models import User
from . forms import articleform
from mainapp.models import article, label, categories

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required

# Global variables

labelvalue=0                            #used in help function to keep track of filter

# Create your views here.

def home(request):
    return render(request, "mainapp/index.html")

def donation(request):
    return render(request, "mainapp/donation.html")

def help(request):
    contex={}
    global labelvalue
    labelvalue = int(request.GET.get('label', labelvalue))
    if labelvalue==0:
        object_list = article.objects.filter(category=5).order_by('-postdate') # category 5 belongs to help
    else:
        object_list = article.objects.filter(label=labelvalue).order_by('-postdate')

    page_num = request.GET.get('page', 1)
    paginator = Paginator(object_list, 6) # 6 article per page
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    contex['page_obj']=page_obj
    labellist = label.objects.filter(parentcategory=5) # parentcategory 5 belongs to help
    contex['labellist']=labellist
    contex['labelvalue']=labelvalue

    return render(request, "mainapp/help.html", contex)

def userlogin(request):
    contex={'Alert':''}
    if request.method=='POST':
        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username= username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                contex['Alert']="Login Credentials could not match/ wrong credentials"
        return render(request, "mainapp/login.html", contex)     
    return render(request, "mainapp/login.html", contex)

def userlogout(request):
    request.session.clear()
    logout(request)
    return redirect(home)

def createuser(request):
    pass

@login_required(login_url='/userlogin')
def addarticle(request):
    contex={}
    if request.method == 'POST':
        form = articleform(request.POST,request.FILES)
        if form.is_valid():
            form.author = request.user.id     
            lbl = label.objects.get(lid=request.POST['label'])
            if int(request.POST['category']) == int(lbl.parentcategory.cid):
                form.save()
                return redirect(help)
            else:
                contex['Alert']="Input category and label category dont match please create new or change accordingly"
    artform = articleform()
    contex['artform']=artform
    return render(request, "mainapp/addarticle.html", contex)

def about(request):
    return render(request, "mainapp/about.html")

@login_required(login_url='/userlogin')
def deletearticle(request, num):
    instance = article.objects.get(bid=num)
    instance.delete()
    return redirect(help)

def viewarticle(request, num):
    contx={}
    instance = article.objects.get(bid=num)
    contx['article']=instance
    return render(request, "mainapp/viewarticle.html", contx)

@login_required(login_url='/userlogin')
def updatearticle(request, pk):
    contex={}
    blog_post = get_object_or_404(article, bid=pk)
    if request.method == 'POST':
        form = articleform(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            lbl = label.objects.get(lid=request.POST['label'])
            if int(request.POST['category']) == int(lbl.parentcategory.cid):
                form.save()
                return redirect('viewarticle', num=pk)
            else:
                contex['Alert']="Input category and label category dont match please create new or change accordingly"
    
    form = articleform(instance=blog_post)
    contex['artform']=form
    return render(request, "mainapp/addarticle.html", contex)