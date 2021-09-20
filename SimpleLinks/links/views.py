from json.encoder import JSONEncoder
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from super_manger.models import siteAttr
from .models import site_map

from .transactions import siteaction

# Create your views here.


def dashboard(request):
    return render(request, 'home/dashboard.html', {})

# Site manger


@permission_required('AddSite', raise_exception=True)
def add_site(request):
    siteid_ = siteAttr.objects.get(key='siteid')
    sitename_ = siteAttr.objects.get(key='sitename')
    contex = {
        'siteid_': siteid_,
        'sitename_': sitename_,
    }
    if request.method == "POST":
        error = ''
        siteid = request.POST['siteid']
        sitename = request.POST['sitename']
        longitude = request.POST['longitude']
        Latitude = request.POST['Latitude']
        site_weight = request.POST['site_weight']
        try:
            add_site_ = site_map(site_id=siteid, site_name=sitename,
                                 site_long=longitude, site_lat=Latitude, site_weight=site_weight)
            add_site_.save()
            error = 'Site ' + str(siteid) + ' added Succssfuly'
        except Exception as e:
            error = str(r)
        contex = {
            'siteid_': siteid_,
            'sitename_': sitename_,
            'error': error,
        }

    return render(request, 'sitemanger/add_site.html', contex)


def site_manger(request):
    site_map_data = site_map.objects.all().order_by('-id')
    siteid_ = siteAttr.objects.get(key='siteid')
    sitename_ = siteAttr.objects.get(key='sitename')
    contex = {
        'siteid_': siteid_,
        'sitename_': sitename_,
        'site_map_data': site_map_data,
        'title':'Sites Manger'
    }
    if request.method == "POST":
        if request.POST['action'] == "check_site_name" and request.is_ajax():
            if site_map.objects.filter(siteid=request.POST['siteid']).exists():
                return HttpResponse('1')
            else:
                return HttpResponse('0')
        if request.POST['action'] == "site_manger_add" and request.is_ajax():
            DB = siteaction('site_manger_add', request)
            if DB.commit() is not None:
                status = {
                    'error': '1',
                    'msg': DB.commit(),
                    'TableData':DB.TableData()
                }
            else:
                status={
                    'error': '0',
                    'msg': 'Site added success',
                    'TableData':DB.TableData()
                }
            return JsonResponse(status,safe=False)
        if request.POST['action'] == "site_manger_edit" and request.is_ajax():
            DB = siteaction('site_manger_edit', request)
            if DB.commit() is not None:
                status = {
                    'error': '1',
                    'msg': DB.commit(),
                    'TableData':DB.TableData()
                }
            else:
                status={
                    'error': '0',
                    'msg': 'Site edit success',
                    'TableData':DB.TableData()
                }
            return JsonResponse(status,safe=False)
            # if DB.commit() is not None:
            #     contex['msg'] = DB.commit()
    return render(request, 'sitemanger/index.html', contex)


def site_manger_delete(request):
    try:
        site_map.objects.filter(id=request.POST['id']).delete()
        status = {
            'error': '0',
            'msg': 'Site removed from list'
        }
    except Exception as e:
        status = {
            'error': '1',
            'msg': 'Failed'
        }
    return JsonResponse(status, safe=False)


def maps(request):
    return render(request,'map/index.html',{})


def initialization_(request):
    if request.method == "POST" and request.is_ajax():
        if request.POST['action'] == 'initialization_':
            initialization_data=list(site_map.objects.all().values('siteid','long','lat'))
            # JSONEncoder(initialization_data)
            return JsonResponse(initialization_data,safe=False)
        return HttpResponse("asd")
    return HttpResponse("asdsad")