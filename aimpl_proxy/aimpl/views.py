# -*- coding: utf-8 -
import hashlib
import hmac
import time
import asyncore, socket
import anyjson


from django import http
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.conf import settings
from django.core.servers.basehttp import is_hop_by_hop
from django.contrib.auth.decorators import login_required


import restkit
from restkit import httpc

from aimpl_proxy.aimpl.models import ProblemList
from aimpl_proxy.aimpl.utils import make_path, encode_params, coerce_put_post, url_quote


HOST = (settings.WEB_PROXY_DOMAIN, settings.WEB_PROXY_PORT)

PROXY_BASE_PATH = "/".join(["", settings.WEB_PROXY_BASE])

connection = httpc.HttpClient(max_size=8)

def default_headers(path, index):
    return {
        "X-AIMPL-Path": path,
        "X-Aimpl-IndexPath": index
    }

def is_plname(fun):
    def decorated(request, plname, *args, **kwargs):
        pls = ProblemList.objects.filter(name=plname)
        if pls.count()>0:
            pl = pls[0]
            return fun(request, pl.path, *args, **kwargs)
        raise Http404
    return decorated


# Utility methods
def has_group(request, group, plname=None):
    user = getattr(request, 'user')
    if user and user.is_authenticated():
        if user.groups.filter(name=group).count() > 0:
            return not plname or ProblemList.objects.filter(path=plname, editors=user).count() > 0
    return False
    
def is_priv(request, plname=None):
    if not plname: return False
    return ProblemList.objects.filter(path=plname, editors=request.user).count() > 0
    
def privileges(request):
    if request.user and request.user.is_authenticated():
        return ProblemList.objects.filter(editors=request.user)
    return []
    
def chief_editor_required(fun):
    def decorated(request, *args, **kwargs):
        if request.method != 'GET' and not has_group(request, 'Chief Editors'):
            return http.HttpResponseForbidden('Access Denied')
        return fun(request, *args, **kwargs)
    return decorated
    
def editor_required(fun):
    def decorated(request, *args, **kwargs):
        if request.method != 'GET' and \
                not has_group(request, 'Chief Editors') and \
                not has_group(request, 'Editors', plname):
            return http.HttpResponseForbidden('Access Denied')
        return fun(request, *args, **kwargs)
    return decorated

def editor(fun):
    def decorated(request, plname, *args, **kwargs):
        if not has_group(request, 'Chief Editors') and \
                not has_group(request, 'Editors', plname):
            return http.HttpResponseForbidden('Access Denied')
        return fun(request, plname, *args, **kwargs)
    return decorated


def static(request, path=None):
    if request.method == "GET" and (path is not None and not path.startswith("/aimpl")):
        path1 = make_path(PROXY_BASE_PATH, request.get_full_path())
    else:
        path1 = request.get_full_path()
    return proxy(request, path1, headers=default_headers(PROXY_BASE_PATH, 
                                                settings.WEB_PROXY_INDEX))

# Views
@chief_editor_required
def index(request):
    if request.method == "POST" or request.method == "PUT":
        return proxy(request, PROXY_BASE_PATH, headers=default_headers(PROXY_BASE_PATH, 
						settings.WEB_PROXY_INDEX))
	
    params = {
        "include_docs": True
    }
    path = make_path(PROXY_BASE_PATH, "_list/index/pls", **encode_params(params))
    return proxy(request, path, headers=default_headers(PROXY_BASE_PATH, 
                                                settings.WEB_PROXY_INDEX))
@is_plname
@editor_required
def pl_detail(request, plname, version=None):
    key=plname
    if version:
        key += "/v%s" % version
    params = {
        "startkey": [key],
        "endkey": [key, {}],
        "include_docs": True
    }
    
    path = make_path(PROXY_BASE_PATH, "_list/pl/pl_with_sections", **encode_params(params))
    return proxy(request, path, plname=plname, 
                headers=default_headers(PROXY_BASE_PATH, 
                                settings.WEB_PROXY_INDEX))
@is_plname
@editor_required
def sec_detail(request, plname, version=None, secnum=None, blocknum=None):
    key=plname
    if version:
        key += "/v%s" % version
    params = {
        "startkey": [key,int(secnum)],
        "endkey": [key,int(secnum), {}],
        "include_docs": True
    }
    path = make_path(PROXY_BASE_PATH, "_list/section/pl_full", **encode_params(params))
    return proxy(request, path, plname=plname, 
                headers=default_headers(PROXY_BASE_PATH,
                                settings.WEB_PROXY_INDEX))

