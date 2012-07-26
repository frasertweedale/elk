import unittest

from . import elk


class A(object):
    __metaclass__ = elk.ElkMeta
    default = elk.ElkAttribute()
    nonereq = elk.ElkAttribute(required=None)
    nonreq = elk.ElkAttribute(required=False)
    req = elk.ElkAttribute(required=True)
    req_default = elk.ElkAttribute(required=True, default=10)


class RequiredTestCase(unittest.TestCase):
    def test_required_default(self):
        """Attribute not required by default, None or False."""
        a = A(req='value')

    def test_required_true(self):
        """Items explicitly required are required."""
        with self.assertRaises(AttributeError):
            a = A()
        a = A(req='value')
        self.assertEqual(a.req, 'value')

    def test_required_true_default(self):
        """Default value satisfies requirement."""
        a = A(req='value')
        self.assertEqual(a.req_default, 10)

    def test_required_true_default_overridable(self):
        """Default of required attribute is override by init arg."""
        a = A(req='value', req_default='othervalue')
        self.assertEqual(a.req_default, 'othervalue')

    def test_can_del_non_required_attr(self):
        a = A(req='value', nonreq='othervalue')
        self.assertEqual(a.nonreq, 'othervalue')
        del a.nonreq
        with self.assertRaises(AttributeError):
            a.nonreq

    def test_cannot_del_required_attr(self):
        """Cannot delete required attribute."""
        a = A(req='value')
        with self.assertRaises(AttributeError):
            del a.req
        with self.assertRaises(AttributeError):
            del a.req_default
