from recomm.models import Assistant

# Init the assistant user
def run():
   print('Init the assistant user...')
   assistant = Assistant(id=0, assistant_name="admin", assistant_password='0000')
   assistant.save()