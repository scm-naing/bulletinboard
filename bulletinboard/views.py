import csv
import json
import os
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core import serializers

from .form import PostForm, PostSearchForm, SignUpForm, UserEditForm, UserForm, UserSearchForm, csvForm, passwordResetForm
from .models import Post, User
from .functions.helpers import check_route, handle_uploaded_file, remove_temp, save_temp

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        email_user = User.objects.filter(
            email=email, delete_user_id=None, deleted_at=None)
        if email_user:
            password = request.POST['password']
            authUser = authenticate(request, username=email, password=password)
            if authUser:
                login(request, authUser)
                return redirect(request.POST.get('next', '/'))
            else:
                messages.error(request, f'Email and Password does not match.')
        else:
            messages.info(request, f'Email does not exist or deleted')
    return render(request, 'registration/login.html')


@login_required
def index(request):
    user = get_object_or_404(User, pk=request.user.id)
    query = Q()
    if user.type == "1":
        query.add(Q(created_user_id__exact=user.id), Q.AND)
    query.add(Q(delete_user_id=None), Q.AND)
    query.add(Q(deleted_at=None), Q.AND)
    post_search_form = PostSearchForm()
    post_list = Post.objects.all().filter(query).order_by("-updated_at")
    if (request.method == "POST"):
        if '_search' in request.POST:
            post_search_form = PostSearchForm(request.POST)
            if post_search_form.is_valid():
                search = post_search_form.cleaned_data.get('keyword')
                search_q = Q()
                search_q.add(Q(title__icontains=search), Q.OR)
                search_q.add(Q(description__icontains=search), Q.OR)
                post_list = post_list.filter(search_q).order_by("-updated_at")
        elif '_create' in request.POST:
            return HttpResponseRedirect(reverse('post-create'))

    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': page_obj, 'form': post_search_form})


@login_required
def userList(request):
    search_form = UserSearchForm()
    user = get_object_or_404(User, pk=request.user.id)
    q = Q()
    if user.type == "1":
        q.add(Q(created_user_id__exact=user.id), Q.AND)
    q.add(Q(delete_user_id=None), Q.AND)
    q.add(Q(deleted_at=None), Q.AND)
    user_list = User.objects.filter(q).order_by("-updated_at")
    if (request.method == 'POST'):
        search_form = UserSearchForm(request.POST)
        if search_form.is_valid():
            name = search_form.cleaned_data.get('name')
            email = search_form.cleaned_data.get('email')
            from_date = search_form.cleaned_data.get('from_date')
            to_date = search_form.cleaned_data.get('to_date')
            or_q = Q()
            if name:
                or_q.add(Q(name__icontains=name), Q.OR)
            if email:
                or_q.add(Q(email__icontains=email), Q.OR)
            if from_date:
                or_q.add(Q(created_at__gte=from_date), Q.AND)
            if to_date:
                or_q.add(Q(created_at__lte=to_date), Q.AND)
            user_list = user_list.filter(or_q).order_by("-updated_at")

    for user_data in user_list:
        user_data.type = 'Admin' if user_data.type == '0' else 'User'
        list_data = User.objects.get(pk=user_data.created_user_id)
        user_data.created_user = list_data.name if hasattr(list_data, 'name') else ''
    paginator = Paginator(user_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'bulletinboard/user_list.html', {'page_obj': page_obj, 'form': search_form})


@login_required
def postCreate(request):
    form = PostForm()
    check_route('post', request.META.get('HTTP_REFERER'), request)
    user = get_object_or_404(User, pk=request.user.id)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            if "_save" in request.POST:
                if request.session.get("save_confirm_page") == True:
                    new_post = Post(
                        title=form.cleaned_data.get('title'),
                        description=form.cleaned_data.get('description'),
                        status="1",
                        user=user,
                        created_user_id=user.id,
                        updated_user_id=user.id,
                        created_at=timezone.now(),
                        updated_at=timezone.now()
                    )
                    new_post.save()
                    return HttpResponseRedirect(reverse('index'))
                else:
                    formData = {
                        'title': form.cleaned_data.get('title'),
                        'description': form.cleaned_data.get('description'),
                    }
                    form = PostForm(initial=formData)
                    form.fields['title'].widget.attrs['readonly'] = True
                    form.fields['description'].widget.attrs['readonly'] = True
                    request.session["save_confirm_page"] = True
            elif "_cancel" in request.POST:
                return HttpResponseRedirect(reverse('post-create'))
    context = {
        "form": form,
        "operation": "create",
        "save_confirm_page": request.session.get("save_confirm_page")
    }
    return render(request, "bulletinboard/post-create.html", context)


