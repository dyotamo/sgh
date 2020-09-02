def get_formdata(form):
    data = form.data
    data.pop('csrf_token')
    return data
