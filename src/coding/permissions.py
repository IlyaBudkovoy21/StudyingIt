from rest_framework.permissions import BasePermission

import logging

from StudyingIt.settings import SERVICES

logger = logging.getLogger("coding.permissions")


class NotForUsers(BasePermission):
    '''
    Class for update date information
    '''

    message = "No access to this function"

    def has_permission(self, request, view):
        user_ip = request.META.get('HTTP_X_REAL_IP', None)
        if user_ip:
            if user_ip in SERVICES:
                return True
            logger.warning(f"{user_ip} wants to get access, {SERVICES} only allows")
            return False
        return False