@login_required
def postUpdate(request, pk):
    edit_post = get_object_or_404(Post, pk=pk)
    form = PostForm(initial={"title": edit_post.title,
                    "description": edit_post.description})
    check_route('post', request.META.get('HTTP_REFERER'), request)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            if "_save" in request.POST:
                if request.session.get("save_confirm_page") == True:
                    user = get_object_or_404(User, pk=request.user.id)
                    edit_post.title = form.cleaned_data.get('title')
                    edit_post.description = form.cleaned_data.get(
                        'description')
                    edit_post.status = request.session.get("status")
                    edit_post.user = user
                    edit_post.updated_user_id = user.id
                    edit_post.updated_at = timezone.now()
                    edit_post.save()
                    request.session["save_confirm_page"] = False
                    return HttpResponseRedirect(reverse('index'))
                else:
                    if len(request.POST.getlist('post_status')) > 0:
                        status = "1"
                    else:
                        status = "0"
                    request.session["status"] = status
                    formData = {
                        'title': form.cleaned_data.get('title'),
                        'description': form.cleaned_data.get('description'),
                        'status': status
                    }
                    form = PostForm(initial=formData)
                    form.fields['title'].widget.attrs['readonly'] = True
                    form.fields['description'].widget.attrs['readonly'] = True
                    request.session["save_confirm_page"] = True
            elif "_cancel" in request.POST:
                return HttpResponseRedirect(reverse('post-update', kwargs={'pk': pk}))
    context = {
        "id": pk,
        "form": form,
        "operation": "edit",
        "save_confirm_page": request.session.get("save_confirm_page"),
        "status": request.session.get("status")
    }
    return render(request, "bulletinboard/post-create.html", context)


@login_required
def post_detail(request):
    post_id = request.GET['post_id']
    obj = Post.objects.get(pk=post_id)
    created_user_name = obj.user.name
    updated_user = User.objects.get(pk=obj.updated_user_id)
    data = serializers.serialize('json', [obj, ])
    struct = json.loads(data)
    struct[0]['created_user_name'] = created_user_name
    struct[0]['updated_user_name'] = updated_user.name
    data = json.dumps(struct[0])
    return HttpResponse(data)


@login_required
def post_delete_confirm(request):
    post_id = request.GET['post_id']
    obj = Post.objects.get(pk=post_id)
    data = serializers.serialize('json', [obj, ])
    struct = json.loads(data)
    data = json.dumps(struct[0])
    return HttpResponse(data)


@login_required
def post_delete(request):
    post_id = request.GET['post_id']
    obj = get_object_or_404(Post, pk=post_id)
    obj.delete_user_id = request.user.id
    obj.deleted_at = timezone.now()
    obj.save()
    return HttpResponseRedirect(reverse('index'))


@login_required
def userCreate(request):
    form = UserForm()
    check_route('user', request.META.get('HTTP_REFERER'), request)
    profile = ''
    if request.method == "POST":
        if "_save" in request.POST:
            form = UserForm(request.POST, request.FILES)
            if form.is_valid():
                if request.session.get("save_confirm_page") == True:
                    try:
                        handle_uploaded_file(request.session.get('profile'))
                        user = get_object_or_404(User, pk=request.user.id)
                        new_user = User(
                            name=form.cleaned_data.get('name'),
                            email=form.cleaned_data.get('email'),
                            password=make_password(
                                form.cleaned_data.get('password')),
                            type=form.cleaned_data.get('type'),
                            phone=form.cleaned_data.get('phone'),
                            dob=form.cleaned_data.get('dob'),
                            address=form.cleaned_data.get('address'),
                            profile='upload/'+request.session.get('profile'),
                            created_user_id=user.id,
                            updated_user_id=user.id,
                            created_at=timezone.now(),
                            updated_at=timezone.now()
                        )
                        new_user.save()
                        request.session["save_confirm_page"] = False
                        remove_temp(request.session.get('profile'), ROOT_DIR)
                        return HttpResponseRedirect(reverse('user-list'))
                    except Exception as error:
                        request.session["save_confirm_page"] = False
                        form.add_error(None, str(error))
                else:
                    if "profile" in request.FILES:
                        profile = save_temp(request.FILES['profile'])
                        formData = {
                            'name': form.cleaned_data.get('name'),
                            'email': form.cleaned_data.get('email'),
                            'password': form.cleaned_data.get('password'),
                            'passwordConfirm': form.cleaned_data.get('passwordConfirm'),
                            'type': form.cleaned_data.get('type'),
                            'phone': form.cleaned_data.get('phone'),
                            'dob': form.cleaned_data.get('dob'),
                            'address': form.cleaned_data.get('address'),
                        }
                        form = UserForm(initial=formData)
                        request.session["save_confirm_page"] = True
                        request.session["profile"] = profile
                        form.fields['name'].widget.attrs['readonly'] = True
                        form.fields['email'].widget.attrs['readonly'] = True
                        form.fields['password'].widget.attrs['readonly'] = True
                        form.fields['passwordConfirm'].widget.attrs['readonly'] = True
                        form.fields['type'].widget.attrs['readonly'] = True
                        form.fields['phone'].widget.attrs['readonly'] = True
                        form.fields['dob'].widget.attrs['readonly'] = True
                        form.fields['address'].widget.attrs['readonly'] = True
                        form.fields['profile'].widget.attrs['readonly'] = True
                    else:
                        request.session["save_confirm_page"] = False
                        form.add_error('profile', 'profile can not be blank')
        else:
            request.session["save_confirm_page"] = False
            remove_temp(request.session.get('profile'), ROOT_DIR)
            return HttpResponseRedirect(reverse('user-create'))
    context = {
        "form": form,
        "operation": "create",
        "profile": 'tmp/'+profile,
        "save_confirm_page": request.session.get("save_confirm_page")
    }
    return render(request, "bulletinboard/user-create.html", context)


