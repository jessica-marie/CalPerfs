#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import jinja2
import os
import webapp2
import random
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users

jinja_environment = jinja2.Environment(loader= jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Availability(ndb.Model):
    name = ndb.StringProperty(required=True)
    month=ndb.IntegerProperty()
    year=ndb.IntegerProperty()
    monday = ndb.FloatProperty(repeated=True)
    tuesday = ndb.FloatProperty(repeated=True)
    wednesday = ndb.FloatProperty(repeated=True)
    thursday = ndb.FloatProperty(repeated=True)
    friday = ndb.FloatProperty(repeated=True)
    saturday = ndb.FloatProperty(repeated=True)
    sunday = ndb.FloatProperty(repeated=True)
    daysGone= ndb.IntegerProperty(repeated=True)
    badTime= ndb.FloatProperty(repeated=True)
    goodTime= ndb.FloatProperty(repeated=True)

class Show(ndb.Model):
    name = ndb.StringProperty(required=True)
    month  = ndb.IntegerProperty()
    year  = ndb.IntegerProperty()
    date = ndb.IntegerProperty()
    numHM = ndb.IntegerProperty()
    numAHM = ndb.IntegerProperty()
    numUsher = ndb.IntegerProperty()
    HM1 = ndb.FloatProperty()
    HM2 = ndb.FloatProperty()
    AHM1 = ndb.FloatProperty()
    AHM2 = ndb.FloatProperty()
    usher1 = ndb.FloatProperty()
    usher2 = ndb.FloatProperty()
    start  = ndb.FloatProperty()
    location = ndb.StringProperty()
    FOH = ndb.StringProperty()
    note = ndb.StringProperty()

class Schedule(ndb.Model):
    shows = ndb.JsonProperty(repeated=True)

class HomeHandler(webapp2.RequestHandler):
	def get(self):
		current_user = users.get_current_user() 
		template_values = {'email':current_user.email(),'logout_url':users.create_logout_url("/"),'message':''}
		template = jinja_environment.get_template('home.html')
		self.response.out.write(template.render(template_values))
class EditHandler(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		template = jinja_environment.get_template('edit.html')
		self.response.out.write(template.render(template_values))
class CreateHandler(webapp2.RequestHandler):
	def get(self):
		now = datetime.datetime.now()
		template_values = {'year':now.year}
		template = jinja_environment.get_template('create.html')
		self.response.out.write(template.render(template_values))
class AddHandler(webapp2.RequestHandler):
	def get(self):
		now = datetime.datetime.now()
		template_values = {'year':now.year,'yearOne':str(now.year),'yearTwo':str(now.year+1)}
		template = jinja_environment.get_template('add.html')
		self.response.out.write(template.render(template_values))
	def post(self):
		s=Show()
		s.name=self.request.get('show')
		s.year=int(self.request.get('chosenYear'))
		s.month=int(self.request.get('month'))
		s.date=int(self.request.get('date'))
		s.numHM=int(self.request.get('numHM'))
		s.numAHM=int(self.request.get('numAHM'))
		s.numUsher=int(self.request.get('numUsher'))
		s.HM1=float(self.request.get('HM1'))
		s.HM2=float(self.request.get('HM2'))
		s.AHM1=float(self.request.get('AHM1'))
		s.AHM2=float(self.request.get('AHM2'))
		s.usher1=float(self.request.get('USHER1'))
		s.usher2=float(self.request.get('USHER2'))
		s.start=float(self.request.get('start'))
		s.location=str(self.request.get('loc'))
		s.FOH=str(self.request.get('FOH'))
		s.note=self.request.get('notes')
		s.put()
		now = datetime.datetime.now()
		template_values = {'year':now.year,'yearOne':str(now.year),'yearTwo':str(now.year+1),'message':'Thank you the show has been recorded'}
		template = jinja_environment.get_template('add.html')
		self.response.out.write(template.render(template_values))
class TradeHandler(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		template = jinja_environment.get_template('trade.html')
		self.response.out.write(template.render(template_values))
class ScheduleHandler(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		template = jinja_environment.get_template('schedule.html')
		self.response.out.write(template.render(template_values))
class ScheduleNewHandler(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		template = jinja_environment.get_template('scheduleNew.html')
		self.response.out.write(template.render(template_values))
class AvailabilityHandler(webapp2.RequestHandler):
	def get(self):
		now = datetime.datetime.now()
		template_values = {'year':now.year,'yearOne':str(now.year),'yearTwo':str(now.year+1)}
		template = jinja_environment.get_template('availability.html')
		self.response.out.write(template.render(template_values))
	def post(self):
		a=Availability()
		a.name=self.request.get('name')
		a.month=int(self.request.get('month'))
		a.year=int(self.request.get('chosenYear'))
		tempDays = self.request.get('not', allow_multiple=True)
		badDays=[]
		for item in tempDays:
			badDays.append(int(item))
		a.daysGone=badDays
		a.put()
		template_values = {'message':'Thank you your availability has been recorded'}
		template = jinja_environment.get_template('home.html')
		self.response.out.write(template.render(template_values))
class ShowsHandler(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		template = jinja_environment.get_template('shows.html')
		self.response.out.write(template.render(template_values))
app = webapp2.WSGIApplication([('/shows', ShowsHandler),
				('/availability', AvailabilityHandler),
				('/schedule', ScheduleHandler),
				('/scheduleNew', ScheduleNewHandler),
				('/trade', TradeHandler),
				('/add', AddHandler),
				('/create', CreateHandler),
				('/edit', EditHandler),
				('/.*', HomeHandler)],
                              debug=True)
