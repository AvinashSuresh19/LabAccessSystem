from myapp.models import news, userData, userTempData, ris
from rest_framework import serializers

class newsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = news
        fields = ('__all__')
		
class userDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = userData
        fields = ('__all__')

class userTempDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = userTempData
        fields = ('__all__')
        
class risSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ris
        fields = ('__all__')