from datetime import datetime

from rest_framework import serializers

from .models import ToDo, Comment


class NoteSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        model = ToDo
        exclude = ('id', )
        read_only_fields = ("author",)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        create_at = datetime.strptime(ret['create_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        ret['create_at'] = create_at.strftime('%d %B %Y %H:%M:%S')
        update_at = datetime.strptime(ret['update_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        ret['update_at'] = update_at.strftime('%d %B %Y %H:%M:%S')
        return ret


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    rating = serializers.SerializerMethodField('get_rating')

    class Meta:
        model = Comment
        exclude = ('id', 'todo', )

    def get_rating(self, obj: Comment):
        return obj.get_rating_display()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        created = datetime.strptime(ret['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
        ret['created'] = created.strftime('%d %B %Y %H:%M:%S')
        return ret


class NoteDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = ToDo
        fields = ('id',
                  'title',
                  'message',
                  'author',
                  'status',
                  'importance',
                  'public',
                  'deadline',
                  'create_at',
                  'update_at',
                  'comments',
                  )
        read_only_fields = ("comments",)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        create_at = datetime.strptime(ret['create_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        ret['create_at'] = create_at.strftime('%d %B %Y %H:%M:%S')
        update_at = datetime.strptime(ret['update_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        ret['update_at'] = update_at.strftime('%d %B %Y %H:%M:%S')
        # deadline = datetime.strptime(ret['deadline'], '%Y-%m-%dT%H:%M:%SZ')
        # ret['deadline'] = deadline.strftime('%d %B %Y %H:%M:%S')
        return ret


class CommentListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    rating = serializers.SerializerMethodField('get_rating')

    class Meta:
        model = Comment
        fields = '__all__'

    def get_rating(self, obj: Comment):
        return obj.get_rating_display()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        created = datetime.strptime(ret['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
        ret['created'] = created.strftime('%d %B %Y %H:%M:%S')
        return ret
