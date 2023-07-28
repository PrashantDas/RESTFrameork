from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MemberRegisterSerializer, MemberLoginSerializer, UserProfileSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


class RegisterMemberView(APIView):
    def post(self, request):
        try:
            received_data = request.data
            serializer = MemberRegisterSerializer(data=received_data)            
            if serializer.is_valid():                
                serializer.save()
                name = serializer.data.get('username', 'has no username')
                return Response({'data':serializer.data, 'message':f'User {name} created'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'data':serializer.errors, 'message':'Username not available'}, status=status.HTTP_400_BAD_REQUEST)                
        except Exception as e:
            print('******** exception', e)
            return Response({'data': {}, 'message': 'received data for register was invalid with an exception'},
                                status = status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        try:
            received_data = request.data
            name = request.data.get('username')
            serializer = MemberLoginSerializer(data=received_data)
            if serializer.is_valid(): # now we'll check if the username - password pair match
                received_username, received_password = serializer.data.get('username'), serializer.data.get('password')
                user = authenticate(username=received_username, password=received_password)
                if user:
                    your_tokens = serializer.get_tokens_for_user(user)
                    return Response({'data':your_tokens, 'message': f"access token is generated, user '{name}' is logged-in"}, status=status.HTTP_200_OK)
                else:
                    return Response({'data':serializer.errors, 'message':f'The username \'{name}\' is correct but the password isn\'t'}, status=status.HTTP_400_BAD_REQUEST)                
            else:
                return Response({'data':serializer.errors, 'message':f'Such username \'{name}\' does not exist'}, status=status.HTTP_400_BAD_REQUEST)                
            
        except Exception as e:
            print('exception', e)
            return Response({'data': {}, 'message': 'credentials invalid!'})
        

class UserProfileView(APIView): # http://127.0.0.1:8000/api/members/profile/
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        logged_in_user = request.user.id
        found_blog_to_delete = User.objects.filter(id=logged_in_user)
        found_blog_to_delete.delete()
        return Response({'message': "user deleted successfully"})
    

class AllUserSerializer(APIView):  # http://127.0.0.1:8000/api/members/all/
    def get(self, request):
        data = User.objects.all()
        serializer = UserProfileSerializer(instance=data, many=True)
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)
