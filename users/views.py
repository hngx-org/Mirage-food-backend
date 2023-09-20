
from .serializers import *

# drf imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 

# django imports
from django.contrib.auth import get_user_model
from django.http import Http404

UserModel = get_user_model()

class SearchUserView(APIView):
	"Api view accepting either a name or email parameter to search for a user"

	def get_object(self, param):
		try:
			return UserModel.objects.get(name=param)
		except UserModel.DoesNotExist:
			try:
				return UserModel.objects.get(email=param)
			except UserModel.DoesNotExist:
				raise Http404

	def get(self, request, name_or_email, *args, **kwargs):
		instance = self.get_object(name_or_email)
		serializer = SearchedUserSerializer(instance)
		data = {
			'message': 'User Found',
			'statusCode': 200,
			'data': serializer.data
		}
		return Response(data, status=status.HTTP_200_OK)
