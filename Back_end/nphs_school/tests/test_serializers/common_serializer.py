from rest_framework.test import APITestCase

class BaseSerializerTestCase(APITestCase):
    """
    Common tests for ModelSerializer classes.
    Child test classes should provide:
    serializer_class
    model
    instance

    """

serializer_class = None
model = None
instance = None

def test_serializer_exists(self):
    self.assertIsNotNone(self.serializer_class)

def test_serializer_has_data(self):
    serializer = self.serializer_class(self.instance)

    self.assertIsNotNone(serializer.data)

def test_serializer_contains_expected_model_fields(self):
    serializer = self.serializer_class(self.instance)

    for field in self.expected_fields:
        self.assertIn(field, serializer.fields)

