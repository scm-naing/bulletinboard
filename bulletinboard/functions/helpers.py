import os
from django.conf import settings


def save_temp(f):
    """
    For image upload as temp file and show in confirm page.
    Param: Django's form file (type: InMemoryFile)
    return: name of file
    """
    if not f:
        return ""
    with open("media/tmp/"+f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        return f.name


def handle_uploaded_file(fname):
    """
    Upload profile from temp file
    param: file name of temp file
    """
    if not fname:
        return ""
    with open("media/tmp/"+fname, "rb") as tmp:
        img_str = tmp.read()
        with open("media/upload/"+fname, "wb+") as upload:
            upload.write(img_str)


def remove_temp(f):
    """
    Remove temp file after save
    param: file name
    """
    if (f):
        os.unlink(str(settings.BASE_DIR)+"\\media\\tmp\\"+f)


def check_route(current_route, previousRoute, request):
    """
    Checking is_confirm_page session flag and control its bugs
    param: current route, previous route and request from view
    """
    if previousRoute is not None:
        splittedRoute = previousRoute.split("/")
        print("==== splittedRoute[-2] ====")
        print(splittedRoute)
        if (splittedRoute[-2] == "create"):
            if (splittedRoute[-3] != current_route):
                request.session["save_confirm_page"] = False
        else:
            if (splittedRoute[-3] != current_route):
                request.session["save_confirm_page"] = False
    else:
        request.session["save_confirm_page"] = False
