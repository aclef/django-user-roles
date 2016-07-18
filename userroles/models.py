from django.contrib.auth.models import User
from django.db import models
from six import python_2_unicode_compatible


class Role(models.Model):
    """
    A single role, eg as returned by `roles.moderator`.
    """
    name = models.CharField(max_length=100)
    base_role = models.ForeignKey('Role', blank=True, null=True)
    verbose_name = models.CharField(max_length=100)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.OneToOneField(User, related_name='role')
    role = models.ForeignKey(Role, blank=True, null=True)
    child = models.CharField(max_length=100, blank=True)

    @property
    def profile(self):
        if not self.child:
            return None
        return getattr(self, self.child)

    def __eq__(self, other):
        if isinstance(other, UserRole):
            other = other.role
        return self.role == other or \
               getattr(self.role, 'base_role', '1') == getattr(other, 'base_role', '2')

    def __getattr__(self, name):
        if name.startswith('is_'):
            return self.role.name == name[3:] or getattr(self.role.base_role, 'name', None)== name[3:]
        return super().__getattr__(name)
        # if name not in ['name', 'base_role_name']:
        #     raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, name))

    @python_2_unicode_compatible
    def __str__(self):
        return getattr(self.role, 'name', 'null')

    @property
    def name(self):
        return getattr(self.role, 'name', 'null')

    @property
    def verbose_name(self):
        return getattr(self.role, 'verbose_name', 'null')

    @property
    def base_role_name(self):
        return getattr(getattr(self.role, 'base_role', 'null'), 'name', 'null')


def set_user_role(user, role, profile=None):
    try:
        UserRole.objects.get(user=user).delete()
    except UserRole.DoesNotExist:
        pass

    if profile:
        profile.user = user
        profile.role = role
        profile.child = str(profile.__class__.__name__).lower()
    else:
        profile = UserRole(user=user, role=role)

    profile.save()
