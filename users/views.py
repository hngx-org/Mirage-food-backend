
from .serializers import *
from .models import *

# drf imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 

# django imports
from django.http import Http404


class SearchUserView(APIView):
	"Api view accepting either a name (first or last) or email parameter to search for a user"

	def get_object(self, param:str):
		try:
			return User.objects.get(first_name=param)
		except User.DoesNotExist:
			try:
				return User.objects.get(last_name=param)
			except User.DoesNotExist:
				try:
					return User.objects.get(email=param)
				except User.DoesNotExist:
					raise Http404

	def get(self, request, name_or_email:str, *args, **kwargs):
		instance = self.get_object(name_or_email)
		serializer = SearchedUserSerializer(instance)
		data = {
			'message': 'User Found',
			'statusCode': 200,
			'data': serializer.data
		}
		return Response(data, status=status.HTTP_200_OK)
