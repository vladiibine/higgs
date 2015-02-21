import types
from unittest import TestCase
from higgs.pyimpl import GlobalScope


class ModuleLoadingTest(TestCase):
    def test_module_looks_properly_initialized(self):
        gs = GlobalScope()

        module = gs.higgs_import('WeirdModule')
        self.assertTrue(hasattr(module, 'interface'))
        self.assertTrue(hasattr(module, 'implementation'))

    def test_module_simple_interface_members_are_initialized(self):
        gs = GlobalScope()

        module = gs.higgs_import('WeirdModule')

        self.assertIn('a', module.interface)
        self.assertIn('increment', module.interface)
        self.assertIn('weird_name', module.interface)

        self.assertTrue(module.interface['a'] is int)
        self.assertTrue(
            issubclass(module.interface['increment'], types.FunctionType))
        self.assertTrue(issubclass(module.interface['weird_name'], str))

    def test_module_simple_implementation_members_are_initialized(self):
        gs = GlobalScope()

        module = gs.higgs_import('WeirdModule')

        self.assertIn('a', module.implementation)
        self.assertIn('increment', module.implementation)
        self.assertNotIn('weird_name', module.implementation)

        self.assertEqual(module.implementation['a'], 3)
        self.assertTrue(
            isinstance(module.implementation['increment'], types.FunctionType))

    def test_on_member_access_the_member_is_initialized(self):
        gs = GlobalScope()

        # math = gs.higgs_import()
