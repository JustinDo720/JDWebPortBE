from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    We only want Owners to perform POST, PUT and DELETE (EXCEPT: Contact Me)
        This permission will enable owners to do these operations
    """

    def has_permission(self, request, view):
        # disable all POST, PUT, DELETE requests
        if request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':
            # idea => return False is we want unauth and return True if we want auth
            # we need to take care of admin users first sooo
            if request.user and request.user.is_superuser:
                return True
            # or else we'll disable this for everyone else
            return False
        elif request.method == 'GET':
            return True # allow GET requests

