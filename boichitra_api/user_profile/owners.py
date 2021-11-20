from rest_framework.exceptions import ValidationError
from .models import PublisherProfile,CustomerProfile


class SectionOwner:
    def is_publisher(self, user):
        try:
            restaurant = PublisherProfile.objects.get(user=user)
        except PublisherProfile.DoesNotExist:
            raise ValidationError('Only for publishers')
        return restaurant

    def is_customer(self, user):
        try:
            customer = CustomerProfile.objects.get(user=user)
        except CustomerProfile.DoesNotExist:
            raise ValidationError('Only customer can access this')
        return customer









