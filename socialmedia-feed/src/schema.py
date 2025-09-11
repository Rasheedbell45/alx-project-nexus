import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import Post, Comment, Interaction
from django.db.models import Count
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
import graphql_jwt
import django_filters

User = get_user_model()

# Filters
class PostFilter(django_filters.FilterSet):
    author_username = django_filters.CharFilter(field_name="author__username", lookup_expr='iexact')
    contains = django_filters.CharFilter(field_name="content", lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['author_username', 'contains']

# Types
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class PostType(DjangoObjectType):
    likes_count = graphene.Int()
    shares_count = graphene.Int()
    comments_count = graphene.Int()

    class Meta:
        model = Post
        fields = ("id", "author", "content", "media_url", "created_at", "comments", "interactions")

    def resolve_likes_count(self, info):
        return self.interactions.filter(interaction_type=Interaction.LIKE).count()

    def resolve_shares_count(self, info):
        return self.interactions.filter(interaction_type=Interaction.SHARE).count()

    def resolve_comments_count(self, info):
        return self.comments.count()

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "post", "author", "content", "created_at")

class InteractionType(DjangoObjectType):
    class Meta:
        model = Interaction
        fields = ("id", "post", "actor", "interaction_type", "created_at")

# Queries
class Query(graphene.ObjectType):
    post = graphene.Field(PostType, id=graphene.ID(required=True))
    posts = DjangoFilterConnectionField(PostType, filterset_class=PostFilter)
    comments = graphene.List(CommentType, post_id=graphene.ID(required=True))

    def resolve_post(self, info, id):
        # optimize
        return Post.objects.select_related('author').prefetch_related('comments', 'interactions').filter(pk=id).first()

    def resolve_posts(self, info, **kwargs):
        # returns a connection (relay) which supports pagination cursors
        qs = Post.objects.select_related('author').annotate(
            likes_count=Count('interactions', filter=models.Q(interactions__interaction_type=Interaction.LIKE))
        ).prefetch_related('comments')
        return qs

    def resolve_comments(self, info, post_id):
        return Comment.objects.filter(post_id=post_id).select_related('author')

# Mutations
class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        content = graphene.String(required=True)
        media_url = graphene.String(required=False)

    @classmethod
    @graphql_jwt.decorators.login_required
    def mutate(cls, root, info, content, media_url=None):
        user = info.context.user
        post = Post.objects.create(author=user, content=content, media_url=media_url)
        return CreatePost(post=post)

class AddComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        post_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    @classmethod
    @graphql_jwt.decorators.login_required
    def mutate(cls, root, info, post_id, content):
        user = info.context.user
        post = Post.objects.get(pk=post_id)
        comment = Comment.objects.create(post=post, author=user, content=content)
        return AddComment(comment=comment)

class ToggleLike(graphene.Mutation):
    liked = graphene.Boolean()
    likes_count = graphene.Int()

    class Arguments:
        post_id = graphene.ID(required=True)

    @classmethod
    @graphql_jwt.decorators.login_required
    def mutate(cls, root, info, post_id):
        user = info.context.user
        post = Post.objects.get(pk=post_id)
        interaction, created = Interaction.objects.get_or_create(
            post=post, actor=user, interaction_type=Interaction.LIKE
        )
        if not created:
            # already liked -> unlike
            interaction.delete()
            liked = False
        else:
            liked = True
        likes_count = post.interactions.filter(interaction_type=Interaction.LIKE).count()
        return ToggleLike(liked=liked, likes_count=likes_count)

class SharePost(graphene.Mutation):
    shared = graphene.Boolean()
    shares_count = graphene.Int()

    class Arguments:
        post_id = graphene.ID(required=True)

    @classmethod
    @graphql_jwt.decorators.login_required
    def mutate(cls, root, info, post_id):
        user = info.context.user
        post = Post.objects.get(pk=post_id)
        interaction, created = Interaction.objects.get_or_create(
            post=post, actor=user, interaction_type=Interaction.SHARE
        )
        # if already exists, we keep it (no toggle) — or you could toggle
        shares_count = post.interactions.filter(interaction_type=Interaction.SHARE).count()
        return SharePost(shared=created, shares_count=shares_count)

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    add_comment = AddComment.Field()
    toggle_like = ToggleLike.Field()
    share_post = SharePost.Field()
