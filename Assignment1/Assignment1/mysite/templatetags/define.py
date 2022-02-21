from django import template
from django.conf import settings
import logging
import re
register = template.Library()

NAMESPACE_PROTECTION = settings.DEBUG

class define_node(template.Node):
  def __init__(self, value, key, parse):
    self.value = value
    self.key = key
    self.parse = parse
  def render(self, context):
    if self.parse:
      context[self.key] = context[self.value]
    else:
      context[self.key] = self.value
    return ''

@register.tag
def define(parser, token):
  """Definition template tag. Use to define variables in your context within the template.
  Sorta like the {% with "blah" as blah %} tag, but without the {% endwith %} mess.

  Supports two modes:
  Literal mode: argument is encapsulated with quotes (e.g. "blah" or 'blah')
                variable, is set to the string literal, ex:
                {% define "fish" as foo %}
  Variable mode: argument is prefixed with a $ (e.g. $blah or $monkey)
                 variable is copied from another context variable, ex:
                 {% define $fish as foo %}

  Namespace protection is also provided if django.conf.settings.DEBUG is True.
  You will get an epic namespace fail if that occurs (please fix it before you deploy)

  TODO:
    * define override nomenclature if you REALLY want to overwrite a variable
      - should decide what nomeclature to use first
    * expand on variables so that {% define $array.blah as foo %} will work
      (this currently WILL NOT)
  """
  try:
    tag_name, arg = token.contents.split(None, 1)
  except ValueError:
      raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
  m = re.search(r'(.*?) as (\w+)', arg)
  if not m:
      raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
  value, key = m.groups()
  if (value[0] == value[-1] and value[0] in ('"', "'")):
    ret = value[1:-1]
    parse = False
  elif (value[0] == '$'):
    ret = value[1:]
    parse = True
  else:
      raise template.TemplateSyntaxError("%r tag's first argument indeciperable" % tag_name)
  return define_node(ret, key, parse)