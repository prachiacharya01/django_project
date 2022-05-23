from pyexpat import model
from rest_framework import serializers
from .models import Post,comment
import datetime
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title','content','date','author','likes']

    # def get_date(self, obj):

    #     date = serializers.DateTimeField(default=serializers.CreateOnlyDefault(timezone.now))


    def get_deadline(self, obj):
            deadline = self.context['request'].data.get('date')
            # try to convert deadline if its in Wed, Mar 10, 2021 7:19 PM format
            try:
                # convert giving date to datetime in this format Wed, Mar 10, 2021 7:19 PM
                d = datetime.strptime(deadline, '%a, %b %d, %Y %I:%M %p')
                # convert it to 2021-3-10 7:48:22 format
                r = d.strftime("%Y-%m-%d %I:%M:%S")
                return r # or return "blabla" works fine also
            except Exception as E:
                print(E)
            return obj.deadline

class commentSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = comment
        fields = '__all__'

