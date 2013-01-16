# Introduction

[Note: this code is still good, but the authors no longer actually use
it in production, so don't expect it to be updated.]

Twister is a simple microapp that makes the functionality of the
python [http://docs.python.org/lib/module-random.html](random library)
available over HTTP. Ie, you can make a GET request and get back
random numbers from a bunch of different statistical distributions.

The python random library uses a Mersenne Twister algorithm, hence the
name 'Twister'.

# HTTP API

(for the examples, we'll assume that Twister is running at
http://twister.example.com/)

The path part of the URL just specifies the distribution to use. The
available distributions are: beta, expo, gamma, gauss, lognormal,
pareto, uniform, vonmises, weibull, randint. They all map in fairly
obvious ways to the appropriate functions in the python library.

Each distribution has its own parameter or parameters that are
required. Eg, a uniform distribution needs a range specified like 0 -
1, while a weibull distribution needs alpha and beta parameters
specified. Read the docs for the python library for full details on
what the parameters mean and what the valid ranges are for
them. Twister doesn't really try to check that the supplied parameters
are there or within the appropriate ranges; it will just give you a
500 error if you give it bogus params. (the exception to this is the
`lambd` parameter for the expo distribution. In the python library
it's renamed like that because 'lambda' is a python keyword. Since
Twister is just HTTP, it uses the regular 'lambda' as the name of the
parameter).

So, eg, to get a random number in the range 0 to 1 with a uniform
distribution, you would do:

    GET /uniform?a=0;b=1

for normal (aka gaussian) distribution, which uses mu and sigma
parameters, a request would be like:

    GET /gauss?mu=1;sigma=2


There are also two global parameters that will be used with any kind
of distribution: seed, and n.

`n` is the number of values you want returned from that
distribution. This is useful if you know you're going to need a bunch
of random numbers from the same distribution; you can just request
them all at once like:

    GET /gauss?mu=1;sigma=2;n=10000

specifying a seed will let you seed the pseudorandom generator so you
can duplicate results. (note that seed is always treated as a string
even if it looks like a number. This is different from directly
accessing the python library where it will take any hashable object
and 123456 hashes differently from "123456". Twister would always
treat it as "12345")

    GET /gauss?mu=1;sigma=2;n=1000;seed=12345

will always return the same set of values each time it is requested.

The response is always a JSON object with the following attributes:

* seed (the seed used to generate the numbers. either the one
  specified as a parameter, or the random one that Twister
  generates. this is so you can always repeat a query even if you
  forgot to specify a seed on the first request)
* n (that you specified. defaults to 1)
* params (a dict of the additional params specified)
* values (a list of the number(s) generated)

Eg,

    $ curl 'http://twister.example.com/weibull?alpha=1;beta=30;n=10'
    {"values": [0.947198604486, 0.957787242769, 0.998331849861, 0.982809154613, 1.02004182685, 0.979367559154, 1.03786998886, 0.975261400968, 0.933165900789, 1.0122563764], "seed": "0.950636881446", "params": {"alpha": "1", "beta": "30"}, "n": 10}


Twister also generates etag headers on all its responses and will
respond properly to conditional requests if an etag and seed are
specified. That can save it from having to regenerate a large number
of numbers in some cases.

There is also now a TwisterClient python client interface that hides
as much of that as possible.

# Installation

Twister is a Paste + WSGI app, which should make it fairly
straightforward to deploy however you want. The tarballs for all the
libraries that it uses are also included with it. The easiest way to
run it is to check it out of git, run `./bootstrap.py`, which will
install all of the included libraries into a virtualenv, copy one of
the `.ini` files to `local.ini`, edit it to your requirements, run

    python setup.py develop 

and then

    ./start.sh . local.ini

which is just a simple script that runs `paster serve local.ini` with
the right virtualenv.
