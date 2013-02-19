import re

FLAGS = {
    'ignorecase': re.I,
    'locale': re.L,
    'multiline': re.M,
    'dotall': re.S,
    'unicode': re.U,
    'verbose': re.X,
}


class TyrannosaurusRegex(object):

    def __init__(self, pattern, **kwargs):

        self.pattern = pattern
        self.flags = set()

        for k, v in kwargs.items():
            self._flag(k, v)

        self.compile()

    #
    # these are scary, don't use these
    #

    def __eq__(self, other):
        return self.matches(other)

    def __ne__(self, other):
        return not self.matches(other)

    def __contains__(self, item):
        return self._re.search(item) is not None

    # override get/set attr for flags

    def __getattr__(self, name):
        if name in FLAGS:
            return FLAGS[name] in self.flags
        return self.__dict__[name]

    def __setattr__(self, name, value):
        if name in FLAGS:
            self._flag(name, value)
            self.compile()
        else:
            self.__dict__[name] = value

    # do matching in call

    def __call__(self, s):
        for m in self._re.finditer(s):
            yield Matchtodon(m)

    def _flag(self, flag, enabled):

        if flag not in FLAGS:
            raise ValueError("%s is not a valid flag" % flag)

        if enabled:
            self.flags.add(FLAGS[flag])
        else:
            self.flags.discard(FLAGS[flag])

    def compile(self, pattern=None):

        if pattern:
            self.pattern = pattern

        flags = reduce(lambda x, y: x | y, self.flags, 0)

        self._re = re.compile(self.pattern, flags)

    def matches(self, s):
        m = self._re.match(s)
        return m is not None


class Matchtodon(list):

    def __init__(self, match):
        super(Matchtodon, self).__init__(match.groups())
        self.match = match

    def __getitem__(self, name):
        return self.named.get(name)

    @property
    def named(self):
        return self.match.groupdict()


def rgx(pattern, **kwargs):
    return TyrannosaurusRegex(pattern, **kwargs)


if __name__ == "__main__":

    r = rgx(r"([a-z]{3})")
    for m in r("abc def GHi jlkm opqr stuvw xYz"):
        print m

    zipcode = "55555"
    print rgx("\d{5}$").matches(zipcode)
    print zipcode == rgx("\d{5}$")
