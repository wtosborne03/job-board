from django.core.exceptions import PermissionDenied


def employer_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.userprofile.user_type == 'employer':
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view
