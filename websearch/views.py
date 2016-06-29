from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.validators import URLValidator, ValidationError
from django.shortcuts import render_to_response
from backend.htmlparser import HtmlParser
from models import *
from django.template import RequestContext
from websearch.backend import query_handler


# Create your views here.
def home(request):
    if request.method == "POST":
        query = request.POST.get('query')
    else:
        query = request.GET.get('query')
    if query is None:
        return render_to_response('home.html', {'links': '', 'query': ''})
    links = query_handler.handle_query(query)
    paginator = Paginator(links, 10)

    page = request.GET.get('page')
    try:
        link = paginator.page(page)
    except PageNotAnInteger:
        link = paginator.page(1)
    except EmptyPage:
        link = paginator.page(paginator.num_pages)
    return render_to_response('home.html', {'link': link, 'query': query})


def indexation(request):
    if request.method == "POST":
        indexing_urls = []
        url_validator = URLValidator(schemes=['http', 'https'])
        urls = request.POST.get('url')
        if urls:
            u_list = urls.split(", ")
            for url in u_list:
                try:
                    url_validator(url)
                except ValidationError:
                    continue
                indexing_urls.append(url)

        if len(indexing_urls):
            h = HtmlParser(indexing_urls)
            h.multiproc()
            result = 'Crawler successfully end working!'
        else:
            result = 'No valid URLs'

    else:
        result = ''

    c = RequestContext(request)
    return render_to_response('indexation.html', {'result': result}, c)


def urls(request):
    pages = WebPage.objects.all()
    id_list = []
    for page in pages:
        id_list.append(page.id)
    if not request.method == "POST" or request.POST.get('id') == '':
        return render_to_response('urls.html', {'pages': pages})
    if int(request.POST.get('id')) in id_list:
        WebPage.objects.get(id=request.POST.get('id')).delete()
    return render_to_response('urls.html', {'pages': pages})


def settings(request):

    error = False
    same_values = False
    was_changed = False
    if request.method == 'POST':
        depth = request.POST.get('depth')
        width = request.POST.get('width')
        if depth is None or width is None:
            error = True
        if depth == HtmlParser.depth and width == HtmlParser.width:
            same_values = True
        HtmlParser.depth = int(depth)
        HtmlParser.width = int(width)
        result_of_saving = 'Saved!'
        if not error or not same_values:
            was_changed = True
    else:
        was_changed = False
        result_of_saving = ''

    curr_depth = HtmlParser.depth
    curr_width = HtmlParser.width

    return render_to_response('settings.html',
                              {'result_of_saving': result_of_saving,
                               'curr_depth': curr_depth,
                               'curr_width': curr_width,
                               'was_changed': was_changed,
                               'error': error,
                               'same_values': same_values})