@login_required
def remark_queue(request):
    user = request.user
    if user.groups.filter(Q(name='Chief Editor') | Q(name='Editors')).count() <= 0:
        return http.HttpResponseForbidden('Access Denied')

    path = make_path(PROXY_BASE_PATH, "_list/remarksqueue/remarks")
    if not user.groups.filter(name='Chief Editor'):
        path = make_path(PROXY_BASE_PATH, "_list/remarksqueue/web_remarks")
        problems = ProblemList.objects.filter(editors=user)
        if problems.count() > 0:
            payload = {
                "keys": [p.name for p in problems]
            }
            request._raw_post_data = anyjson.serialize(payload).encode('utf-8')
            
            request.META['CONTENT_TYPE'] = 'application/json'
            request.META['CONTENT_LENGTH'] = len(request._raw_post_data)
            request.method = "POST"
            request.META['METHOD'] = "POST"
    
    return proxy(request, path, headers=default_headers(PROXY_BASE_PATH,
                                    settings.WEB_PROXY_INDEX))
   
@editor
@login_required                         
def remark_moderate(request, plname):
    params = {
        "startkey": [plname],
        "endkey": [plname, {}]
    }
    path = make_path(PROXY_BASE_PATH, "_list/remarksqueue/remarks", **encode_params(params))
    return proxy(request, path, plname=plname, headers=default_headers(PROXY_BASE_PATH,
                                     settings.WEB_PROXY_INDEX))

def remark_detail(request, plname, secnum, blocknum, remarknum):
    params = {
        "startkey": [plname,int(secnum), int(blocknum), int(remarknum)],
        "endkey": [plname,{},int(secnum), int(blocknum), int(remarknum)],
        "include_docs": True
    }
    headers = {"X-AIMPL-Path": PROXY_BASE_PATH}
    path = make_path(PROXY_BASE_PATH, "_list/block/pl", **encode_params(params))
    return proxy(request, path, plname=plname,
                headers=default_headers(PROXY_BASE_PATH, 
                                        settings.WEB_PROXY_INDEX))


def proxy(request, path, plname=None, headers=None):
    """ handle revproxy """
    headers = headers or {}
    for key, value in request.META.iteritems():
        if key.startswith('HTTP_'):
            key = header_name(key)
            
        elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            key = key.replace('_', '-')
            if not value: continue
        else:
            continue
        
        # rewrite location
        if key.lower() == "host":
            continue
        if is_hop_by_hop(key):
            continue
        else:
            headers[key] = value
    
    headers["X-Forwarded-For"] = request.META.get("REMOTE_ADDR")
    headers["X-Forwarded-Host"] = request.get_host()
    headers["PATH-INFO"] = request.get_full_path()
    if hasattr(request, 'user') and request.user.is_authenticated():
            headers.update({
                'X-AIMPL-User': request.user.username,
                'X-AIMPL-Priv': is_priv(request, plname),
                'X-AIMPL-User-PL': ','.join([p.name for p in privileges(request)]),
                'X-AIMPL-Groups': ','.join(str(g) \
                            for g in request.user.groups.all() \
                            if has_group(request, str(g), plname) \
                            or str(g) == "Chief Editor"),
                'X-AIMPL-Token': hmac.new(settings.SECRET_KEY, 
                            request.user.username, hashlib.sha1).hexdigest()
            })
    
    uri = "http://%s:%s%s" % (settings.WEB_PROXY_DOMAIN, 
                            settings.WEB_PROXY_PORT, path)
                            
   
    # Django's internal mechanism doesn't pick up
    # PUT request, so we trick it a little here.
    if request.method.upper() == "PUT":
        coerce_put_post(request)
    try:
        resp = connection.request(uri, method=request.method, 
                            body=request.raw_post_data,
                            headers=headers)
        body = resp.body_file
    except restkit.RequestFailed, e:
        msg = getattr(e, 'msg', '')
        
        if e.status_int >= 100:
            resp = e.response
            body = msg
        else:
            return http.HttpResponseBadRequest(msg)
             
    response = HttpResponse(body, status=resp.status_int)
    for k, v in resp.headers.items():
        if is_hop_by_hop(k):
            continue
        else:
            response[k] = v
    return response

def header_name(name):
    """Convert header name like HTTP_XXXX_XXX to Xxxx-Xxx:"""
    words = name[5:].split('_')
    for i in range(len(words)):
        words[i] = words[i][0].upper() + words[i][1:].lower()
        
    result = '-'.join(words)
    return result
