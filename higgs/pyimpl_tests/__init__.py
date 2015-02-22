import types
import unittest
from higgs.pyimpl import GlobalScope


class ModuleLoadingTest(unittest.TestCase):
    def test_module_looks_properly_initialized(self):
        """On import, the 'interface' and 'impl' members of a module
        are created
        """
        gs = GlobalScope()

        module = gs.higgs_import('WeirdModule')
        self.assertTrue(hasattr(module, 'interface'))
        self.assertTrue(hasattr(module, 'impl'))

    def test_module_simple_interface_members_are_initialized(self):
        """Assignment, in the module inline code, has an effect on the module
        interface and possibly impl

        Needs attention, because things will change. The types of the objects
        will change to the proper higgs types.
        """
        gs = GlobalScope()

        module = gs.higgs_import('WeirdModule')

        self.assertIn('a', module.interface)
        self.assertIn('increment', module.interface)
        self.assertIn('weird_name', module.interface)

        self.assertTrue(module.interface['a'] is int)
        self.assertTrue(
            issubclass(module.interface['increment'], types.FunctionType))
        self.assertTrue(issubclass(module.interface['weird_name'], str))

    def test_module_simple_impl_members_are_initialized(self):
        """Tests that the correct impls are assigned to the module
        members

        Needs attention. The actual values will change, and be replaced with
        proper Higgs types (which will have their own interface member, which
        can only be a super set of the module member's interface)
        """
        gs = GlobalScope()

        module = gs.higgs_import('WeirdModule')

        self.assertIn('a', module.impl)
        self.assertIn('increment', module.impl)

        self.assertNotIn('weird_name', module.impl)

        self.assertEqual(module.impl['a'], 3)
        self.assertTrue(
            isinstance(module.impl['increment'], types.FunctionType))

    def test_member_and_actual_object_interface_are_alike(self):
        """Duck typing: test it!

        Needs attention: at the moment, the gs.satisfies returns a Python
        bool. This will be changed to the HiggsBool

        We wouldn't want to copy methods on all the objects, because the
        sheer number of pointers would go up a lot.... simple as that

        We'd like to refer to the type object for all our properties,
        just because it's more memory efficient, and then override anything
        in the object's dict that we need to customize.

        Why in Python, you can't assign methods to an object, only to a class:
            because determining the scope of the self reference is tricky.
            -In Python you can bind the 'self' with functools.partial
            -In JS there's always a 'this', but it's bound at run time, and
             there's a way to bind it with the .bind() method of functions
            -In Java you don't have this problem, because classes aren't
            objects, and you can't assign methods, or move them around in any
            way (unless with reflection?)
        """
        gs = GlobalScope()

        module = gs.higgs_import('WeirdModule')

        # for name in 'a', 'increment', 'weird_name':
            # self.assertTrue(gs.satisfies(module.impl) is )
