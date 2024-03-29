import json 
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer  

class NotificationConsumer(WebsocketConsumer):
  def __init__(self,*args,**kwargs):
    super().__init__(args,kwargs)
    self.room_name = None
    self.room_group_name = None

  def connect(self):
    self.room_name = 'notification'
    self.room_group_name = 'notification_group'


    self.accept()

    async_to_sync(self.channel_layer.group_add)(
      self.room_group_name,self.channel_name
    )

  def disconnect(self,close_code):
    async_to_sync(self.channel_layer.group_discard)( 
      self.room_group_name,self.channel_name
    )

  def receive(self,text_data=None,bytes_data=None):
    text_data_json = json.loads(text_data)
    

    self.room_name = text_data_json['room_name']
    self.room_group_name = text_data_json['room_group_name']


    async_to_sync(self.channel_layer.group_add)(
      self.room_group_name,self.channel_name
    )


    # async_to_sync(self.channel_layer.group_send)(
    #   self.room_group_name,
    #   {
    #     'type':'send_notification',
    #     'message':json.dumps({'message':'Greetings dude ! Happy to connect'}),
    #   }
    # )

  def send_notification(self,event):
    self.send(text_data=json.dumps(event))

