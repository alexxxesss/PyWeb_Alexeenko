from rest_framework import serializers

from .models import Note, Comment


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ("author",)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class NoteDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = ('title', 'message', 'author', 'status', 'importance', 'public', 'deadline', 'create_at', 'update_at',
                  'comment_set',
                  )
