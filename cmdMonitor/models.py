# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mongoengine import *

# Create your models here.

class Logs(Document):
	timestamp = DateTimeField()
	cmd = StringField()
	host = StringField()
	user = StringField()
	identity =  StringField()

	def __str__(self):
		return self.user+':'+self.identity+'@'+self.host+"#"+self.cmd	
