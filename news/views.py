import hashlib, random, string, datetime, json
from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict
from news.models import Post, Comment, Clap
from cicsa_ranking.models import Account


def index(request):
    return redirect('posts')


def login(request):
    if request.POST.get("email") is not None and request.POST.get("password") is not None:
        uemail = request.POST.get("email")
        upwd = request.POST.get("password")
        u = Account.objects.filter(account_email=uemail)
        if not len(u):
            return HttpResponse('{"Response": "Failed"}')
        else:
            u = u.get()
            u_pwd = u.account_pwd
            u_salt = u.account_hash_salt
            verify_pwd = hashlib.sha224((upwd + u_salt).encode("utf-8")).hexdigest()
            if u_pwd == verify_pwd:
                request.session['uid'] = u.id
                return redirect('../posts/')
            else:
                return HttpResponse('{"Response": "Failed"}')
    else:
        return HttpResponse('{"Error": "You have not given sufficient parameters."}')


def logout(request):
    if 'uid' in request.session:
        request.session['uid'] = None
        return redirect('../posts/')
    else:
        return HttpResponse('{"Error": "You have not logged in"}')


def permission(request):
    signed_in = True if 'uid' in request.session and request.session['uid'] is not None else False
    return render(request, 'blog/login.html', {'signedIn': signed_in})


def addPost(request, pt, pc):
    # check session
    if 'uid' in request.session and request.session['uid'] is not None:
        uid = request.session['uid']
        try:
            post = Post(post_title=pt, post_content=pc, post_claps=0, post_owner=uid,
                        post_create_time=datetime.datetime.now())
            post.save()
            return HttpResponse('{"Response": "Success"}')
        except Exception as e:
            return HttpResponse(str(e))
    else:
        return HttpResponse('{"Response": "Error: You have no permission."}')


def clapPost(request, pid):
    if 'uid' in request.session and request.session['uid'] is not None:
        uid = request.session['uid']
        post = Post.objects.filter(id=pid)
        clap = Clap.objects.filter(post_id=pid, clapper_id=uid)
        if not len(clap):
            post.update(post_claps=post[0].post_claps + 1)
            claplog = Clap(clapper_id=uid, post_id=pid)
            claplog.save()
            return HttpResponse('{"Response": "Success"}')
        else:
            return HttpResponse('{"Response": "Error: You have clapped the post already."}')
    else:
        return HttpResponse('{"Response": "Error: You have no permission."}')


def addComment(request, pid, cc):
    if 'uid' in request.session and request.session['uid'] is not None:
        try:
            uid = request.session['uid']
            comment = Comment(comment_owner=uid, comment_content=cc, post_id=pid,
                              comment_create_time=datetime.datetime.now())
            comment.save()
            return redirect('../posts/?id=' + pid)
        except Exception as e:
            return HttpResponse(str(e))
    else:
        return HttpResponse('{"Response": "Error: You have no permission."}')


def addAccount(request, account_name, account_email, account_pwd):
    try:
        if len(Account.objects.filter(account_email=account_email)) == 0:
            randText = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
            hashpwd = hashlib.sha224((account_pwd + randText).encode("utf-8")).hexdigest()
            time = datetime.datetime.now()
            account_hid = hashlib.sha224((account_name + str(time)).encode("utf-8")).hexdigest()
            account = Account(account_name=account_name, account_email=account_email, account_pwd=hashpwd,
                        account_hash_salt=randText, account_create_time=time)
            account.save()
            return HttpResponse('{"Response": "Success"}')
        else:
            return HttpResponse('{"Response": "Error: Account Already Exists"}')
    except Exception as e:
        return HttpResponse(str(e))


def getAccount(request, account_id):
    u = Account.objects.filter(id=account_id)
    if not len(u):
        return HttpResponse('{"Response": "Error: Account Does Not Exist"}')
    else:
        u = u.get()
        uarr = {"account_id": u.id, "account_name": u.account_name, "account_email": u.account_email}
        return HttpResponse(json.dumps(uarr))


def getAllPosts(request):
    posts = reversePostTimeSort(Post.objects.all())
    for p in posts:
        p.post_owner_name = Account.objects.filter(id=p.post_owner)[0].account_name
    signed_in = True if 'uid' in request.session and request.session['uid'] is not None else False
    return render(request, 'blog/allPosts.html', {'posts': posts, 'signedIn': signed_in})


