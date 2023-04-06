from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import resolve
from django.db.models import Q
from .models import *
from django.http import HttpResponseBadRequest

def custom_400(request):
    return render(request, '400.html', status=400)


def home(request):    
    if(request.user.is_authenticated):
        import datetime
        today = datetime.date.today()
        curryr = f'{(today.strftime("%Y"))}'
        curryr = int(curryr[2:len(curryr)])
        mailyr = request.user.email
        mailyr = mailyr[(mailyr).find('@kongu.edu')-5:(mailyr).find('@kongu.edu')-3]
        isspl=False
        yr=0
        splpost=[]
        if(mailyr.isdigit()):
            print('...................')
            isspl=True
            yr=int(curryr)-int(mailyr)
            if(yr==1):
                splpost=Article.objects.filter(forfirst=True).filter(status='published', visibility='public').order_by('-dt_published')[:3]
            if(yr==2):
                splpost=Article.objects.filter(forsecond=True).filter(status='published', visibility='public').order_by('-dt_published')[:3]
            if(yr==3):
                splpost=Article.objects.filter(forthird=True).filter(status='published', visibility='public').order_by('-dt_published')[:3]
            if(yr==4):
                splpost=Article.objects.filter(forfinal=True).filter(status='published', visibility='public').order_by('-dt_published')[:3]
            if(len(splpost)==0):
                isspl=False
            print("=>",len(splpost), yr)
            allOfficialPosts=Article.objects.filter(isofficial=True, isspl=False).filter(status='published', visibility='public').order_by('-dt_published')[:3]
            allHighlightPosts=Article.objects.filter(highlight=True, isspl=False).filter(status='published', visibility='public').order_by('-dt_published')[:3]
            allposts=Article.objects.filter(highlight=False, isofficial=False, isspl=False).filter(status='published', visibility='public').order_by('-dt_published')
            context={'allOfficialPosts':allOfficialPosts, 'allHighlightPosts':allHighlightPosts, 'allposts':allposts, 'isspl':isspl, 'yr':yr, 'splpost':splpost}
            return render(request, 'index.html', context)
    allOfficialPosts=Article.objects.filter(isofficial=True, isspl=False).filter(status='published', visibility='public').order_by('-dt_published')[:3]
    allHighlightPosts=Article.objects.filter(highlight=True).filter(status='published', visibility='public').order_by('-dt_published')[:3]
    allposts=Article.objects.filter(highlight=False, isofficial=False).filter(status='published', visibility='public').order_by('-dt_published')[:20]
    context={'allOfficialPosts':allOfficialPosts, 'allHighlightPosts':allHighlightPosts, 'allposts':allposts}
    print(allHighlightPosts, allOfficialPosts, allposts)
    
    return render(request, 'index.html', context)


def newpost(request):
    try:
        isspr = request.user.is_superuser
        if(request.method=='POST'):
            title = request.POST.get('title', None)
            content = request.POST.get('content', None)
            tags = [x.strip() for x in request.POST.get('tags', None).split(',')]
            slug = request.POST.get('slug', None)
            saveas = request.POST.get('saveas', None)
            isofficial = request.POST.get('isofficial', None)
            forall = request.POST.get('all', None)
            if(forall!='on'):
                is1 = request.POST.get('option1', None)=='on'
                is2 = request.POST.get('option2', None)=='on'
                is3 = request.POST.get('option3', None)=='on'
                is4 = request.POST.get('option4', None)=='on'
                print("is1 -", is1)
                print("is2 -", is2)
                print("is3 -", is3)
                print("is4 -", is4)
            else:
                is1, is2, is3, is4 = True, True, True, True
            if(not(is1==True and is1==True and is1==True and is1==True and is1==True)):
                isspl=True
            if(isspl and request.user.is_superuser):
                alluser = User.objects.all()
                mails = []
                for x in alluser:
                    if(x.email.__contains__('.20') and is3):
                        mails.append(x.email)
                    elif(x.email.__contains__('19') and is4):
                        mails.append(x.email)
                    elif(x.email.__contains__('21') and is2):
                        mails.append(x.email)
                    elif(x.email.__contains__('22') and is1):
                        mails.append(x.email)
                print('-------------->', mails)
                send_mail(
                    f"New Special Post - {title}",
                    f"New Post on {title} is added by admin http://127.0.0.1:8000/blog/{slug}/",
                    'kecianblogger@gmail.com',
                    mails,
                    fail_silently=False
                )
            official=False
            highlight=False
            if(isofficial=="official"):
                official=True
            if(isofficial=="highlight"):
                highlight=True
            iskecian = False
            if(request.user.email.endswith('@kongu.edu')):
                iskecian=True
            if(isspr==False):
                is1=True
                is2=True
                is3=True
                is4=True
            else:
                pass
            newarticle = Article(title=title, content=content, author=User.objects.get(username=request.user.username), status=saveas, slug=slug, iskecian=iskecian, isofficial=official, highlight=highlight, forfirst=is1, forsecond=is2, forthird=is3, forfinal=is4, isspl=isspl)
            newarticle.save()
            for tag in tags:
                newarticle.tags.add(tag)
            thome=reverse('home')
            return redirect(thome)
        allslugs = [post.slug for post in Article.objects.all()]
        print(allslugs)
        context={'allslugs':allslugs}
        return render(request, 'add_post.html', context)
    except Exception as e:
        print(e)
        return render(request, 'error.html', {'err':'The content is too large please reduce the content to 2000kb'})


