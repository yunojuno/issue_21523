"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import mock
import datetime
from django.test import TestCase
from example.models import ModelWithDateField
from example.utils import Today, FakeDate


class DateFieldTests(TestCase):
    """Test the behaviour of a DateField when mocking out today()."""

    def test_default_value(self):
        """Confirm that the field is unset by default (pre-save)."""
        model = ModelWithDateField()
        self.assertIsNone(model.test_field)

    def test_save_without_mock(self):
        """Confirm that saving the model sets the test_field value to today."""
        model = ModelWithDateField()
        model.save()
        self.assertIsNotNone(model.test_field)
        self.assertIsInstance(model.test_field, datetime.date)
        self.assertEqual(model.test_field, datetime.date.today())


class MethodDecoratorTests(TestCase):
    """Test mocking at a method level using decorators."""

    @Today(1999, 12, 31)
    def test_today_decorator(self):
        """Mock out today() using the Today decorator."""
        model = ModelWithDateField()
        with self.assertRaises(TypeError):
            model.save()

    @mock.patch('datetime.date', FakeDate)
    def test_mock_fakedate(self):
        """Mock out datetime.date using FakeDate and mock.patch decorator."""
        FakeDate.today = classmethod(lambda cls: datetime.date(2000, 1, 1))
        model = ModelWithDateField()
        model.save()
        self.assertIsNotNone(model.test_field)
        self.assertIsInstance(model.test_field, datetime.date)
        self.assertEqual(model.test_field.year, 2000)
        self.assertEqual(model.test_field.month, 1)
        self.assertEqual(model.test_field.day, 1)


@mock.patch('datetime.date', FakeDate)
class ClassDecoratorTests(TestCase):
    """Test with datetime.date mocked out at a class level."""

    def test_save_with_mock(self):
        """Confirm that using mock #2 causes a TypeError."""
        model = ModelWithDateField()
        model.save()
        self.assertIsNotNone(model.test_field)
        self.assertIsInstance(model.test_field, datetime.date)
        self.assertEqual(model.test_field.year, 2000)
        self.assertEqual(model.test_field.month, 1)
        self.assertEqual(model.test_field.day, 1)

    def test_save_with_mock_2(self):
        """Confirm that value returned from FakeDate.today() can be set."""
        FakeDate.today = classmethod(lambda cls: datetime.date(1999, 12, 31))
        model = ModelWithDateField()
        model.save()
        self.assertIsNotNone(model.test_field)
        self.assertIsInstance(model.test_field, datetime.date)
        self.assertEqual(model.test_field.year, 1999)
        self.assertEqual(model.test_field.month, 12)
        self.assertEqual(model.test_field.day, 31)
