import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from mygpu import MyGpu

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)

class COMPAREGPU(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        firstgpu = self.request.GET.get("GPU1")
        secondgpu = self.request.GET.get("GPU2")
       
        gpu_array = MyGpu.query()
        #if firstgpu == secondgpu:
            #error = "GPU's name Should not be same"
        user_array = MyGpu.query().fetch()
        
        template_values = {
            'gpu_array' : gpu_array,
            'firstgpu' : firstgpu,
            'secondgpu' : secondgpu,
            #'error' : error,
            }
        template = JINJA_ENVIRONMENT.get_template('CompareGPU.html')
        self.response.write(template.render(template_values))
        
   