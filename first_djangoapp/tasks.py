from django.contrib.auth.models import User 
from celery import shared_task
from datetime import datetime, timedelta
import pytz
from pytz import utc
from blog.models import Post
from django.core.mail import send_mail
from first_djangoapp import settings

@shared_task(bind= True)
def email_task(self):
    list1 = ""
    diff_time = datetime.now(tz = pytz.timezone('UTC')) - timedelta(hours = 1)
    post_objs = Post.objects.all()
    for i in range(len(post_objs)):
        if (diff_time - post_objs[i].date).days == 1:
            list1+=post_objs[i].title + " "
# filter(date__gte)
    # recipient 
    r_email = []
    us_obj = User.objects.all()
    for i in range(len(us_obj)):
        r_email.append(us_obj[i].email)

    subject = 'New Blogs'
    message = list1
    print(message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = r_email
    send_mail(subject, message, email_from, recipient_list)
    return "mailsend"

 
    # diff_time.replace(tzinfo=utc)
    # x = datetime.now(tz=pytz.timezone('UTC'))
#      for i in range(0,a):
# ...     if (diff_time - post_date1).days == 11 : 
# ...             print("hi")





'''
admin credentials in login
find the number of new blogs (created, updated)

date as a checker 

if id exists then updated and id doesnt exists add it to created 

# code 
created and updated

if user_id exists 
    then add to created else add it to updated

combine the result and parse it to message varible of email
'''