import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os

from tornado.options import define, options

define("port", default=8888, help="run on port", type=int)


class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/login", AuthLoginHandler),
			(r"/logout", AuthLogoutHandler),
		]
		settings = dict(
			login_url = "/auth/login",
			template_path = os.path.join(os.path.dirname(__file__),"templates"),
			static_path = os.path.join(os.path.dirname(__file__),"static"), 
		)
		tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return None


class MainHandler(BaseHandler):
	def get(self):
		self.render("index.html")


class AuthLoginHandler(BaseHandler):
	def get(self):
		self.render("login.html")


class AuthLogoutHandler(BaseHandler):
	def get(self):
		self.write("Logout Handler")


def main():
	tornado.options.parse_command_line()
	app = Application()
	app.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
	main()