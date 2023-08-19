from django.db import models
from django.conf import settings

class TgMessages(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	msgtext = models.CharField(max_length=450, default=None, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.msgtext[:28]} by {self.user}- #{self.pk}"
	
class ChatIdList(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	chat_id = models.BigIntegerField()
	first_msg_token = models.CharField(max_length=50)

	def __str__(self):
		return f"{self.chat_id}- {self.first_msg_token} by {self.user}- #{self.pk}"

