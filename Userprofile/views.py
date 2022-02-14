from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from Alluser.models import User
from .models import *
from .forms import *
import json
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def dashboard(request):
    Id = request.GET.get('pk')
    print(Id)
    userdetail = User.objects.get(pk=Id)
    alluser = User.objects.exclude(pk=Id)
    userBio = UserBio.objects.get(id=userdetail)
    suguser = UserBio.objects.all_notfriend(userdetail)[:5]
    friend = UserBio.objects.all_friend(userdetail)[:5]
    post = Post.objects.friendpost(userdetail).order_by('-created')[:10]
    mypost = Post.objects.filter(author=userBio).order_by('-created')[:1]
    for i in friend:
        print(i)
    #alluser = alluser.exclude(id__in=ListBox)
    return render(request,'index.html',{'user':userdetail,'userbio':userBio,'suggestuser':suguser,'friends':friend,'Post':post,'MyPost':mypost})
@login_required
def invite(request):
    Id = request.GET.get('pk')
    userdetail = User.objects.get(pk=Id)
    invite_req = UserBio.objects.allreceiver_invited(Id)[:7]
    suguser = UserBio.objects.all_notfriend(userdetail)[:5]
    friend = UserBio.objects.all_friend(userdetail)[:5]
    mypost = Post.objects.friendpost(userdetail).order_by('-created')[:1]
    return render(request,'invite.html',{'invite_req':invite_req,'MyPost':mypost,'suggestuser':suguser,'friends':friend})
@login_required
def friends(request):
    Id = request.GET.get('pk')
    userdetail = User.objects.get(pk=Id)
    suguser = UserBio.objects.all_notfriend(Id)[:5]
    friend = UserBio.objects.all_friend(Id)
    mypost = Post.objects.friendpost(userdetail).order_by('-created')[:1]
    return render(request,'friends.html',{'suggestuser':suguser,'friends':friend,'MyPost':mypost})
@login_required
def myprofile(request):
    Id = request.GET.get('pk')
    print(Id)
    userdetail = User.objects.get(pk=Id)
    alluser = User.objects.exclude(pk=Id)
    userBio = UserBio.objects.get(id=userdetail)
    suguser = UserBio.objects.all_notfriend(userdetail)[:5]
    friend = UserBio.objects.all_friend(userdetail)[:5]
    post = Post.objects.filter(author=userBio).order_by('-created')
    mypost = Post.objects.friendpost(userdetail).order_by('-created')[:1]
    for i in friend:
        print(i)
    #alluser = alluser.exclude(id__in=ListBox)
    return render(request,'home.html',{'user':userdetail,'userbio':userBio,'suggestuser':suguser,'friends':friend,'Post':post,'MyPost':mypost})
@login_required
def removefriend(request):
    if request.method == 'POST':
        user = request.POST.get('friendprofile')
        userid = User.objects.get(mobile=user)
        Id = request.GET.get('pk')
        frienduser = UserBio.objects.get(id=userid.id)
        userBio = UserBio.objects.get(id=Id)
        try : 
            rel = Relationship.objects.filter(sender=frienduser,receiver=userBio).delete()
            for i in rel:
                print(rel)
            url = '/dashboard/friends/?pk={}'.format(Id)
            return HttpResponseRedirect(url)
        except Relationship.DoesNotExist:
            Relationship.objects.filter(sender=userBio,receiver=frienduser).delete()
            for i in rel:
                print(rel)
            url = '/dashboard/friends/?pk={}'.format(Id)
            return HttpResponseRedirect(url)
@login_required
def addfriend(request):
    if request.method == 'POST':
        user = request.POST.get('friendprofile')
        userid = User.objects.get(mobile=user)
        Id = request.GET.get('pk')
        frienduser = UserBio.objects.get(id=userid.id)
        userBio = UserBio.objects.get(id=Id)
        if request.POST.get('accept') == None:
            Relationship.objects.update(sender=frienduser,receiver=userBio,status='accepted')
            url = '/dashboard/friends/?pk={}'.format(Id)
            return HttpResponseRedirect(url)
        else:
            Relationship.objects.get(sender=frienduser,receiver=userBio).delete()
            url = '/dashboard/friends/?pk={}'.format(Id)
            return HttpResponseRedirect(url)