@login_required
def userProfile(request):
    current_user = get_object_or_404(User, pk=request.user.id)
    context = {
        "id": current_user.id,
        "name": current_user.name,
        "type": current_user.type,
        "email": current_user.email,
        "phone": current_user.phone,
        "dob": current_user.dob,
        "address": current_user.address,
        "profile": current_user.profile,
    }
    return render(request, "bulletinboard/profile.html", context=context)


@login_required
def userUpdate(request, pk):
    req_user = get_object_or_404(User, pk=pk)
    check_route('user', request.META.get('HTTP_REFERER'), request)
    profile = req_user.profile
    tmp_file = profile
    formData = {
        'name': req_user.name,
        'email': req_user.email,
        'type': req_user.type,
        'phone': req_user.phone,
        'dob': req_user.dob,
        'address': req_user.address,
        'profile': profile,
    }
    form = UserEditForm(initial=formData)
    if request.method == "POST":
        if "_save" in request.POST:
            form = UserEditForm(request.POST, request.FILES)
            if form.is_valid():
                if request.session.get("save_confirm_page") == True:
                    try:
                        image = ''
                        if request.session.get("updated_image") == True:
                            handle_uploaded_file(request.session.get('profile'))
                            image = 'upload/'+request.session.get('profile')
                        else:
                            image = request.session.get('profile')
                        user = get_object_or_404(User, pk=request.user.id)
                        user.name = form.cleaned_data.get('name')
                        user.email = form.cleaned_data.get('email')
                        user.type = form.cleaned_data.get('type')
                        user.phone = form.cleaned_data.get('phone')
                        user.dob = form.cleaned_data.get('dob')
                        user.address = form.cleaned_data.get('address')
                        user.profile = image
                        user.updated_user_id = user.id
                        user.updated_at = timezone.now()
                        user.save()
                        request.session["save_confirm_page"] = False
                        if request.session.get("updated_image") == True:
                            remove_temp(request.session.get('profile'), ROOT_DIR)
                        return HttpResponseRedirect(reverse('user-list'))
                    except Exception as error:
                        request.session["save_confirm_page"] = False
                        form.add_error(None, str(error))
                else:
                    if 'profile' in request.FILES:
                        profile = save_temp(request.FILES['profile'])
                        request.session["updated_image"] = True
                        tmp_file = 'tmp/{}'.format(profile)
                    else:
                        request.session["updated_image"] = False

                    formData = {
                        'name': form.cleaned_data.get('name'),
                        'email': form.cleaned_data.get('email'),
                        'type': form.cleaned_data.get('type'),
                        'phone': form.cleaned_data.get('phone'),
                        'dob': form.cleaned_data.get('dob'),
                        'address': form.cleaned_data.get('address'),
                        'profile': profile,
                    }
                    form = UserEditForm(initial=formData)
                    request.session["save_confirm_page"] = True
                    request.session["profile"] = profile
                    form.fields['name'].widget.attrs['readonly'] = True
                    form.fields['email'].widget.attrs['readonly'] = True
                    form.fields['type'].widget.attrs['readonly'] = True
                    form.fields['phone'].widget.attrs['readonly'] = True
                    form.fields['dob'].widget.attrs['readonly'] = True
                    form.fields['address'].widget.attrs['readonly'] = True
                    form.fields['profile'].widget.attrs['disabled'] = True
        else:
            request.session["save_confirm_page"] = False
            if request.session.get("updated_image") == True:
                remove_temp(request.session.get('profile'), ROOT_DIR)
            return HttpResponseRedirect(reverse('user-update', kwargs={'pk': pk}))
    context = {
        "id": req_user.id,
        "form": form,
        "old_profile":  req_user.profile,
        "profile": tmp_file,
        "save_confirm_page": request.session.get("save_confirm_page")
    }
    return render(request, "bulletinboard/user-update.html", context)


