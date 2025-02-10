from rest_framework import serializers


class Code(serializers.Serializer):
    """
    Serializer for code
    """
    code = serializers.CharField(max_length=2000)