@login_required
def sendfriend(request):
    if request.method == 'POST':
        user = request.POST.get('friendprofile')
        userid = User.objects.get(mobile=user)
        Id = request.GET.get('pk')
        frienduser = UserBio.objects.get(id=userid.id)
        userBio = UserBio.objects.get(id=Id)
        Relationship.objects.create(sender=userBio,receiver=frienduser,status='send')
        url = '/dashboard/friends/?pk={}'.format(Id)
        return HttpResponseRedirect(url)
@login_required
def pending(request):
    Id = request.GET.get('pk')
    userdetail = User.objects.get(pk=Id)
    invite_req = UserBio.objects.allsender_invited(Id)[:7]
    suguser = UserBio.objects.all_notfriend(userdetail)[:5]
    friend = UserBio.objects.all_friend(userdetail)[:5]
    mypost = Post.objects.friendpost(userdetail).order_by('-created')[:1]
    return render(request,'pending.html',{'invite_req':invite_req,'MyPost':mypost,'suggestuser':suguser,'friends':friend})
@login_required
def alluser(request):
    Id = request.GET.get('pk')
    userdetail = User.objects.get(pk=Id)
    alluser = UserBio.objects.all_user(Id)[:7]
    jsondata = json.dumps(list(UserBio.objects.all_user(Id).values()))
    suguser = UserBio.objects.all_notfriend(userdetail)[:5]
    friend = UserBio.objects.all_friend(userdetail)[:5]
    mypost = Post.objects.friendpost(userdetail).order_by('-created')[:1]
    return render(request,'alluser.html',{'alluser':alluser,'MyPost':mypost,'suggestuser':suguser,'friends':friend,'jsondata':jsondata})
@login_required
def friendprofile(request):
    if request.method == 'POST':
        try :
            user = request.POST.get('friendprofile')
            userid = User.objects.get(mobile=user)
            frienduser = UserBio.objects.get(id=userid.id)
            Id = request.GET.get('pk')
            print(Id)
            userdetail = User.objects.get(pk=Id)
            friendpro = User.objects.get(pk=userid.id)
            userBio = UserBio.objects.get(id=userid.id)
            suguser = UserBio.objects.all_notfriend(userdetail)[:5]
            friend = UserBio.objects.all_friend(userid.id)[:5]
            post = Post.objects.filter(author=frienduser).order_by('-created')
            mypost = Post.objects.friendpost(userid.id).order_by('-created')[:1]
            mutual = UserBio.objects.all_mutual(userdetail,userid.id)
            for i in mutual:
                print(i)
            #alluser = alluser.exclude(id__in=ListBox)
            return render(request,'friendprofile.html',{'user':userdetail,'friendpro':friendpro,'userbio':userBio,'suggestuser':suguser,'friends':friend,'Post':post,'MyPost':mypost})
        except UserBio.DoesNotExist or Relationship.DoesNotExist:
            user = request.POST.get('friendprofile')
            userid = User.objects.get(mobile=user)
            frienduser = UserBio.objects.get(id=userid.id)
            Id = request.GET.get('pk')
            print(Id)
            userdetail = User.objects.get(pk=Id)
            friendpro = User.objects.get(pk=userid.id)
            userBio = UserBio.objects.get(id=userid.id)
            suguser = UserBio.objects.all_notfriend(userdetail)[:5]
            post = Post.objects.filter(author=frienduser).order_by('-created')
            mypost = Post.objects.friendpost(userid.id).order_by('-created')[:1]
            mutual = UserBio.objects.all_mutual(userdetail,userid.id)
            for i in mutual:
                print(i)
            #alluser = alluser.exclude(id__in=ListBox)
            return render(request,'unknown.html',{'user':userdetail,'friendpro':friendpro,'userbio':userBio,'suggestuser':suguser,'friends':friend,'Post':post,'MyPost':mypost})
