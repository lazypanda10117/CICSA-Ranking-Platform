def filterModelObject(model_name, **kwargs):
    result = model_name.objects.filter(**kwargs).all()
    return result


def excludeModelObject(model_name, **kwargs):
    result = model_name.objects.exclude(**kwargs).all()
    return result


def getModelObject(model, **kwargs):
    try:
        result = model.objects.get(**kwargs)
    except model.DoesNotExist:
        result = None
    return result
