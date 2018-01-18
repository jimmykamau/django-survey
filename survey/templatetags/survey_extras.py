# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from django import template
from future import standard_library
from django.utils.translation import gettext_lazy as _
import re

standard_library.install_aliases()

register = template.Library()


def collapse_form(form, category):
    """ Permit to return the class of the collapsible according to errors in
    the form. """
    categories_with_error = set()
    for field in form:
        if field.errors:
            categories_with_error.add(field.field.widget.attrs["category"])
    if category.name in categories_with_error:
        return "in"
    return ""


register.filter('collapse_form', collapse_form)


class CounterNode(template.Node):

    def __init__(self):
        self.count = 0

    def render(self, context):
        self.count += 1
        return self.count


@register.tag
def counter(parser, token):
    return CounterNode()


class ExprNode(template.Node):
    def __init__(self, expr_string, var_name):
        self.expr_string = expr_string
        self.var_name = var_name

    def render(self, context):
        try:
            clist = list(context)
            clist.reverse()
            d = {}
            d['_'] = _
            for c in clist:
                d.update(c)
            if self.var_name:
                context[self.var_name] = eval(self.expr_string, d)
                return ''
            else:
                return str(eval(self.expr_string, d))
        except:
            raise


r_expr = re.compile(r'(.*?)\s+as\s+(\w+)', re.DOTALL)


def do_expr(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise(template.TemplateSyntaxError,
            "%r tag requires arguments" % token.contents[0])
    m = r_expr.search(arg)
    if m:
        expr_string, var_name = m.groups()
    else:
        if not arg:
            raise(template.TemplateSyntaxError,
                "%r tag at least require one argument" % tag_name)

        expr_string, var_name = arg, None
    return ExprNode(expr_string, var_name)


do_expr = register.tag('expr', do_expr)