def viewpost(request, slug):
    if(request.user.is_authenticated):
        import datetime
        today = datetime.date.today()
        curryr = f'{(today.strftime("%Y"))}'
        curryr = int(curryr[2:len(curryr)])
        mailyr = request.user.email
        mailyr = mailyr[(mailyr).find('@kongu.edu')-5:(mailyr).find('@kongu.edu')-3]
        isspl=False
        yr=0
        is1, is2, is3, is4 = False, False, False, False
        if(mailyr.isdigit()):
            isspl=True
            yr=int(curryr)-int(mailyr)
            if(yr==1):
                is1=True
            if(yr==2):
                is2=True
            if(yr==3):
                is3=True
            if(yr==4):
                is4=True
        content=[]
        content=Article.objects.get(slug=slug)
        print(yr)
        if(yr==2):
            if(content.isspl==True and content.forsecond==True):
                # print(content.forsecond)
                content=content
            elif(content.isspl==False and content.isofficial==True):
                # print(content.forsecond)
                content=content
            else:
                content=None
        if(yr==3):
            if(content.isspl==True and content.forthird==True):
                # print(content.forthird)
                content=content
            elif(content.isspl==False and content.isofficial==True):
                # print(content.forthird)
                content=content
            else:
                content=None
        # if(yr==2 and isspl==True and content.forsecond==False):
        #     print('...')
        #     content=None
            
        if(content is None):
            return render(request, 'error.html', {'err':'You don\'t have that access'})
        bordercolor=''
        context={}
        followbtn=True
        isfollowing=False
        allf = [x.followed for x in Follow.objects.filter(follower=request.user)]
        isliked=False
        if(ArticleLike.objects.filter(user=User.objects.filter(username=request.user.username).first(), article=content).first()):
            isliked=True
        print(isliked)
        alllikes = ArticleLike.objects.filter(article=content)
        print(alllikes)
        likecount=0
        if(alllikes):
            likecount=len(alllikes)
        if(request.user.username==content.author.username):
            followbtn=False
        if(content.author in allf):
            isfollowing=True
        if(content==None):
            context={'content':'Opps! No such content published yet... 😮'}
        elif((content.status=='published' and content.visibility=='public') or (content.status=='published' and content.visibility=='private' and content.author.username==request.user.username) or (content.status=='draft' and content.visibility!='deleted' and content.author.username==request.user.username)):
            if(content.author.email.endswith("@kongu.edu")):
                bordercolor='rgb(247, 250, 83)'
            allcomments = Comment.objects.filter(article=Article.objects.get(slug=slug)).order_by('cmt_date')
            context={'content':content, 'bordercolor':bordercolor, 'followbtn':followbtn, 'isfollowing':isfollowing, 'isliked':isliked, 'likecount':likecount, 'comment':allcomments}
        else:
            context={'content':'404 ERROR : Content not available might be removed/private 🤔'}
        return render(request, 'viewpost.html', context)
    return redirect('login')
    

def allmypublicpost(request):
    if(request.user.is_authenticated):
        context={}
        allmypost=Article.objects.filter(author=request.user.id, visibility='public')
        context={'allmypublicpost':allmypost}
        return render(request, 'allmypublicpost.html', context)
    else:
        tlogin=reverse('login')
        return redirect(tlogin)

def allmyprivatepost(request):
    if(request.user.is_authenticated):
        context={}
        allmypost=Article.objects.filter(author=request.user.id, visibility='private')
        context={'allmyprivatepost':allmypost}
        return render(request, 'allmyprivatepost.html', context)
    else:
        tlogin=reverse('login')
        return redirect(tlogin)

def makepublicprivate(request, slug):
    if(request.user.is_authenticated):
        article=Article.objects.get(slug=slug)
        if(request.user.username==article.author.username):
            if(article.visibility=='public'):
                article.visibility='private'
                article.save()
                return redirect(reverse('allmypublicpost'))
            else:
                article.visibility='public'
                article.save()
                return redirect(reverse('allmyprivatepost'))
        else:
            return render(request, 'error.html', {'err':'You don\'t have an access to it...'})
    else:
        tlogin=reverse('login')
        return redirect(tlogin)


def deletePost(request, slug):
    if(request.user.is_authenticated):
        if(request.user.username == Article.objects.get(slug=slug).author.username):
            redirectlink=''
            curr = Article.objects.get(slug=slug)
            if(curr.status=='public'):
                redirectlink='allmypublicpost'
            else:
                redirectlink='allmyprivatepost'
            curr.visibility='deleted'
            curr.save()
            return redirect(reverse(redirectlink))
        else:
            return render(request, 'error.html', {'err':'ERROR 404 : You can\'t perform this action... 🤔'})
    else:
        tlogin = reverse('login')
        return redirect(tlogin)


