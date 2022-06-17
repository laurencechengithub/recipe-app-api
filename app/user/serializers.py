from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers


# model serializer do is allow us to automatically valide and things to a specific model
class UserSerializer(serializers.ModelSerializer):

    #class meta tells django the model and the fields or any additial argements
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        #kwargs tells django whats the keyword arguments are
        extra_kwargs = {
            'password':{'write_only':True,'min_length':5 }
        }

    #create is called only after the validation pass
    def create(self, validated_data):
        """create and return a user with encrypte"""
        return get_user_model().objects.create_user(**validated_data)

class AuthTokenSerializer(serializers.Serializer):

    email = serializer.EmailField()
    password = serializer.CharField(
        style={'input_type':'password'},
        trim_whitespace=False,
    )

    def validete(self, attrs):
        """validate and auth the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            #authenticate comes from django
            request=self.context.get('request'),
            #get the request context
            username=email,
            #since we are setting the username as the email add. here
            password=password,
        )

        if not user:
            msg = _('Unable to auth with provided credentails')
            raise serializers.ValidationError(msg, code='authorization')
            #raisee a valiation error

        attrs['user'] = user
        return attrs