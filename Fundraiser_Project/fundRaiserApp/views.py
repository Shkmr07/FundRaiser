from rest_framework import viewsets
from .models import Campaign, Donation
from .serializers import CampaignSerializer, DonationSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate,logout,login
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination

import jwt,datetime



class RegisterView(APIView):
    permission_classes= [AllowAny]
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Signup Successfully','data': serializer.data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):

        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request,username=username,password=password)

        if not user: raise AuthenticationFailed('Unauthorized')

        login(request,user)

        payload = {'id' : user.id, 'exp' : datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60),'iat': datetime.datetime.now(datetime.timezone.utc) }
        token = jwt.encode(payload,'cap004',algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwtToken',value=token)
        response.data = {'message': 'Login Successfully','token' : token}
        return response

class LogoutView(APIView):

    def post(self,request):
        logout(request)
        response = Response()
        response.delete_cookie('jwtToken')
        response.delete_cookie('csrftoken')
        response.data = {'message' : 'Logout Successfully'}
        return response


class CampaignView(APIView):

    def getToken(self,request):

        token = request.COOKIES.get('jwtToken')

        if not token : return Response({'message': 'Try to Login First'})
        payload = jwt.decode(token,'cap004',algorithms=['HS256'])
        user = User.objects.get(id=payload['id'])
        print('Maine yeha hu')
        
        return user
        

    def post(self,request):
        user = self.getToken(request)

        if isinstance(user, Response):return user

        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['owner'] = user
            serializer.save()
            return Response({'message': 'Campaign Added Successfully', 'data': serializer.data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,*args, **kwargs):

        user = self.getToken(request)

        if isinstance(user, Response):return user
        
        campaign_id = kwargs.get('pk')
        campaign = Campaign.objects.get(id=campaign_id)

        serializer = CampaignSerializer(campaign,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Campaign Updated Successfully', 'data': serializer.data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self,request,*args, **kwargs):

        user = self.getToken(request)

        if isinstance(user, Response):return user

        campaign_id = kwargs.get('pk')
        campaign = Campaign.objects.get(id=campaign_id)
        campaign.delete()
        return Response({'message': 'Campaign Deleted Successfully'},status=status.HTTP_204_NO_CONTENT)
    


class DonationView(APIView):

    def getToken(self,request):

        token = request.COOKIES.get('jwtToken')

        if not token : return Response({'message': 'Try to Login First'})
        payload = jwt.decode(token,'cap004',algorithms=['HS256'])
        user = User.objects.get(id=payload['id'])
        
        return user

    def post(self,request):

        user = self.getToken(request)

        if isinstance(user, Response):return user

        campaign_owner = Campaign.objects.get(id=request.data['campaign'])

        if campaign_owner.owner.username == user.username: return Response({'message': 'Campaign owner is not allow for Donate'},status=status.HTTP_401_UNAUTHORIZED)
        serializer = DonationSerializer(data=request.data)
        campaign = Campaign.objects.get(id=request.data['campaign']) 
        campaign.current_amount += int(request.data['amount'])
        campaign.save()

        if serializer.is_valid():
            serializer.validated_data['donor'] = user
            serializer.save()
            return Response({'message': 'Donation Added Successfully', 'data': serializer.data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def put(self,request,*args, **kwargs):

        user = self.getToken(request)

        if isinstance(user, Response):return user

        donation_id = kwargs.get('pk')
        donation = Donation.objects.get(id=donation_id)
        serializer = DonationSerializer(donation,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Donation Updated Successfully', 'data': serializer.data},status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,*args, **kwargs):

        user = self.getToken(request)

        if isinstance(user, Response):return user

        donation_id = kwargs.get('pk')
        donation = Donation.objects.get(id=donation_id)

        donation.delete()
        return Response({'message': 'Donation Deleted Sucessfully'},status=status.HTTP_204_NO_CONTENT)
        


# class CampaignPage(PageNumberPagination):

#     page_size = 1
#     page_query_param = 'page_size'
#     max_page_size = 10


# class DonationPage(PageNumberPagination):

#     page_size = 1
#     page_query_param = 'page_size'
#     max_page_size = 10
        
    
class CampaignList(generics.ListAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer 
    # pagination_class = CampaignPage


class DonationList(generics.ListAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    # pagination_class = DonationPage


class getCampaign(APIView):

    def get(self,request,*args, **kwargs):

        campaign_id = kwargs.get('pk')
        campaign = Campaign.objects.get(id=campaign_id)
        serializer = CampaignSerializer(campaign)
        return Response(serializer.data,status=status.HTTP_200_OK)