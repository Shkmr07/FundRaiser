from rest_framework import serializers
from .models import Campaign, Donation
from django.contrib.auth.models import User
import re

class CampaignSerializer(serializers.ModelSerializer):
    owner_detail = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        exclude = ['owner']  # Exclude the 'owner' field

    def get_owner_detail(self, obj):
        return {
            'id': obj.owner.id,
            'username' : obj.owner.username,
            'firstname': obj.owner.first_name,
            'email': obj.owner.email,
        }

        

class DonationSerializer(serializers.ModelSerializer):
    donor_detail = serializers.SerializerMethodField()

    class Meta:
        model = Donation
        exclude = ['donor']  # Exclude the 'owner' field

    def get_donor_detail(self, obj):
        return {
            'id': obj.donor.id,
            'username': obj.donor.first_name,
            'email': obj.donor.email,
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['first_name','last_name','username','password','email']
        extra_kextra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):

        if len(data['password']) < 8: raise serializers.ValidationError({'message' : 'Password must be greater or equal to 8'})

        if not re.search(r'[A-Z]', data['password']) or not re.search(r'[a-z]', data['password']) or not re.search(r'\d', data['password']):
            raise serializers.ValidationError({'message' : 'Password must contain at least one lowercase and uppercase letter and contain one digit'})
        return data
    
    def create(self,validated_data):

        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None: instance.set_password(password)
        instance.save()
        return instance 
