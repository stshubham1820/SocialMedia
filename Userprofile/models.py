from django.db import models
from matplotlib.style import available
from Alluser.models import User
from django.db.models import Q
# Create your models here.
class UserBioManager(models.Manager):
    def allreceiver_invited(self,sender):
        All = UserBio.objects.all().exclude(id=sender)
        profile = UserBio.objects.get(id=sender)
        Qs = Relationship.objects.filter(Q(receiver=profile))
        send = []
        for i in Qs:
            if i.status == 'send':
                send.append(i.receiver)
                send.append(i.sender)
        available = [pro for pro in All if pro in send]
        return available
    def allsender_invited(self,sender):
        All = UserBio.objects.all().exclude(id=sender)
        profile = UserBio.objects.get(id=sender)
        Qs = Relationship.objects.filter(Q(sender=profile))
        send = []
        for i in Qs:
            if i.status == 'send':
                send.append(i.receiver)
                send.append(i.sender)
        available = [pro for pro in All if pro in send]
        return available
    def all_friend(self,sender):
        All = UserBio.objects.all().exclude(id=sender)
        profile = UserBio.objects.get(id=sender)
        Qs = Relationship.objects.filter(Q(sender=profile)|Q(receiver=profile))
        accepted = []
        for i in Qs:
            if i.status == 'accepted':
                accepted.append(i.receiver)
                accepted.append(i.sender)
        available = [pro for pro in All if pro in accepted]
        return available
    def all_notfriend(self,sender):
        All = UserBio.objects.all().exclude(id=sender)
        profile = UserBio.objects.get(id=sender)
        Qs = Relationship.objects.filter(Q(sender=profile)|Q(receiver=profile))
        accepted = []
        for i in Qs:
            accepted.append(i.receiver)
            accepted.append(i.sender)
        available = [pro for pro in All if pro not in accepted]
        return available
    def all_user(self,me):
        profile = UserBio.objects.all().exclude(id=me)
        return profile
    def all_mutual(self,me,friend):
        All = UserBio.objects.all().exclude(id=me)
        myprofile = UserBio.objects.get(id=me)
        friendprofile = UserBio.objects.get(id=friend)
        Qsme = Relationship.objects.filter(Q(sender=myprofile)|Q(receiver=myprofile))
        Qsfriend = Relationship.objects.filter(Q(sender=friendprofile)|Q(receiver=friendprofile))
        acceptedme = []
        acceptedfriend = []
        for i in Qsme:
            if i.status == 'accepted':
                acceptedme.append(i.receiver)
                acceptedme.append(i.sender)
        for i in Qsfriend:
            if i.status == 'accepted':
                acceptedfriend.append(i.receiver)
                acceptedfriend.append(i.sender)
        available = [pro for pro in All if pro in acceptedfriend and pro in acceptedme]
        return available
class UserBio(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True,unique=True)
    name = models.CharField(max_length=50,null=True,blank=True)
    bio = models.TextField(null=True,blank=True)
    facebook = models.URLField(max_length=200,null=True,blank=True)
    instagram = models.URLField(max_length=200,null=True,blank=True)
    twitter = models.URLField(max_length=200,null=True,blank=True)
    friends = models.ManyToManyField(User,related_name='friends',blank=True)

    objects = UserBioManager()

    def get_friends(self):
        return self.friends.all()
    def get_friends_no(self):
        return self.friends.all().count()
    def __str__(self) -> str:
        return str(self.id)
STATUS_CHOICES=(
    ('send','send'),
    ('accepted','accepted'),
)
VIEW_CHOICES=(
    ('All','All'),
    ('Friends','Friends')
)
class RelationshipManager(models.Manager):
    def invitations_received(self,receiver):
        qs = Relationship.objects.filter(receiver=receiver,status='send')
        return qs

class Relationship(models.Model):
    sender = models.ForeignKey(UserBio,on_delete=models.CASCADE,related_name='sender')
    receiver = models.ForeignKey(UserBio,on_delete=models.CASCADE,related_name='receiver')
    status = models.CharField(max_length=8,choices=STATUS_CHOICES)

    objects = RelationshipManager()

    def __str__(self) -> str:
        return f"{self.sender}"

class PostManager(models.Manager):
    def friendpost(self,user):
        All = UserBio.objects.all()
        profile = UserBio.objects.get(id=user)
        Qs = Relationship.objects.filter(Q(sender=profile)|Q(receiver=profile))
        accepted = []
        for i in Qs:
            if i.status == 'accepted':
                accepted.append(i.receiver)
                accepted.append(i.sender)
        available = [pro for pro in All if pro in accepted]
        qs = Post.objects.filter(author__in=available)
        return qs

class Post(models.Model):
    author = models.ForeignKey(UserBio,on_delete=models.CASCADE,related_name='user')
    title = models.CharField(max_length=50,null=True,blank=True)
    body = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='media',null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    view = models.CharField(max_length=8,choices=VIEW_CHOICES)
    objects = PostManager()

    def __str__(self) -> str:
        return f"{self.author}"