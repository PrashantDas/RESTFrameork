from .serializers import NotesModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import NotesModel
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render # new

def front_page(request): # new
    return render(request, 'notes/front.html', {})


class NotesPublicView(APIView):  # http://127.0.0.1:8000/api/notes/notes-public/
    def get(self, request):
        all_notes = NotesModel.objects.all().order_by('?')
        serializer = NotesModelSerializer(instance=all_notes, many=True)

        # Pagination
        no_of_blogs_per_page = 2
        if request.GET.get('page'):
            page_number = request.GET.get('page', 1)
            paginator = Paginator(object_list=all_notes, per_page=no_of_blogs_per_page)
            serializer = NotesModelSerializer(instance=paginator.page(number=page_number), many=True)
            
        return Response({'data': serializer.data, 'message': 'here is the data'}, status=status.HTTP_200_OK)


class NotesView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get(self, request):  #http://127.0.0.1:8000/api/notes/notes-view/
        """ shows data of the logged-in user """
        try:
            logged_in_user = request.user 
            model_instance = NotesModel.objects.filter(writer__exact=logged_in_user)

            if request.GET.get('search'):  # http://127.0.0.1:8000/api/notes/notes-view/?search=music                
                search_criteria = request.GET.get('search') # comes from the search-bar
                model_instance = model_instance.filter(Q(title__icontains = search_criteria) | Q(matter__icontains = search_criteria))           
                
            
            serializer = NotesModelSerializer(instance=model_instance, many=True)
            # specially adding 'agent' because there is no way to get the name of the writer at the front end
            return Response({'data': serializer.data, 'message': 'here is the data', 'agent':request.user.username}, status=status.HTTP_200_OK)
        except Exception as e:
            print('%%%%%%%',e)
            return Response({'data': ''}, status=status.HTTP_400_BAD_REQUEST)
        

    def post(self, request): # http://127.0.0.1:8000/api/notes/notes-view/
        try:
            # received_data = request.data # code used generally, but isn't working here for some reason
            received_data = request.POST.copy()  # to avoid "This QueryDict instance is immutable" the reason or which is not known
            print('****printing received', received_data)
            received_data['writer'] = request.user.id # only accepting id here
            serializer = NotesModelSerializer(data=received_data)
            if not serializer.is_valid():
                return Response({'data':serializer.errors, 'message': 'notes data was invalid'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response({'data': serializer.data, 'message': 'blog created successfully'}, status=status.HTTP_201_CREATED)        
        except Exception as e:
            print('****** error', e)
            return Response({'data': {}, 'message': 'data in wrong format'}, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request): # http://127.0.0.1:8000/api/notes/notes-view/
        try:
            received_data = request.data            
            received_blog_id = received_data.get('id')            
            logged_in_user = request.user.id
            # we should have used .get() below but we used .filter() so that we may 
            # chain another filter later to check the user
            # but this will return a query-set & not an instance ( which .get() would have yielded )
            # now since this is a query-set we're using .first() below to turn it into an instance
            found_blog_to_edit = NotesModel.objects.filter(id=received_blog_id)             
            logged_in_user_is_writer = bool(found_blog_to_edit.filter(Q(writer=logged_in_user)))
            if found_blog_to_edit and logged_in_user_is_writer:
                serializer = NotesModelSerializer(instance=found_blog_to_edit.first(), data = received_data, partial=True)
                if not serializer.is_valid():
                    return Response({'data':serializer.errors, 'message': 'notes data was invalid'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer.save()
                    return Response({'data': serializer.data, 'message': 'blog successfully edited'}, status=status.HTTP_201_CREATED)        
            else:
                return Response({'message': "blog not found / user not permitted"})
                        
        except Exception as e:
            print('****** error', e)
            return Response({'data': {}, 'message': 'data in wrong format'}, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request): # http://127.0.0.1:8000/api/notes/notes-view/        
        try:
            received_data = request.data            
            received_blog_id = received_data.get('id')            
            logged_in_user = request.user.id
            found_blog_to_delete = NotesModel.objects.filter(id=received_blog_id)             
            logged_in_user_is_writer = bool(found_blog_to_delete.filter(Q(writer=logged_in_user)))
            if found_blog_to_delete and logged_in_user_is_writer:
                found_blog_to_delete.delete()
                return Response({'message': "blog entry deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({'message': "blog not found / user not permitted"})
        except Exception as e:
            print('****** error', e)
            return Response({'data': {}, 'message': 'data in wrong format'}, status=status.HTTP_400_BAD_REQUEST)

