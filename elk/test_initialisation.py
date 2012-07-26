import unittest

from . import elk


class A(object):
    __metaclass__ = elk.ElkMeta
    x = elk.ElkAttribute()
    y = elk.ElkAttribute(init_arg='init_y')
    z = elk.ElkAttribute(init_arg=None)


class InitialisationTestCase(unittest.TestCase):
    def test_no_arg(self):
        """Test that no argument result in AttributeError."""
        with self.assertRaises(AttributeError):
            a = A()
            a.x

    def test_arg_none(self):
        """Test that arg of None sets value to None."""
        a = A(x=None)
        self.assertIsNone(a.x)

    def test_arg_not_none(self):
        """Test that arg of regular value has value set."""
        a = A(x=10)
        self.assertEqual(a.x, 10)

    def test_init_arg(self):
        """``init_arg`` parameter overrides init argument."""
        a = A(init_y=20)
        self.assertEqual(a.y, 20)

    def test_init_arg_non_str(self):
        """Non-str ``init_arg`` value raises TypeError."""
        with self.assertRaises(TypeError):
            class B(object):
                __metaclass__ = elk.ElkMeta
                x = elk.ElkAttribute(init_arg=10)

    def test_init_arg_none(self):
        """``None`` init_arg is same as not supplying."""
        a = A(z='zed')
        self.assertEqual(a.z, 'zed')


class OverrideChecker(object):
    __metaclass__ = elk.ElkMeta
    default = elk.ElkAttribute(default=10)
    builder = elk.ElkAttribute(builder='_build')
    default_and_builder = elk.ElkAttribute(default=10, builder='_build')

    def _build(self):
        return 'buttercup'


class InitialisationOrderTestCase(unittest.TestCase):
    """Test that attributes are initialised in correct order.

    Attributes whose values are supplied to the constructor are
    initialised first, followed by non-lazy attributes with default
    and finally non-lazy attributes with builders.  Within each
    of these groups the order is undefined and must not be relied
    upon.
    """

    def test_value_before_builder(self):
        class B(object):
            __metaclass__ = elk.ElkMeta
            value = elk.ElkAttribute()
            builder = elk.ElkAttribute(builder='_build')

            def _build(self):
                return self.value + 1

        with self.assertRaises(AttributeError):
            b = B()
        b = B(value=10)
        self.assertEqual(b.builder, 11)

    def test_default_before_builder(self):
        class B(object):
            __metaclass__ = elk.ElkMeta
            default = elk.ElkAttribute(default=10)
            builder = elk.ElkAttribute(builder='_build')

            def _build(self):
                return self.default + 1

        b = B()
        self.assertEqual(b.builder, 11)

    def test_value_overrides_default(self):
        obj = OverrideChecker(default='override')
        self.assertEqual(obj.default, 'override')

    def test_value_overrides_builder(self):
        obj = OverrideChecker(builder='override')
        self.assertEqual(obj.builder, 'override')

    def test_default_overrides_builder(self):
        obj = OverrideChecker(default_and_builder='override')
        self.assertEqual(obj.default_and_builder, 'override')
