from django.template import Library

register = Library()


def calc_percentage(value,args):
  res = (value * args)//100
  res = value - res
  return res

def get_percentage(value,args):
  return (args / value) * 100

def mul(value,args):
  return value * args 

def div(value,args):
  return int(value // args)

register.filter('mul',mul)
register.filter('calc_percentage',calc_percentage)
register.filter('get_percentage',get_percentage)
register.filter('div',div)