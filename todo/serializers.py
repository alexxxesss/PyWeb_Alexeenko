from rest_framework import serializers

from .models import ToDo, Comment


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = '__all__'
        read_only_fields = ("author",)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class NoteDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = ToDo
        fields = ('title', 'message', 'author', 'status', 'importance', 'public', 'deadline', 'create_at', 'update_at',
                  'comments',
                  )
