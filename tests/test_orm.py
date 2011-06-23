# -*- coding: utf-8 -*-

from . import BaseTest

from sentry.db import models

class TestModel(models.Model):
    str_ = models.String()
    int_ = models.Integer()
    float_ = models.Float()
    list_ = models.List()
    
    class Meta:
        sortables = ('int_', 'float_')
        indexes = (('str_',),)


class ORMTest(BaseTest):
    def test_create(self):
        inst = TestModel.objects.create(
            str_='foo',
            int_=0,
            float_=0.1,
            list_=[1, 2, 3],
        )
        self.assertEquals(TestModel.objects.count(), 1)
        self.assertTrue(inst.pk)
        self.assertEquals(inst.str_, 'foo')
        self.assertEquals(inst.int_, 0)
        self.assertEquals(inst.float_, 0.1)
        self.assertEquals(len(inst.list_), 3)
        self.assertTrue(1 in inst.list_)
        self.assertTrue(2 in inst.list_)
        self.assertTrue(3 in inst.list_)

    def test_get_or_create(self):
        inst, created = TestModel.objects.get_or_create(str_='foo', defaults={
            'int_': 0,
            'float_': 0.1,
            'list_': [1, 2, 3],
        })
        self.assertTrue(created)
        self.assertEquals(TestModel.objects.count(), 1)
        self.assertTrue(inst.pk)
        self.assertEquals(inst.str_, 'foo')
        self.assertEquals(inst.int_, 0)
        self.assertEquals(inst.float_, 0.1)
        self.assertEquals(len(inst.list_), 3)
        self.assertTrue(1 in inst.list_)
        self.assertTrue(2 in inst.list_)
        self.assertTrue(3 in inst.list_)

        inst, created = TestModel.objects.get_or_create(str_='foo', defaults={
            'int_': 1,
            'float_': 1.1,
            'list_': [1],
        })
        self.assertFalse(created)
        self.assertEquals(TestModel.objects.count(), 1)
        self.assertTrue(inst.pk)
        self.assertEquals(inst.str_, 'foo')
        self.assertEquals(inst.int_, 0)
        self.assertEquals(inst.float_, 0.1)
        self.assertTrue(len(inst.list_), 3)
        self.assertTrue(1 in inst.list_)
        self.assertTrue(2 in inst.list_)
        self.assertTrue(3 in inst.list_)

    def test_get(self):
        self.assertEquals(TestModel.objects.count(), 0)

        self.assertRaises(TestModel.DoesNotExist, TestModel.objects.get, 'foo')

        inst = TestModel.objects.create(str_='foo')

        self.assertEquals(TestModel.objects.count(), 1)

        self.assertEquals(TestModel.objects.get(inst.pk), inst)

    def test_delete(self):
        self.assertEquals(TestModel.objects.count(), 0)

        inst = TestModel.objects.create(str_='foo')

        self.assertEquals(TestModel.objects.count(), 1)
        
        inst.delete()

        self.assertEquals(TestModel.objects.count(), 0)

        self.assertRaises(TestModel.DoesNotExist, TestModel.objects.get, 'foo')

    def test_saving_behavior(self):
        self.assertEquals(TestModel.objects.count(), 0)

        inst = TestModel()
        
        self.assertFalse(inst.pk)
        
        self.assertEquals(TestModel.objects.count(), 0)
        
        inst.save()
        
        self.assertTrue(inst.pk)
        self.assertEquals(TestModel.objects.count(), 1)
        self.assertEquals(TestModel.objects.get(inst.pk), inst)

        self.assertEquals(inst.str_, '')
        self.assertEquals(inst.int_, 0)
        self.assertEquals(inst.float_, 0.0)
        self.assertEquals(len(inst.list_), 0)
        
        inst.update(str_='foo')

        self.assertEquals(TestModel.objects.count(), 1)
        self.assertEquals(inst.str_, 'foo')
        self.assertEquals(inst.int_, 0)
        self.assertEquals(inst.float_, 0.0)
        self.assertEquals(len(inst.list_), 0)
        
        inst = TestModel.objects.get(pk=inst.pk)

        self.assertEquals(inst.str_, 'foo')
        self.assertEquals(inst.int_, 0)
        self.assertEquals(inst.float_, 0.0)
        self.assertEquals(len(inst.list_), 0)

        inst = TestModel(float_=1.0)
        
        self.assertFalse(inst.pk)
        
        inst.save()

        self.assertEquals(TestModel.objects.count(), 2)
        
        self.assertEquals(inst.str_, '')
        self.assertEquals(inst.int_, 0)
        self.assertEquals(inst.float_, 1.0)
        self.assertEquals(len(inst.list_), 0)



import unittest2

class TestModel(unittest2.TestCase):
    def setUp(self):
        class Sample(models.Model):
            attr1 = models.String()
            attr2 = models.String()
            class Meta:
                manager = ldtools.Manager

        self.p1 = Sample(attr1=u"hü", attr2=u"vä")
        self.p2 = Sample(attr1=u"hü", attr2=u"vä")
        self.p3 = Sample(attr1=u"hüa", attr2=u"vä")

    def test_hash1(self):
        logging.info("h1")
        sett=set([self.p1, self.p2])
        logging.info("h11")
        self.assertIn(self.p1, sett)

    def test_hash2(self):
        logging.info("h2")
        self.assertNotIn(self.p3, set([self.p1, self.p2]))

    def test_equivalence1(self):
        logging.info("e1")
        self.assertEquals(self.p1, self.p2)

    def test_equivalence2(self):
        logging.info("e2")
        self.assertNotEquals(self.p1, self.p3)
