from slugify import slugify
from taggit.models import Tag, TaggedItem
from transliterate import translit


class RuTag(Tag):
    class Meta:
        proxy = True

    def slugify(self, tag, i=None):
        """print(translit('пуоцш32', 'ru'))
        return slugify(translit(self.name, 'ru'))[:128] """
        slug = slugify(translit(self.name, 'ru'))
        return slug


class RuTaggedItem(TaggedItem):
    class Meta:
        proxy = True

    @classmethod
    def tag_model(cls):
        return RuTag