# -*- coding: utf-8 -
# Copyright (c) 2009 Benoit Chesneau <benoitc@e-engura.com> 
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


import os
import re
import urllib
try:
    import simplejson as json
except ImportError:
    import json
    

try:#python 2.6, use subprocess
    import subprocess
    subprocess.Popen  # trigger ImportError early
    closefds = os.name == 'posix'
    
    def popen3(cmd, mode='t', bufsize=0):
        p = subprocess.Popen(cmd, shell=True, bufsize=bufsize,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
            close_fds=closefds)
        p.wait()
        return (p.stdin, p.stdout, p.stderr)
except ImportError:
    subprocess = None
    popen3 = os.popen3


def coerce_put_post(request):
    """
    Django doesn't particularly understand REST.
    In case we send data over PUT, Django won't
    actually look at the data and load it. We need
    to twist its arm here.
    
    The try/except abominiation here is due to a bug
    in mod_python. This should fix it.
    
    Function from django-piston project.
    """
    if request.method == "PUT":
        try:
            request.method = "POST"
            request._load_post_and_files()
            request.method = "PUT"
        except AttributeError:
            request.META['REQUEST_METHOD'] = 'POST'
            request._load_post_and_files()
            request.META['REQUEST_METHOD'] = 'PUT'
            
        request.PUT = request.POST


def encode_params(params):
    """ encode parameters in json if needed """
    _params = {}
    if params:
        for name, value in params.items():
            if name in ('key', 'startkey', 'endkey') \
                    or not isinstance(value, basestring):
                value = json.dumps(value)
            _params[name] = value
    return _params
    
def make_path(base, *path, **query):
    base_trailing_slash = False
    if base and base.endswith("/"):
        base_trailing_slash = True
        base = base[:-1]
    retval = [base]

    # build the path
    _path = []
    trailing_slash = False       
    for s in path:
        if s is not None and isinstance(s, basestring):
            if len(s) > 1 and s.endswith('/'):
                trailing_slash = True
            else:
                trailing_slash = False
            _path.append(url_quote(s.strip('/'), safe=":/%"))
                   
    path_str =""
    if _path:
        path_str = "/".join([''] + _path)
        if trailing_slash:
            path_str = path_str + "/" 
    elif base_trailing_slash:
        path_str = path_str + "/" 
        
    if path_str:
        retval.append(path_str)

    params = []
    for k, v in query.items():
        if type(v) in (list, tuple):
            params.extend([(k, i) for i in v if i is not None])
        elif v is not None:
            params.append((k,v))
    if params:
        retval.extend(['?', url_encode(dict(params), True)])

    return ''.join(retval)
    

def url_quote(s, charset='utf-8', safe='/:'):
    """URL encode a single string with a given encoding."""
    if isinstance(s, unicode):
        s = s.encode(charset)
    elif not isinstance(s, str):
        s = str(s)
    return urllib.quote(s, safe=safe)

def url_encode(obj, charset="utf8", encode_keys=False):
    if isinstance(obj, dict):
        items = []
        for k, v in obj.iteritems():
            if not isinstance(v, (tuple, list)):
                v = [v]
            items.append((k, v))
    else:
        items = obj or ()

    tmp = []
    for key, values in items:
        if encode_keys and isinstance(key, unicode):
            key = key.encode(charset)
        else:
            key = str(key)

        for value in values:
            if value is None:
                continue
            elif isinstance(value, unicode):
                value = value.encode(charset)
            else:
                value = str(value)
        tmp.append('%s=%s' % (urllib.quote(key),
            urllib.quote_plus(value)))

    return '&'.join(tmp)