# from django.shortcuts import render
# from rest_framework.views import APIView
# from .models import User
# from rest_framework.response import Response
# from rest_framework import status

# # Create your views here.

# class DeleteUserView:

#     def get_user_by_pk(self, pk):
#         try:
#             return User.objects.get(pk=id)
#         except:
#             return Response({
#                 'error': 'User does not exist'
#             }, status=status.HTTP_404_NOT_FOUND)


#     def delete_user(self, request, pk):
#         user = self.get_user_by_pk(pk=id)
#         user.delete()
#         return Response({'Message': 'User Deleted'}, status=status.HTTP_204_NO_CONTENT)
