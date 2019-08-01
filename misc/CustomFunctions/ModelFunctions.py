from django.shortcuts import get_object_or_404


def filterModelObject(model_name, **kwargs):
    result = model_name.objects.filter(**kwargs).all()
    return result


def excludeModelObject(model_name, **kwargs):
    result = model_name.objects.exclude(**kwargs).all()
    return result


def getModelObject(model_name, **kwargs):
    return get_object_or_404(model_name, **kwargs)
