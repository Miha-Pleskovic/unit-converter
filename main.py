#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "html")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("unit-converter.html")

    def post(self):
        number = self.request.get("number")
        unit = self.request.get("unit").lower()
        converting_unit = self.request.get("converting_unit").lower()
        if number.replace(".", "").isdigit() or number.isdigit():
            if unit == "kilometer" or unit == "kilometra" or unit == "kilometri" or unit == "kilometrov":
                if converting_unit == "meter" or converting_unit == "metre":
                    total = float(number) * 1000
                    result = number + " kilometer/-ov je enako " + str(total) + " meter/-ov."
                    self.write(result)
                elif converting_unit == "milje":
                    total = float(number) * 0.62137
                    result = number + " kilometer/-ov je enako " + str(total) + " milja/-lj."
                    self.write(result)
                else:
                    result = "V polje ste vpisali enoto, ki je ne prepoznamo. Želite pretvoriti v metre ali milje?"
                    self.write(result)
            elif unit == "meter" or unit == "metra" or unit == "metri" or unit == "metrov":
                if converting_unit == "kilometer" or converting_unit == "kilometre":
                    total = float(number) / 1000
                    result = number + " meter/-ov je enako " + str(total) + " kilometer/-ov."
                    self.write(result)
                elif converting_unit == "milje":
                    total = float(number) * 0.00062137
                    result = number + " meter/-ov je enako " + str(total) + " milja/-lj."
                    self.write(result)
                else:
                    result = "V polje ste vpisali enoto, ki je ne prepoznamo. Želite pretvoriti v kilometre ali milje?"
                    self.write(result)
            elif unit == "milja" or unit == "milji" or unit == "milje" or unit == "milj":
                if converting_unit == "meter" or converting_unit == "metre":
                    total = float(number) / 0.00062137
                    result = number + " milja/-lj je enako " + str(total) + " meter/-ov."
                    self.write(result)
                elif converting_unit == "kilometer" or converting_unit == "kilometre":
                    total = float(number) / 0.62137
                    result = number + " milja/-lj je enako " + str(total) + " kilometer/-ov."
                    self.write(result)
                else:
                    result = "V polje ste vpisali enoto, ki je ne prepoznamo. Želite pretvoriti v metre ali kilometre?"
                    self.write(result)
            else:
                result = "V polje ste vpisali enoto, ki je ne prepoznamo. Prosimo, poskusite s kilometri, metri ali miljami."
                self.write(result)
        else:
            result = "V polje za količino niste pravilno vpisali številk. Prosimo, poskusite znova."
            self.write(result)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler)
], debug=True)
