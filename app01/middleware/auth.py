from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 0. Exclude pages that can be accessed without logging in
        #   request.path_info retrieves the URL requested by the current user, e.g., /login/
        if request.path_info in ["/login/", "/image/code/"]:
            return

        # 1. Read the session information of the currently accessed user.
        #    If session info is found, it means the user has already logged in and can proceed.
        info_dict = request.session.get("info")
        # print(info_dict)
        if info_dict:
            return

        # 2. If not logged in, redirect back to the login page
        return redirect('/login/')

