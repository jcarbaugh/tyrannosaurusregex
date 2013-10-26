tyrannosaurusregex
==================

Just playing around with some regular expression ideas. Other ideas or suggestions are welcome.

The goal is to make it easy to do simple regex stuff. Not that it's incredibly HARD right now, but it could be easier, right?
::

    >>> from trex import rex
    >>> r = rex(r"([a-z]{3})")
    >>> for m in r("abc def GHi jlkm opqr stuvw xYz"):
    >>>    print m
    ['abc']
    ['def']
    ['jlk']
    ['opq']
    ['stu']

Or...
::

    >>> from trex import rex
    >>> zipcode = "55555"
    >>> rex("\d{5}$").matches(zipcode)
    True


Usage
-----

Create your TyrannosaurusRegex object by calling `rex` with your pattern.
::

    >>> from trex import rex
    >>> r = rex(r"(?P<threeletters>[a-z]{3})")


You can pass flags as arguments to `rex` or set them on the returned TyrannosaurusRegex object.
::

    >>> r = rex(r"(?P<threeletters>[a-z]{3})", ignorecase=True)
    >>> r.ignorecase = False


To find matches, the TyrannosaurusRegex object can be called with the text that is to be searched.
::

    >>> text = "abc def GHi jlkm opqr stuvw xYz"
    >>> g = r(text)
    >>> matches = list(g)

Calling the TyrannosaurusRegex object returns a generator that emits Matchtodon objects. A Matchtodon is a list of the matched groups.
::

    >>> print matches
    [['abc'], ['def'], ['jlk'], ['opq'], ['stu']]


A Matchtodon also provides dict-like access to named groups.
::

    >>> print matches[0]['threeletters']
    abc

Changing a flag will force recompilation of the pattern.
::

    >>> print list(r(text))
    [['abc'], ['def'], ['jlk'], ['opq'], ['stu']]
    >>> r.ignorecase = True
    >>> print list(r(text))
    [['abc'], ['def'], ['GHi'], ['jlk'], ['opq'], ['stu'], ['xYz']]


Don't do this
-------------

I'm not actually proposing this, unless you think it's a good idea... in which case I take full credit for it.

Equality acts like re.match. The objects are equal if zero or more characters at the beginning of the string match the pattern.
::

    >>> print "ABC" == rex("[a-z]{3}")
    False
    >>> print "abcdef" == rex("[a-z]{3}")
    True
    >>> print "abcdef" == rex("[a-z]{3}$")
    False


The *in* operator acts like re.search. It evaluates to True if the pattern is found anywhere in the string. I'd love to be able to reverse the operands, but oh well.
::

    >>> print "235 wgg ADGKJE" in rex("[a-z]{3}")
    True
