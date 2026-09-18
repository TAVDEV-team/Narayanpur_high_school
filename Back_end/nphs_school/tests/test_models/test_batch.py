from django.test import TestCase

from nphs_school.models import AClass, Batch


class BatchModelTest(TestCase):

    def test_create_batch(self):
        batch = Batch.objects.create(
            graduation_year="2027"
        )

        self.assertIsNotNone(batch.pk)
        self.assertEqual(batch.graduation_year, "2027")
        self.assertFalse(batch.is_graduated)

    def test_label_is_generated_automatically(self):
        batch = Batch.objects.create(
            graduation_year="2027"
        )

        self.assertEqual(batch.label, "SSC-2027")

    def test_label_updates_when_graduation_year_changes(self):
        batch = Batch.objects.create(
            graduation_year="2027"
        )

        self.assertEqual(batch.label, "SSC-2027")

        batch.graduation_year = "2028"
        batch.save()

        batch.refresh_from_db()

        self.assertEqual(batch.label, "SSC-2028")

    def test_label_is_not_manually_used(self):
        batch = Batch(
            label="MY-CUSTOM-BATCH",
            graduation_year="2027",
        )

        batch.save()

        self.assertEqual(batch.label, "SSC-2027")

    def test_default_is_graduated_is_false(self):
        batch = Batch.objects.create(
            graduation_year="2027"
        )

        self.assertFalse(batch.is_graduated)

    def test_active_batches_returns_non_graduated_batches(self):
        active_batch_1 = Batch.objects.create(
            graduation_year="2027",
            is_graduated=False,
        )

        active_batch_2 = Batch.objects.create(
            graduation_year="2028",
            is_graduated=False,
        )

        Batch.objects.create(
            graduation_year="2025",
            is_graduated=True,
        )

        active_batches = Batch.active_batches()

        self.assertEqual(active_batches.count(), 2)
        self.assertIn(active_batch_1, active_batches)
        self.assertIn(active_batch_2, active_batches)

    def test_archived_batches_returns_graduated_batches(self):
        Batch.objects.create(
            graduation_year="2027",
            is_graduated=False,
        )

        archived_batch_1 = Batch.objects.create(
            graduation_year="2024",
            is_graduated=True,
        )

        archived_batch_2 = Batch.objects.create(
            graduation_year="2025",
            is_graduated=True,
        )

        archived_batches = Batch.archived_batches()

        self.assertEqual(archived_batches.count(), 2)
        self.assertIn(archived_batch_1, archived_batches)
        self.assertIn(archived_batch_2, archived_batches)

    def test_active_batches_does_not_include_archived_batches(self):
        active_batch = Batch.objects.create(
            graduation_year="2027",
            is_graduated=False,
        )

        archived_batch = Batch.objects.create(
            graduation_year="2025",
            is_graduated=True,
        )

        active_batches = Batch.active_batches()

        self.assertIn(active_batch, active_batches)
        self.assertNotIn(archived_batch, active_batches)

    def test_archived_batches_does_not_include_active_batches(self):
        active_batch = Batch.objects.create(
            graduation_year="2027",
            is_graduated=False,
        )

        archived_batch = Batch.objects.create(
            graduation_year="2025",
            is_graduated=True,
        )

        archived_batches = Batch.archived_batches()

        self.assertIn(archived_batch, archived_batches)
        self.assertNotIn(active_batch, archived_batches)

    def test_current_class_returns_related_class(self):
        batch = Batch.objects.create(
            graduation_year="2027"
        )

        academic_class = AClass.objects.create(
            name="9_science",
            batch=batch,
            room_number="201",
            grade=9,
            group="science",
        )

        self.assertEqual(batch.current_class, academic_class)

    def test_current_class_returns_none_when_no_class_exists(self):
        batch = Batch.objects.create(
            graduation_year="2027"
        )

        self.assertIsNone(batch.current_class)

    def test_current_class_returns_first_class_when_multiple_exist(self):
        batch = Batch.objects.create(
            graduation_year="2027"
        )

        first_class = AClass.objects.create(
            name="9_science",
            batch=batch,
            room_number="201",
            grade=9,
            group="science",
        )

        AClass.objects.create(
            name="10_science",
            batch=batch,
            room_number="202",
            grade=10,
            group="science",
        )

        self.assertEqual(batch.current_class, first_class)

    def test_str_returns_label(self):
        batch = Batch.objects.create(
            graduation_year="2027"
        )

        self.assertEqual(str(batch), "SSC-2027")

    def test_created_at_and_updated_at_are_set(self):
        batch = Batch.objects.create(
            graduation_year="2027"
        )

        self.assertIsNotNone(batch.created_at)
        self.assertIsNotNone(batch.updated_at)