def getPostAccount(request, account_id):
    posts = reversePostTimeSort(Post.objects.filter(post_owner=account_id))
    u = Account.objects.filter(id=account_id)[0]
    uname = u.account_name
    signed_in = True if 'uid' in request.session and request.session['uid'] is not None else False
    return render(request, 'blog/postAccount.html', {'posts': posts, 'name': uname, 'signedIn': signed_in})


def getSpecificPost(request, post_id):
    posts = Post.objects.filter(id=post_id)
    if len(posts) == 0:
        return HttpResponse('{"Response": "Error: No post with the id was found."}')
    else:
        u = Account.objects.filter(id=posts[0].post_owner)[0]
        uname = u.account_name
        signed_in = True if 'uid' in request.session and request.session['uid'] is not None else False
        comments = reverseCommentTimeSort(Comment.objects.filter(post_id=post_id))
        for c in comments:
            c.comment_owner_name = Account.objects.filter(id=c.comment_owner)[0].account_name
        return render(request, 'blog/post.html',
                      {'posts': posts, 'name': uname, 'comments': comments, 'signedIn': signed_in})


def getComments(request, pid):
    return Comment.objects.filter(post_id=pid)


def getAccountComments(request, account_id):
    return Comment.objects.filter(comment_owner=account_id)


def delPost(request, post_id):
    if 'uid' in request.session and request.session['uid'] is not None:
        uid = request.session['uid']
        post = Post.objects.filter(id=post_id)[0]
        if post.post_owner == uid:
            post.delete()
            return redirect('../admin/?posts=True')
        else:
            return HttpResponse('{"Response": "Error: You have no permission."}')
    else:
        return HttpResponse('{"Response": "Error: You have no permission."}')


def delComment(request, comment_id):
    if 'uid' in request.session and request.session['uid'] is not None:
        uid = request.session['uid']
        comment = Comment.objects.filter(id=comment_id)[0]
        if comment.comment_owner == uid:
            comment.delete()
            return redirect('../admin/?comments=True')
        else:
            return HttpResponse('{"Response": "Error: You have no permission."}')
    else:
        return HttpResponse('{"Response": "Error: You have no permission."}')


def posts(request):
    if request.method == 'POST':
        if request.POST.get("title") is not None and request.POST.get("content") is not None:
            return addPost(request, request.POST.get("title"), request.POST.get("content"))
        else:
            return HttpResponse('{"Response": "Error: You have not given sufficient parameters."}')
    elif request.method == 'GET':
        if request.GET.get("id") is not None:
            if request.GET.get("clap") == "True":
                return clapPost(request, request.GET.get("id"))
            else:
                return getSpecificPost(request, request.GET.get("id"))
        else:
            return getAllPosts(request)
    elif request.method == 'DELETE':
        qd = QueryDict(request.body)
        return delPost(request, qd['id'])
    else:
        return HttpResponse('{"Response": "Error: You have not given sufficient parameters."}')


def comments(request):
    if request.method == 'POST':
        if request.POST.get("comment") is not None and request.POST.get("post_id") is not None:
            return addComment(request, request.POST.get("post_id"), request.POST.get("comment"))
        else:
            return HttpResponse('{"Response": "Error: You have not given sufficient parameters."}')
    elif request.method == 'DELETE':
        qd = QueryDict(request.body)
        return delComment(request, qd['id'])
    else:
        return HttpResponse('{"Response": "Error: You have not given sufficient parameters."}')


def accountPost(request, account_id):
    if account_id is not None:
        return getPostAccount(request, account_id)
    else:
        return HttpResponse('{"Response": "Error: You have not given sufficient parameters."}')


def reversePostTimeSort(obj):
    return sorted(obj, key=lambda x: x.post_create_time, reverse=True)


def reverseCommentTimeSort(obj):
    return sorted(obj, key=lambda x: x.comment_create_time, reverse=True)


def adminPost(request):
    posts = reversePostTimeSort(Post.objects.filter(post_owner=request.session['uid']))
    return render(request, 'blog/adminPost.html', {'posts': posts, 'uid': request.session['uid']})


def adminComment(request):
    comments = reverseCommentTimeSort(getAccountComments(request, request.session['uid']))
    return render(request, 'blog/adminComment.html', {'comments': comments, 'uid': request.session['uid']})


def admin(request):
    if 'uid' in request.session and request.session['uid'] is not None:
        if request.GET.get("posts") == "True":
            return adminPost(request)
        elif request.GET.get("comments") == "True":
            return adminComment(request)
        else:
            return adminPost(request)
    else:
        return HttpResponse('{"Response": "Error: You have no permission."}')
