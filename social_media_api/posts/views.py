"""
posts/views.py

WHY ModelViewSet?
    ModelViewSet provides all 5 actions (list, create, retrieve,
    update, destroy) with one class. We only override where we need
    custom behaviour (setting author, filtering).

WHY perform_create()?
    This DRF hook runs after validation. We use it to inject
    request.user as the author — the serializer marks author as
    read_only so clients can't spoof it.

WHY filter_backends with SearchFilter?
    DRF's SearchFilter integrates with the ?search= query param.
    search_fields = ['^title', '=content'] means:
        ^title   → starts-with search on title
        =content → exact match on content (use 'content' for contains)
    We use 'title' and 'content' (no prefix) for contains-search,
    which is the most intuitive UX for a social feed.

WHY PageNumberPagination?
    As the dataset grows, returning all posts in one response becomes
    impractical. PageNumberPagination adds ?page= support and returns
    count/next/previous links in the response body so clients can
    implement infinite scroll or traditional pagination.
"""

from rest_framework import filters, viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import Comment, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, PostSerializer


class PostPagination(PageNumberPagination):
    """
    Custom pagination class so we can set page size per-viewset.
    10 posts per page is a sensible default for a social feed.
    max_page_size prevents clients from requesting huge pages.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD endpoints for Posts.

    list:     GET  /api/posts/
    create:   POST /api/posts/
    retrieve: GET  /api/posts/{id}/
    update:   PUT  /api/posts/{id}/
    partial:  PATCH /api/posts/{id}/
    destroy:  DELETE /api/posts/{id}/
    """
    queryset = Post.objects.all().select_related('author')
    # select_related('author') → one SQL JOIN instead of N+1 queries
    # for author_username on every post in the list

    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = PostPagination

    # SearchFilter: adds ?search= query parameter
    # OrderingFilter: adds ?ordering=created_at or ?ordering=-created_at
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']     # contains-search on both fields
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']               # default: newest first

    def perform_create(self, serializer):
        # Inject the authenticated user as author at save time
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD endpoints for Comments.

    list:     GET  /api/comments/             (all comments, paginated)
    create:   POST /api/comments/
    retrieve: GET  /api/comments/{id}/
    update:   PUT  /api/comments/{id}/
    partial:  PATCH /api/comments/{id}/
    destroy:  DELETE /api/comments/{id}/

    WHY not nest under /api/posts/{id}/comments/?
        Nested routers add complexity. A flat /api/comments/?post=<id>
        filter achieves the same result with standard DRF tools.
        We can always add nested routes later if the frontend prefers them.
    """
    queryset = Comment.objects.all().select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = PostPagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def get_queryset(self):
        """
        Optionally filter comments by post via ?post=<post_id>.
        This replaces the need for nested URL routing.
        """
        queryset = super().get_queryset()
        post_id = self.request.query_params.get('post')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedView(generics.ListAPIView):
    """
    GET /api/feed/

    Returns posts from users the authenticated user follows,
    ordered by most recent first.

    WHY ListAPIView instead of ModelViewSet?
        The feed is read-only — there's no creating, updating or
        deleting from the feed endpoint. ListAPIView gives us just
        the GET list action with pagination built in.

    WHY filter on following in get_queryset()?
        request.user.following.all() returns all users this user
        follows. We then filter posts to only those whose author
        is in that set. If the user follows nobody, the feed is
        empty — which is correct behaviour.

    WHY order by -created_at?
        Most recent posts at the top — standard social media feed
        behaviour (reverse chronological order).
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PostPagination

    def get_queryset(self):
        # Get all users the current user follows
        followed_users = self.request.user.following.all()

        # Return their posts, newest first
        return Post.objects.filter(
            author__in=followed_users
        ).order_by('-created_at')