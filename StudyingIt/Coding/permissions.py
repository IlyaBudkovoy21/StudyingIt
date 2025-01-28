from rest_framework.permissions import BasePermission

from StudyingIt.settings import SERVICES


class NotForUsers(BasePermission):
    '''
    Class for update date information
    '''

    message = "No access"

    def has_permission(self, request, view):
        print(request.META["REMOTE_ADDR"])
        if request.META["REMOTE_ADDR"] in SERVICES:
            return True
        return False