@login_required
def user_detail(request):
    user_id = request.GET['user_id']
    obj = User.objects.get(pk=user_id)
    created_user = User.objects.get(pk=obj.created_user_id)
    updated_user = User.objects.get(pk=obj.updated_user_id)
    data = serializers.serialize('json', [obj, ])
    struct = json.loads(data)
    struct[0]['created_user_name'] = created_user.name
    struct[0]['updated_user_name'] = updated_user.name
    data = json.dumps(struct[0])
    return HttpResponse(data)


@login_required
def user_delete_confirm(request):
    user_id = request.GET['user_id']
    obj = get_object_or_404(User, pk=user_id)
    data = serializers.serialize('json', [obj, ])
    struct = json.loads(data)
    data = json.dumps(struct[0])
    return HttpResponse(data)


@login_required
def user_delete(request):
    user_id = request.GET['user_id']
    obj = get_object_or_404(User, pk=user_id)
    obj.delete_user_id = request.user.id
    obj.deleted_at = timezone.now()
    obj.save()
    return HttpResponseRedirect(reverse('user-list'))


def check_csv_row(data):
    arr_csv = []
    for row in data:
        if len(row) != 3:
            return False
        arr_csv.append(row)
    return arr_csv


@login_required
def csv_import(request):
    form = csvForm()
    message = ''
    if request.method == "POST":
        form = csvForm(request.POST, request.FILES)
        if "csv_file" in request.FILES:
            user = get_object_or_404(User, pk=request.user.id)
            req_file = request.FILES["csv_file"]
            if (req_file.content_type == "application/vnd.ms-excel"):
                csv_path = handle_uploaded_file(req_file)
                with open("bulletinboard/static/{}".format(csv_path)) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    valid_csv = check_csv_row(csv_reader)
                    if valid_csv:
                        for i, row in enumerate(valid_csv):
                            if i != 0:
                                csv_post = Post(
                                    title=row[0],
                                    description=row[1],
                                    status=row[2],
                                    user=user,
                                    created_user_id=user.id,
                                    updated_user_id=user.id,
                                    created_at=timezone.now(),
                                    updated_at=timezone.now()
                                )
                                csv_post.save()
                        return HttpResponseRedirect(reverse("index"))
                    else:
                        message = "Post upload csv must have 3 columns"
            else:
                message = "Please choose csv format"
        else:
            message = "Please choose a file"
    context = {
        "form": form,
        "err_message": message
    }
    return render(request, "bulletinboard/csv-import.html", context=context)


@login_required
def download_post_list_csv(request):
    post_list = Post.objects.all().order_by("-updated_at")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="post_list.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'title', 'description', 'status', 'created_user_id',
                    'updated_user_id', 'delete_user_id', 'deleted_at', 'created_at', 'updated_at'])

    for post in post_list:
        writer.writerow([post.id, post.title, post.description, post.status, post.created_user_id,
                        post.updated_user_id, post.delete_user_id, post.deleted_at, post.created_at, post.updated_at])
    return response


@login_required
def user_password_reset(request):
    reset_form = passwordResetForm()
    if request.method == "POST":
        reset_form = passwordResetForm(request.POST)
        if reset_form.is_valid():
            password = reset_form.cleaned_data.get('password')
            new_password = reset_form.cleaned_data.get('new_password')
            valid_pass = get_object_or_404(User, pk=request.user.id)
            if (check_password(password, valid_pass.password)):
                valid_pass.password = make_password(new_password)
                valid_pass.save()
                # requirement was go to user list but django will go to login page
                return HttpResponseRedirect(reverse("user-list"))
            else:
                reset_form.add_error("password", "Current password is wrong!")
    return render(request, "registration/password-reset.html", {"form": reset_form})


def signup(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = User(
                name=form.cleaned_data.get('name'),
                email=form.cleaned_data.get('email'),
                password=make_password(form.cleaned_data.get('password')),
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            new_user.save()
            authUser = authenticate(request, username=form.cleaned_data.get(
                'email'), password=form.cleaned_data.get('password'))
            if authUser:
                login(request, authUser)
                request.session['login_username'] = form.cleaned_data.get(
                    'name')
            messages.info(request, f'User signup successful.')
            return HttpResponseRedirect(reverse('index'))
    context = {
        'title': 'Sign Up',
        'form': form
    }
    return render(request, 'registration/sign_up.html', context)
