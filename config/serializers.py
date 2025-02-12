from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group

from config.models import UIComponent  

User = get_user_model()  # Ensure we use the correct User model

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()  # Convert Group IDs to names
    user_permissions = serializers.SerializerMethodField()  # Co

    class Meta:
        model = User  # Now using the correct model
        fields = ('id', 'date_joined', 'email', 'first_name', 'last_name', 'username', 'groups', 'user_permissions')

    def get_groups(self, obj):
        return list(obj.groups.values_list('name', flat=True))

    def get_user_permissions(self, obj):
        user_perms = set(obj.user_permissions.values_list('codename', flat=True))
        group_perms = set(Permission.objects.filter(group__user=obj).values_list('codename', flat=True))
        return list(user_perms | group_perms)  # Combine both user and group permissions

class UIComponentSerializer(serializers.ModelSerializer):
    allowed_groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all()
    )

    class Meta:
        model = UIComponent
        fields = ['name', 'is_visible', 'allowed_groups']
