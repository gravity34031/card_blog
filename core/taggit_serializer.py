"""
Django-taggit serializer support
Originally vendored from https://github.com/glemmaPaul/django-taggit-serializer
"""
import json

# Third party
from django.utils.translation import gettext_lazy
from rest_framework import serializers


class TagList(list):
    def __init__(self, *args, **kwargs):
        pretty_print = kwargs.pop("pretty_print", True)
        super().__init__(*args, **kwargs)
        self.pretty_print = pretty_print

    def __add__(self, rhs):
        return TagList(super().__add__(rhs))

    def __getitem__(self, item):
        result = super().__getitem__(item)
        try:
            return TagList(result)
        except TypeError:
            return result

    def __str__(self):
        if self.pretty_print:
            return json.dumps(self, sort_keys=True, indent=4, separators=(",", ": "))
        else:
            return json.dumps(self)


class TagListSerializerField(serializers.Field):
    def to_internal_value(self, data):
        if type(data) is not list:
            raise Exception("expected a list of data")
        return data

    def to_representation(self, obj):
        if type(obj) is not list:
            return [tag.name for tag in obj.all() if not (tag.name.isspace() and tag.name)]
        return obj


class TaggitSerializer(serializers.Serializer):
    def create(self, validated_data):
        to_be_tagged, validated_data = self._pop_tags(validated_data)

        tag_object = super().create(validated_data)

        return self._save_tags(tag_object, to_be_tagged)

    def update(self, instance, validated_data):
        to_be_tagged, validated_data = self._pop_tags(validated_data)

        tag_object = super().update(instance, validated_data)

        return self._save_tags(tag_object, to_be_tagged)

    def _save_tags(self, tag_object, tags):
        for key in tags.keys():
            tag_values = tags.get(key)
            getattr(tag_object, key).set(tag_values)
        return tag_object

    def _pop_tags(self, validated_data):
        to_be_tagged = {}

        for key in self.fields.keys():
            field = self.fields[key]
            if isinstance(field, TagListSerializerField):
                if key in validated_data:
                    to_be_tagged[key] = validated_data.pop(key)
        
        to_be_tagged = {'tags': [i for i in to_be_tagged['tags'] if not i.isspace() and i]}
        return (to_be_tagged, validated_data)