import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from mygpu import MyGpu
from edit import Edit
from CompareGPU import COMPAREGPU
from GPUList import GPUListclass

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)

class MainPage(webapp2.RequestHandler):

	def get(self):
		self.response.headers['Content-Type'] = 'text/html'

        # URL that will contain a login or logout link
        # and also a string to represent this
		url = ''
		url_string = ''
		welcome = 'Welcome back'
				# pull the current user from the request
		user = users.get_current_user()

		if user:
			url = users.create_logout_url(self.request.uri)
			url_string = 'logout'

		else:
			url = users.create_login_url(self.request.uri)
			url_string = 'login'


		template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
			
		}

        # pull the template file and ask jinja to render
        # it with the given template values
		template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(template.render(template_values))

	def post(self):
		self.response.headers['Content-Type'] = 'text/html'

		# URL that will contain a login or logout link
		# and also a string to represent this
		url = ''
		url_string = ''
		welcome = 'Welcome back'

		# pull the current user from the request
		user = users.get_current_user()

		if not user:
			return self.redirect("/")

		name = self.request.get('name')

		mygpu_key = ndb.Key('MyGpu',name)
		mygpu = mygpu_key.get()

		if mygpu:
			return self.redirect("/")

		mygpu = MyGpu(id = name)
		mygpu.dateIssued, mygpu.manufacturer = str(self.request.get('date_issued')), self.request.get('manu')
		mygpu.geometryShader = self.request.get('geometryShader') == "on"
		mygpu.tesselationShader= self.request.get('tesselationShader') == "on"
		mygpu.shaderInt16 = self.request.get('shaderInt16') == "on"
		mygpu.sparseBinding = self.request.get('sparseBinding') == "on"
		mygpu.textureCompressionETC2 = self.request.get('textureCompressionETC2') == "on"
		mygpu.vertexPipelineStoresAndAtomics = self.request.get('vertexPipelineStoresAndAtomics') == "on"
		mygpu.put()
		self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/edit',Edit),
    ('/CompareGPU',COMPAREGPU),
    ('/GPUList',GPUListclass),
],debug=True)
