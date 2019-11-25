from __future__ import absolute_import, unicode_literals

from django import template

from towel.utils import parse_args_and_kwargs, resolve_args_and_kwargs


register = template.Library()


@register.tag
def testtag(parser, token):
    return TestNode(*parse_args_and_kwargs(parser, token.split_contents()[1:]))


class TestNode(template.Node):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs

    def render(self, context):
        args, kwargs = resolve_args_and_kwargs(context, self.args, self.kwargs)

        return "ARGS: %s\nKWARGS: %s\n" % (
            ",".join(str(arg) for arg in args),
            ",".join("%s=%s" % (k, v) for k, v in sorted(kwargs.items())),
        )
