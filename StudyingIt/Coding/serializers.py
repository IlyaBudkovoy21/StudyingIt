from rest_framework import serializers



class Code(serializers.Serializer):
    code = serializers.CharField(max_length=2000)
