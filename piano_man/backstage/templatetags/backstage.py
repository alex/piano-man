from django import template

from django_vcs.models import CodeRepository

register = template.Library()

class OtherRepos(template.Node):
    def __init__(self, repo, varname):
        self.repo = repo
        self.varname = varname

    def render(self, context):
        repo = self.repo.resolve(context)
        if not repo:
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
