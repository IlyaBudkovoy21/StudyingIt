from rest_framework.permissions import BasePermission

import logging

from StudyingIt.settings import SERVICES

logger = logging.getLogger("Coding.persmissions")


class NotForUsers(BasePermission):
    '''
    Class for update date information
    '''

    message = "No access"

    def has_permission(self, request, view):
        logger.warning(f"{request.META['REMOTE_ADDR']} wants to get access, {SERVICES} only allows")
        if request.META["REMOTE_ADDR"] in SERVICES:
            return True
        return False
