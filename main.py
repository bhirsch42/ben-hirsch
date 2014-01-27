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
import webapp2
from Handler import *
from PersonalHandler import *

class MainHandler(Handler):
    def get(self):
        self.render("front.html")

class ResumeHandler(Handler):
	def get(self):
		self.render("resume.html")

class ResumeSourceHandler(Handler):
	def get(self):
		self.render("resume-source.html")

class BioHandler(Handler):
	def get(self):
		self.render("bio.html")

class ContactHandler(Handler):
	def get(self):
		self.render("contact.html")

class SampleWorksHandler(Handler):
	def get(self):
		self.render("sampleworks.html")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/resume', ResumeHandler),
    ('/resume-source', ResumeSourceHandler),
    ('/bio', BioHandler),
    ('/contact', ContactHandler),
    ('/sampleworks', SampleWorksHandler),
    ('/personal', PersonalHandler)
 ], debug=True)