def search(request):
    query = request.GET.get("q")
    if query:
        allpost = Article.objects.filter(
            Q(title__icontains=query) |
            Q(tags__name__in=[query])
        ).distinct().filter(status="published", visibility="public")
    else:
        allpost = Article.objects.none()
    print(allpost)
    return render(request, "index.html", {"allPost": allpost})


@login_required
def follow_unfollow(request, username):
    user = get_object_or_404(User, username=username)
    follow, created = Follow.objects.get_or_create(follower=request.user, followed=user)

    if not created:
        follow.delete()
        action = "unfollowed"
    else:
        action = "followed"

    return redirect("home")

@login_required
def like_unlinked(request, slug):
    article = get_object_or_404(Article, slug=slug)
    like, created = ArticleLike.objects.get_or_create(user=request.user, article=article)

    if not created:
        like.delete()
        action = "liked"
    else:
        action = "unlinked"

    return redirect("home")



def validateReport(request):
    reports = ArticleReport.objects.all()
    tart=[]
    for x in reports:
        if(x.article not in tart):
            tart.append(x.article)
    d={}
    lst=["Violent or repulsive content","Harassment or bullying","Harmful or dangerous acts","Misinformation","Child Abuse","Sexual Content","Infringes my rights","Promotes Terrorism","Spam or Misleading"]
    for x in tart:
        td={}
        for y in reports:
            if(x==y.article):
                if(y.reason not in td):
                    td[y.reason]=[y.user]
                else:
                    td[y.reason]+=[y.user]  
        d[x]=td
    context={'allreport':d}
    for x in d:
        print(x.slug)
    return render(request, 'validateReport.html', context)


def deleteArticle(request, slug):
    if(request.user.is_superuser):
        currArticle = Article.objects.get(slug=slug)
        currArticle.visibility='deleted'
        currArticle.save()
        currReport = ArticleReport.objects.filter(article=Article.objects.get(slug=slug ))
        for x in currReport:
            x.delete()
        return redirect(reverse('validateReport'))
    else:
        return render(request, 'error.html', {'err':'You dont have this access'})

def banUser(request, slug):
    if(request.user.is_superuser):
        currUser = User.objects.get(username=Article.objects.get(slug=slug).author.username)
        
        # sending mail
        send_mail(
            "Accout banned KEConnect...",
            f"Your account has been banned, since you have violated the terms and conditions of KEConnect",
            'kecianblogger@gmail.com',
            [currUser.email],
            fail_silently=False
        )
        
        currUser.is_active=False
        currUser.save()
        currArticle = Article.objects.get(slug=slug)
        currArticle.visibility='deleted'
        currArticle.save()
        currReport = ArticleReport.objects.filter(article=Article.objects.get(slug=slug))
        for x in currReport:
            x.delete()
        
        
        return redirect(reverse('validateReport'))
    else:
        return render(request, 'error.html', {'err':'You dont have this access'})

def reportPost(request, slug, id):
    id=id-1
    lst=["Violent or repulsive content","Harassment or bullying","Harmful or dangerous acts","Misinformation","Child Abuse","Sexual Content","Infringes my rights","Promotes Terrorism","Spam or Misleading"]
    print("==>",slug, lst[id])
    trep = ArticleReport.objects.filter(user=User.objects.get(username=request.user.username), article=Article.objects.get(slug=slug), reason=lst[id])
    print(len(trep))
    if(len(trep)==0):
        newReport = ArticleReport(user=User.objects.get(username=request.user.username), reason=lst[id], article=Article.objects.get(slug=slug))
        newReport.save()
    return redirect(f"/blog/{slug}/")

def ignoreReport(request, slug):
    currReport = ArticleReport.objects.filter(article=Article.objects.get(slug=slug ))
    for x in currReport:
        x.delete()
    print(currReport)
    return redirect(reverse('validateReport'))


def moreh(request):
    allpost=Article.objects.filter(highlight=True, isspl=False).filter(status='published', visibility='public').order_by('-dt_published')
    context={'allpost':allpost, 'border_c':'gradient-border'}
    return render(request, 'more.html', context)

def moreo(request):
    allpost=Article.objects.filter(isofficial=True, isspl=False).filter(status='published', visibility='public').order_by('-dt_published')
    context={'allpost':allpost, 'border_c':'border-danger bg-dark'}
    return render(request, 'more.html', context)

def more(request):
    allpost=Article.objects.filter(isofficial=False, highlight=False, isspl=False).filter(status='published', visibility='public').order_by('-dt_published')
    context={'allpost':allpost, 'border_c':'light bg-dark', 'canchk':True}
    return render(request, 'more.html', context)

def postcomment(request, slug):
    if(request.method=='POST'):
        comment = request.POST.get('comment', None)
        article = Article.objects.get(slug=slug)
        user = User.objects.get(username=request.user.username)
        newComment = Comment(user=user, article=article, comment=comment)
        newComment.save()
        return redirect(f'/blog/{slug}#comments')