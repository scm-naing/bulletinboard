import os


def save_temp(f):
    if not f:
        return ''
    with open('bulletinboard/static/tmp/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        return f.name


def handle_uploaded_file(fname):
    if not fname:
        return ''
    with open('bulletinboard/static/tmp/'+fname, 'rb') as tmp:
        img_str = tmp.read()
        with open('bulletinboard/static/upload/'+fname, 'wb+') as upload:
            upload.write(img_str)


def remove_temp(f, root_dir):
    if (root_dir and f):
        os.unlink(root_dir+'\\static\\tmp\\'+f)


def check_route(current_route, previousRoute, request):
    if previousRoute is not None:
        splittedRoute = previousRoute.split('/')
        print('==== splittedRoute[-2] ====')
        print(splittedRoute)
        if (splittedRoute[-2] == 'create'):
            if (splittedRoute[-3] != current_route):
                request.session["save_confirm_page"] = False
        else:
            if (splittedRoute[-3] != current_route):
                request.session["save_confirm_page"] = False
    else:
        request.session["save_confirm_page"] = False
