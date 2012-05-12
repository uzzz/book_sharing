class LoginMixin:
    class Login(object):
        def __init__(self, testcase, user, password):
            self.testcase = testcase
            success = testcase.client.login(username=user, password=password)
            self.testcase.assertTrue(
                success,
                "login with username=%r, password=%r failed" % (user, password)
            )

        def __enter__(self):
            pass

        def __exit__(self, *args):
            self.testcase.client.logout()

    def login(self, user):
        user.set_password('password')
        user.save()
        return LoginMixin.Login(self, user, 'password')
