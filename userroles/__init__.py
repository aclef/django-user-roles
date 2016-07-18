from importlib import import_module

import six
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist

__version__ = '0.1.3'

_IMPORT_FAILED = "Could not import role profile '%s'"
_INCORRECT_ARGS = "USER_ROLES should be a list of strings and/or two-tuples"


def _import_class_from_string(class_path):
    """
    Given a string like 'foo.bar.Baz', returns the class it refers to.
    If the string is empty, return None, rather than raising an import error.
    """
    if not class_path:
        return None
    module_path, class_name = class_path.rsplit('.', 1)
    return getattr(importlib.import_module(module_path), class_name)


class Roles(object):
    _roles_dict = None

    @property
    def roles_dict(self):
        """
        Load list style config into dict of {role_name: role_class}
        """
        if self._roles_dict is None:
            from userroles.models import Role
            self._roles_dict = {}
            for item in Role.objects.all():
                self._roles_dict[item.name] = item.verbose_name
        return self._roles_dict

    @property
    def choices(self):
        """
        Return a list of two-tuples of role names, suitable for use as the
        'choices' argument to a model field.
        """
        return [role for role in six.iteritems(self.roles_dict)]

    def __getattr__(self, name):
        """
        Handle custom properties for returning Role objects.
        For example: `roles.moderator`
        """
        if name in self.roles_dict.keys():
            from userroles.models import Role
            try:
                return Role.objects.get(name=name)
            except ObjectDoesNotExist:
                pass
        raise AttributeError("No such role exists '%s'" % name)


roles = Roles()
