from django.test import TestCase
from models.step import Step

class StepModelTest(TestCase):

    def test_create_step(self):
        step = Step.objects.create(
            order=1,
            description="Pelar las patatas"
        )

        self.assertEqual(step.order, 1)
        self.assertEqual(step.description, "Pelar las patatas")
        self.assertIsNotNone(step.created_at)
        self.assertIsNotNone(step.updated_at)
