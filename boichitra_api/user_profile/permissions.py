from rest_framework.permissions import BasePermission,SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    message = 'You must be the owner of this object'
    my_safe_method = ['GET', 'PATCH', 'DELETE']

    def has_permission(self, request, view):
        if request.method in self.my_safe_method:
            return True
        return False
    
    def has_object_permission(self,request,view,obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class IsPublisher(BasePermission):
    """
    Allows access only to authenticated users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_publisher)


class IsCustomer(BasePermission):
    """
    Allows access only to authenticated customer users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_customer)


class IsAdmin(BasePermission):
    """
    Allows access only to authenticated users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_customer)




