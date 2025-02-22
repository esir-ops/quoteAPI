from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Quote
from .serializers import QuoteSerializer

class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

    # Specify allowed HTTP methods
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        queryset = super().get_queryset()
        author = self.request.query_params.get('author', None)
        year_start = self.request.query_params.get('year_start', None)
        year_end = self.request.query_params.get('year_end', None)

        if author:
            queryset = queryset.filter(author__iexact=author)
        if year_start and year_end:
            queryset = queryset.filter(year__gte=year_start, year__lte=year_end)

        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        quote = self.get_object()
        serializer = self.get_serializer(quote)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, partial=False):  # Accept the partial argument
        quote = self.get_object()
        serializer = self.get_serializer(quote, data=request.data, partial=partial)  # Pass partial to the serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        quote = self.get_object()
        quote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)