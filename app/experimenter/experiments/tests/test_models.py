from django.core.exceptions import ValidationError
from django.test import TestCase

from experimenter.experiments.models import ExperimentVariant
from experimenter.experiments.tests.factories import ExperimentFactory


class TestExperimentModel(TestCase):

    def test_control_property_returns_experiment_control(self):
        experiment = ExperimentFactory.create_with_variants()
        control = ExperimentVariant.objects.get(
            experiment=experiment, is_control=True)
        self.assertEqual(experiment.control, control)

    def test_variant_property_returns_experiment_variant(self):
        experiment = ExperimentFactory.create_with_variants()
        variant = ExperimentVariant.objects.get(
            experiment=experiment, is_control=False)
        self.assertEqual(experiment.variant, variant)

    def test_setting_status_from_not_started_to_started_sets_start_date(self):
        experiment = ExperimentFactory.create()
        self.assertEqual(experiment.status, experiment.EXPERIMENT_NOT_STARTED)
        self.assertEqual(experiment.is_complete, False)
        self.assertIsNotNone(experiment.created_date)
        self.assertIsNone(experiment.start_date)
        self.assertIsNone(experiment.end_date)

        experiment.status = experiment.EXPERIMENT_STARTED
        experiment.save()

        self.assertEqual(experiment.status, experiment.EXPERIMENT_STARTED)
        self.assertEqual(experiment.is_complete, False)
        self.assertIsNotNone(experiment.created_date)
        self.assertIsNotNone(experiment.start_date)
        self.assertIsNone(experiment.end_date)

    def test_setting_status_from_started_to_complete_sets_end_date(self):
        experiment = ExperimentFactory.create()
        experiment.status = experiment.EXPERIMENT_STARTED
        experiment.save()

        self.assertEqual(experiment.status, experiment.EXPERIMENT_STARTED)
        self.assertIsNotNone(experiment.created_date)
        self.assertIsNotNone(experiment.start_date)
        self.assertIsNone(experiment.end_date)

        experiment.status = experiment.EXPERIMENT_COMPLETE
        experiment.save()

        self.assertEqual(experiment.status, experiment.EXPERIMENT_COMPLETE)
        self.assertEqual(experiment.is_complete, True)
        self.assertIsNotNone(experiment.created_date)
        self.assertIsNotNone(experiment.start_date)
        self.assertIsNotNone(experiment.end_date)

    def test_setting_from_started_to_not_started_raises_validation_error(self):
        experiment = ExperimentFactory.create()
        experiment.status = experiment.EXPERIMENT_STARTED
        experiment.save()

        with self.assertRaises(ValidationError):
            experiment.status = experiment.EXPERIMENT_NOT_STARTED
            experiment.save()
