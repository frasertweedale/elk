import unittest

from . import elk


class A(object):
    __metaclass__ = elk.ElkMeta
    x = elk.ElkAttribute(default=10)
    y = elk.ElkAttribute(default=None)
    z = elk.ElkAttribute()


class DefaultTestCase(unittest.TestCase):
    def test_without_arg(self):
        """Test default value when no init arg provided."""
        a = A()
        self.assertEqual(a.x, 10)

    def test_with_arg(self):
        """Test that init arg preferred to default."""
        a = A(x=20)
        self.assertEqual(a.x, 20)

    def test_default_is_none(self):
        """Test that a default of ``None`` sets the value."""
        a = A()
        self.assertIsNone(a.y)

    def test_no_default(self):
        """Test that no specified default does not set the attribute."""
        a = A()
        with self.assertRaises(AttributeError):
            a.z

    def test_callable_default(self):
        """Callable default is called to generate default."""
        class B(object):
            __metaclass__ = elk.ElkMeta
            x = elk.ElkAttribute(default=lambda: [])

        b1 = B()
        b2 = B()
        self.assertEqual(b1.x, [])
        self.assertEqual(b2.x, [])
        self.assertIsNot(b1.x, b2.x)

    def test_callable_default_expects_args(self):
        """Callable default that expects args raises TypeError."""
        with self.assertRaises(TypeError):
            class B(object):
                __metaclass__ = elk.ElkMeta
                x = elk.ElkAttribute(default=lambda x: [])

    def test_nonhashable_default(self):
        """Nonhashable default raises TypeError."""
        with self.assertRaises(TypeError):
            class B(object):
                __metaclass__ = elk.ElkMeta
                x = elk.ElkAttribute(default=[])
