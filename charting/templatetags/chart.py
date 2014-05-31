# coding=UTF-8
from django.template import Library, Node, Variable, TemplateSyntaxError

from myproject.charting.populatecharts import *
 
register = Library()

class Chart(Node):
    def __init__(self, arg):
         self.arg = Variable(arg)

    def render(self, context):
        # If size is not an int, then it's a Variable, so try to resolve it.
        context['me'] = '2' #self.arg
        canvas = tsimple()#self.arg.resolve(context)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)
        return 'me' 


@register.tag
def get_chart(parser, token):
    try:
        data = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    return Chart(data[1])

