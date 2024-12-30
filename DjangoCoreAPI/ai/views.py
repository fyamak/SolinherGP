from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import os
from .rag_manager import RAGManager

class RAGSearchView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize RAG manager as a class attribute so it persists between requests
        self.rag_manager = RAGManager()
        

    def post(self, request):
        try:
            # Get query from request data
            query = request.data.get('query')
            
            if not query:
                return Response(
                    {'error': 'Query is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Process query through RAG
            response = self.rag_manager.send_query_to_rag(query)

            return Response({
                'query': query,
                'response': response
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )