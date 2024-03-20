from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Title, Review
from .serializers import ReviewSerializer, CommentSerializer, TitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('titles_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(title=title)
        self.update_title_rating(title)

    def perform_update(self, serializer):
        title = self.get_title()
        serializer.save(title=title)
        self.update_title_rating(title)

    def perform_destroy(self, instance):
        instance.delete()
        self.update_title_rating(self.get_title())

    def update_title_rating(self, title):
        reviews = Review.objects.filter(title=title)
        average_score = (sum(review.score for review in reviews)
                         / reviews.count()) if reviews.count() > 0 else 0
        title.raiting = round(average_score, 2)
        title.save()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review,
                                 id=self.kwargs.get('review_id'),
                                 title_id=self.kwargs.get('titles_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(review=self.get_review())
