from django.contrib.auth import get_user_model
from rest_framework import serializers


# model serializer do is allow us to automatically valide and things to a specific model
class UserSerializer(serializers.ModelSerializers):

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
        return get_user_model.objects.create_user(**validated_data)
