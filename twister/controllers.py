import selector
import cgi
import random, simplejson
from md5 import md5


def render_json(start_response, struct, headers=None,etag=None):
    if headers is None:
        headers = []
    body = simplejson.dumps(struct)
    start_response("200 OK", [('Content-Type', 'application/json'),
                              ('etag',etag)])
    return [body]

def get_param(environ,key,default=None):
    """ cgi fieldstorage is broken. it pretends to be a dict but doesn't implement
    a get() method. and the thing it returns isn't really a value. :(

    also, cgi by default doesn't work with ';' parameter seperators in the
    query string, which is really annoying. So we fix that here with a
    nasty little hack.

    """

    # this may not work in other applications.
    # in twister, the query string is simple enough
    # that we can get away with it
    environ['QUERY_STRING'].replace(';','&') 
    
    fs = cgi.FieldStorage(environ=environ)
    try:
        return fs[key].value
    except:
        return default

# distribution functions
# each is just a simple wrapper for the function in random
# it just accepts an extra **params dict so we don't
# have to be as careful about stripping out extra params
# before calling

def beta(alpha=None,beta=None,**params):
    # alpha > 0, beta > 0
    return random.betavariate(float(alpha),float(beta))

def expo(lambd=None,**params):
    return random.expovariate(float(lambd))

def gamma(alpha=None,beta=None,**params):
    # alpha > 0, beta > 0
    return random.gammavariate(float(alpha),float(beta))

def gauss(mu=None,sigma=None,**params):
    return random.gauss(float(mu),float(sigma))

def lognormal(mu=None,sigma=None,**params):
    return random.lognormvariate(float(mu),float(sigma))

def pareto(alpha=None,**params):
    return random.paretovariate(float(alpha))

def uniform(a=None,b=None,**params):
    return random.uniform(float(a),float(b))

def randint(a=None,b=None,**params):
    return random.randint(int(a),int(b))

def vonmises(mu=None,kappa=None,**params):
    # 0 <= mu <= 2*pi
    # kappa >= 0
    return random.vonmisesvariate(float(mu),float(kappa))

def weibull(alpha=None,beta=None,**params):
    return random.weibullvariate(float(alpha),float(beta))

def error_message(start_response,message=""):
    start_response("500 Server Error",[("Content-Type","text/plain")])
    return [message]

class Root:
    def __call__(self, environ, start_response):
        # seed the random number generator
        # for consistency and ease of dealing with HTTP,
        # the seed will always be a string
        seed = get_param(environ,'seed',None)

        # first, handle conditional requests and generate an etag
        # from the request. etags only make sense though if there is
        # a seed (otherwise, we expect it to return different results
        # for the same params)
        request = str(environ['QUERY_STRING']) + str(environ['selector.vars'])
        etag = '"%s"' % md5(request).hexdigest()
        if seed is not None and etag == environ.get('HTTP_IF_NONE_MATCH', ''):
            start_response('304 Not Modified', [])
            return []
        
        if seed is None:
            seed = str(random.random())
        random.seed(str(seed))

        # collect all the parameters that we might need
        n = int(get_param(environ,'n',1))

        params = dict()
        for p in ['alpha','beta','lambda','mu','sigma','kappa','a','b']:
            params[p] = get_param(environ,p)

        # since lambda is a keyword in python, we have to
        # change it a bit so we can use it as a function
        # argument later with **params
        params['lambd'] = params['lambda']
        del params['lambda']

        distros = dict(beta=beta,expo=expo,gamma=gamma,gauss=gauss,
                       lognormal=lognormal,pareto=pareto,
                       uniform=uniform,vonmises=vonmises,
                       weibull=weibull,randint=randint)
        
        distribution = environ['selector.vars'].get('distribution','uniform')

        if distribution not in distros:
            return error_message("unknown distribution type")

        f = distros[distribution]

        values = [f(**params) for i in xrange(n)]


        # clean up params dict for spitting it back
        # first we munge lambda back into the params dict
        # so no one has to know about python's internal stuff
        params['lambda'] = params['lambd']
        del params['lambd']
        
        # then remove unused params
        nparams = dict()
        for (key,value) in params.iteritems():
            if value is not None:
                nparams[key] = value

        # get a next_seed so clients can chain requests
        next_seed = str(random.random())
        return render_json(start_response,
                           dict(seed=seed, n=n, params=nparams, values=values,
                                next_seed=next_seed),
                           etag=etag)
        
urls = selector.Selector()
urls.add('/[{distribution}]', _ANY_=Root())


