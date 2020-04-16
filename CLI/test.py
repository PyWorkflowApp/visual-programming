from django.test import TestCase

from pyworkflow.pyworkflow import Workflow


class WorkflowTest(TestCase):

    def set_up(self):
        self.workflow = Workflow()

    def test_workflow_init(self):
        self.assertEqual(self.workflow.name, "a-name")

if __name__ == '__main__':
    unittest.main()