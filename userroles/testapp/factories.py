from django.conf import settings

import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Sequence(lambda n: '{0}@{0}.com'.format(n))
    email = factory.Sequence(lambda n: '{0}@{0}.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password',
                                                'password')