@login_required
def mutualfriend(request):
    if request.method == 'POST':
        user = request.POST.get('friendprofile')
        userid = User.objects.get(id=user)
        frienduser = UserBio.objects.get(id=userid.id)
        Id = request.GET.get('pk')
        print(Id)
        userdetail = User.objects.get(pk=Id)
        friendpro = User.objects.get(pk=userid.id)
        userBio = UserBio.objects.get(id=userid.id)
        suguser = UserBio.objects.all_notfriend(userdetail)[:5]
        friend = UserBio.objects.all_friend(userid.id)[:5]
        post = Post.objects.filter(author=frienduser).order_by('-created')
        mypost = Post.objects.friendpost(userid.id).order_by('-created')[:1]
        mutual = UserBio.objects.all_mutual(userdetail,userid.id)
        for i in mutual:
            print(i)
        #alluser = alluser.exclude(id__in=ListBox)
        return render(request,'mutual.html',{'user':userdetail,'friendpro':friendpro,'userbio':userBio,'suggestuser':suguser,'friends':friend,'Post':post,'MyPost':mypost,'mutual':mutual})
@login_required
def unknown(request):
    if request.method == 'POST':
        user = request.POST.get('friendprofile')
        userid = User.objects.get(mobile=user)
        frienduser = UserBio.objects.get(id=userid.id)
        Id = request.GET.get('pk')
        print(Id)
        userdetail = User.objects.get(pk=Id)
        friendpro = User.objects.get(pk=userid.id)
        userBio = UserBio.objects.get(id=userid.id)
        suguser = UserBio.objects.all_notfriend(userdetail)[:5]
        post = Post.objects.filter(author=frienduser).exclude(view='Friends').order_by('-created')
        mypost = Post.objects.friendpost(userid.id).order_by('-created')[:1]
        mutual = UserBio.objects.all_mutual(userdetail,userid.id)
        for i in mutual:
            print(i)
            #alluser = alluser.exclude(id__in=ListBox)
        return render(request,'unknown.html',{'user':userdetail,'friendpro':friendpro,'userbio':userBio,'suggestuser':suguser,'Post':post,'MyPost':mypost})
@login_required
def createpost(request):
    Id = request.GET.get('pk')
    userdetail = User.objects.get(pk=Id)
    userBio = UserBio.objects.get(id=userdetail)
    suguser = UserBio.objects.all_notfriend(userdetail)[:5]
    friend = UserBio.objects.all_friend(userdetail)[:5]
    post = Post.objects.filter(author=userBio).order_by('-created')
    mypost = Post.objects.friendpost(userdetail).order_by('-created')[:1]
    postform = PostForm()
    if request.method == 'POST':
        postform = PostForm(request.POST,request.FILES)
        if postform.is_valid():
            postform = postform.save(commit=False)
            postform.author = userBio
            print(postform)
            postform.save()
        return render(request,'home.html',{'Postform':postform,'user':userdetail,'userbio':userBio,'suggestuser':suguser,'friends':friend,'Post':post,'MyPost':mypost})
    return render(request,'createpost.html',{'Postform':postform,'user':userdetail,'userbio':userBio,'suggestuser':suguser,'friends':friend,'Post':post,'MyPost':mypost})
@login_required
def editprofile(request):
    Id = request.GET.get('pk')
    userdetail = User.objects.get(pk=Id)
    userBio = UserBio.objects.get(id=userdetail)
    suguser = UserBio.objects.all_notfriend(userdetail)[:5]
    friend = UserBio.objects.all_friend(userdetail)[:5]
    post = Post.objects.filter(author=userBio).order_by('-created')
    mypost = Post.objects.friendpost(userdetail).order_by('-created')[:1]
    postform = UserBioForm(instance=userBio)
    if request.method == 'POST':
        postform = UserBioForm(request.POST,instance=userBio)
        if postform.is_valid():
            postform = postform.save(commit=False)
            postform.author = userBio
            print(postform)
            postform.save()
        return render(request,'home.html',{'Postform':postform,'user':userdetail,'userbio':userBio,'suggestuser':suguser,'friends':friend,'Post':post,'MyPost':mypost})
    return render(request,'editprofile.html',{'Postform':postform,'user':userdetail,'userbio':userBio,'suggestuser':suguser,'friends':friend,'Post':post,'MyPost':mypost})
