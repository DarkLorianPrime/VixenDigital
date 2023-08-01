#  Copyright (c) 2023. Kasimov Alexander, Ulyanovsk. All right reserved.

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.organizations.models import Organization
from apps.organizations.repositories import OrganizationRepository
from core.slugifer import slugify

organizations_repo = OrganizationRepository()


class OrganizationSerializer(ModelSerializer):
    name = serializers.CharField()
    maintainer = serializers.CharField(default=None)
    contributors = serializers.ListField(write_only=True)
    logo = serializers.ImageField()
    slug = serializers.SlugField(default=None)
    verified = serializers.BooleanField(default=False)

    class Meta:
        model = Organization
        fields = "__all__"

    @property
    def method(self):
        return self.context["request"].method

    def validate_verified(self, verified):
        if self.context["request"].user.is_staff:
            return verified

        return False

    def validate_logo(self, image):
        if self.method in ["PUT", "PATCH"]:
            organizations_repo.organization_logo_delete(instance=self.instance)

        return image

    def validate_name(self, name):
        self.context["name"] = name

        instance: Organization | dict = self.instance or {}
        instance_name = getattr(instance, "name", None)

        if instance_name == name:
            return name

        return organizations_repo.is_exist_organization(name=name)

    def validate_maintainer(self, _):
        user = self.context["request"].user
        if self.method == "POST":
            return user

        return organizations_repo.get_maintainer(user)

    def validate_slug(self, _):
        return slugify(self.context["name"])

    def validate_contributors(self, contributors):
        return organizations_repo.get_contributors(contributors)
