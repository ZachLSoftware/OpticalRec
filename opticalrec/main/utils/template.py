def getTemplate(request):
    if request.user.is_authenticated:
        if request.user.theme=="Dark":
            template='base_template_dark.html'
        else:
            template='base_template.html'
    elif not request.user.is_authenticated:
        template='base_template.html'
    return template