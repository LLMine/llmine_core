from django.shortcuts import render
from datasources.models import Datasource

from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_api_key.permissions import HasAPIKey

from .serializers import DatasourceSerialzer

from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer

from api.openapi_defs import KnoxTokenScheme  # Important Import, not an unused one

from knox.views import LoginView as KnoxLoginView

from core.models import (
    ContentPool,
    InjestedTextContent,
    ExtracterChain,
    ExtracterPrompt,
    ProcessedData,
)
from .serializers import (
    ContentPoolSerializer,
    InjestedTextContentSerializer,
    ExtracterChainSerializer,
    ExtracterPromptSerializer,
    ProcessedDataSerializer,
)

from .filters import (
    ContentPoolFilter,
    InjestedTextContentFilter,
    ExtracterChainFilter,
    ExtracterPromptFilter,
    ProcessedDataFilter,
)


class BaseLLMineRetrieveUpdateDestroyAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class DatasourceList(generics.ListCreateAPIView):
    queryset = Datasource.objects.all()
    serializer_class = DatasourceSerialzer
    permission_classes = [HasAPIKey | IsAuthenticated]
    filterset_fields = ["datasource_name", "datasource_type_name"]


class DatasourceDetail(BaseLLMineRetrieveUpdateDestroyAPIView):
    queryset = Datasource.objects.all()
    serializer_class = DatasourceSerialzer
    permission_classes = [HasAPIKey | IsAuthenticated]


# ContentPool
class ContentPoolListView(generics.ListCreateAPIView):
    queryset = ContentPool.objects.all()
    serializer_class = ContentPoolSerializer
    permission_classes = [HasAPIKey | IsAuthenticated]
    filterset_class = ContentPoolFilter


class ContentPoolDetailView(BaseLLMineRetrieveUpdateDestroyAPIView):
    queryset = ContentPool.objects.all()
    serializer_class = ContentPoolSerializer
    permission_classes = [HasAPIKey | IsAuthenticated]


# InjestedTextContent
class InjestedTextContentListView(generics.ListCreateAPIView):
    queryset = InjestedTextContent.objects.all()
    serializer_class = InjestedTextContentSerializer
    permission_classes = [HasAPIKey | IsAuthenticated]
    filterset_class = InjestedTextContentFilter


class InjestedTextContentDetailView(BaseLLMineRetrieveUpdateDestroyAPIView):
    queryset = InjestedTextContent.objects.all()
    serializer_class = InjestedTextContentSerializer
    permission_classes = [HasAPIKey | IsAuthenticated]


# ExtracterChain
class ExtracterChainListView(generics.ListCreateAPIView):
    queryset = ExtracterChain.objects.all()
    serializer_class = ExtracterChainSerializer
    permission_classes = [HasAPIKey | IsAuthenticated]
    filterset_fields = ["chain_name", "content_pool__pool_name", "llm_name"]
    filterset_class = ExtracterChainFilter


class ExtracterChainDetailView(BaseLLMineRetrieveUpdateDestroyAPIView):
    queryset = ExtracterChain.objects.all()
    serializer_class = ExtracterChainSerializer
    permission_classes = [HasAPIKey | IsAuthenticated]


# ExtracterPrompt
class ExtracterPromptListView(generics.ListCreateAPIView):
    queryset = ExtracterPrompt.objects.all()
    serializer_class = ExtracterPromptSerializer
    permission_classes = [HasAPIKey | IsAuthenticated]
    filterset_class = ExtracterPromptFilter


class ExtracterPromptDetailView(BaseLLMineRetrieveUpdateDestroyAPIView):
    queryset = ExtracterPrompt.objects.all()
    serializer_class = ExtracterPromptSerializer
    permission_classes = [HasAPIKey | IsAuthenticated]


# ProcessedData
class ProcessedDataListView(generics.ListCreateAPIView):
    queryset = ProcessedData.objects.all()
    serializer_class = ProcessedDataSerializer
    permission_classes = [HasAPIKey | IsAuthenticated]
    filterset_class = ProcessedDataFilter


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format=None)
