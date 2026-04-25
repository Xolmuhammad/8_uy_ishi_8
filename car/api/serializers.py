from rest_framework import serializers
from .models import *
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()



class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(min_length=8,max_length=126,write_only=True)
    password2 = serializers.CharField(min_length=8,max_length=126,write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1','password2')

    def validate(self,attrs):
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")

        if password1 != password2:
            raise serializers.ValidationError({
                "password":"Parollar bir biriga mos emas"
            })

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        return User.objects.create_user(**validated_data,password=password)


class CarSerializerForCourse(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id','car_name','car_year','price')
        read_only_fields = ('id','brand')

    def validate_car_name(self,value):
        if not value.istitle():
            raise serializers.ValidationError("Mashina ismining bosh harfi kattada bo'lishi kerak!")

        if not value.isalpha():
            raise serializers.ValidationError("Mashina ismi harflardan tashkil topgan bo'lishi kerak")
        return value

    def validate_car_year(self, value):
        hozirgi_yil = datetime.now().year
        if value.year < (hozirgi_yil - 50) or value.year > hozirgi_yil:
            raise serializers.ValidationError(
                "Mashina 50 yildan eski yoki kelajakda ishlab chiqarilgan bo'lmasligi kerak")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Narx musbat son bo'lishi kerak!")

        if value > 999999999:
            raise serializers.ValidationError("Narx juda baland. Iltimos, qayta tekshiring.")

        return value

class BrandSerializer(serializers.ModelSerializer):
    # cars = serializers.StringRelatedField(many=True)
    # cars = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    # cars = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='car-detail')
    # cars = serializers.SlugRelatedField(many=True,read_only=True,slug_field='car_name')
    url = serializers.HyperlinkedIdentityField(view_name='brands-detail')
    cars = CarSerializerForCourse(many=True, source='brands', read_only=True)
    class Meta:
        model = Brand
        fields = '__all__'
        read_only_fields = ('id',)


    def create(self, validated_data):
        cars_data = validated_data.pop('cars')
        brand = Brand.objects.create(**validated_data)
        for car_data in cars_data:
            Car.objects.create(brand=brand, **car_data)
        return brand


    def validate_name(self,value):
        if not value.istitle():
            raise serializers.ValidationError("Ismning bosh harfi katta bo'lishi kerak!")

        if not value.isalpha():
            raise serializers.ValidationError("Ism faqat harflardan tashkil topgan bo'lishi kerak")
        return value

    def validate_country(self, value):
        if not value.istitle():
            raise serializers.ValidationError("Davlatning bosh harfi katta bo'lishi kerak!")

        if not value.isalpha():
            raise serializers.ValidationError("Davlat faqat harflardan tashkil topgan bo'lishi kerak")
        return value

    def validate_founded_year(self, value):
        hozirgi_yil = datetime.now().year
        if not value > hozirgi_yil-150 and value < hozirgi_yil:
            raise serializers.ValidationError("Brand 150 yildan eski bo'lmasligi kerak ")
        return value

class BrandAminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id','name','country','founded_year')
        read_only_fields = ('id',)


class CarSerializer(serializers.ModelSerializer):
    brand = serializers.CharField()
    class Meta:
        model = Car
        fields = ('id','name','country','founded_year','brand')
        read_only_fields = ('id',)