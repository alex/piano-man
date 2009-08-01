import os

from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from django_vcs.models import CodeRepository

register = template.Library()

class OtherRepos(template.Node):
    def __init__(self, repo, varname):
        self.repo = repo
        self.varname = varname

    def render(self, context):
        repo = self.repo.resolve(context)
        if repo:
            repo = repo.id
        else:
            repo = None
        context[self.varname] = CodeRepository.objects.exclude(id=repo)
        return ''

@register.tag
def get_other_repos(parser, token):
    bits = token.split_contents()
    bits.pop(0)
    repo = parser.compile_filter(bits.pop(0))
    varname = bits.pop()
    return OtherRepos(repo, varname)

@register.filter
def urlize_path(path, repo):
    bits = path.split(os.path.sep)
    parts = []
    for i, bit in enumerate(bits[:-1]):
        parts.append('<a href="%(url)s">%(path)s</a>' % {
            'url': reverse('code_browser', kwargs={
                'path': '/'.join(bits[:i+1])+'/',
                'slug': repo.slug
            }),
            'path': bit,
        })
    return ' / '.join(parts + bits[-1:])

@register.inclusion_tag('backstage/nav_bar_urls.html')
def nav_bar_urls(repo, nested):
    return {'repo': repo, 'nested': nested}

@register.inclusion_tag('backstage/chartlist.html', takes_context=True)
def chartlist(context, data, total, option):
    new_context = {
        'data': data,
        'total': total,
        'option': option,
        'request': context['request'],
        'repo': context['repo'],
    }
    return new_context

@register.inclusion_tag('backstage/form.html')
def render_form(form):
    return {'form': form}
