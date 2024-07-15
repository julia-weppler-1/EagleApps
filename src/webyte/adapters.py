from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from user.models import Student  # Adjust the import path as necessary

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)
        # The email is already guaranteed to be unique by allauth.
        student, created = Student.objects.get_or_create(email=user.email, defaults={'name': user.get_full_name()})
        # No need to check `created` because the user is new at this point.
        return user

@receiver(user_signed_up)
def create_student_profile(request, user, **kwargs):
    # This will be triggered after a user signs up via social account.
    # No need to check for `get_or_create` as `save_user` has already done it.
    student = Student.objects.get(email=user.email)
    student.name = user.get_full_name()  # Update the name in case it has changed.
    student.save()