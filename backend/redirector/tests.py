from django.test import TestCase

from .etl import DomainETL
from .models import Domain, DomainPool


class DomainETLTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        first_pool = DomainPool.objects.create(name="First Pool", description="My First Pool")
        second_pool = DomainPool.objects.create(name="Second Pool", description="My Second Pool")

        cls.domain_1 = Domain.objects.create(name="domain1.com.br", weight=1, domain_pool=first_pool)
        cls.domain_2 = Domain.objects.create(name="domain2.com.br", weight=2, domain_pool=first_pool)
        cls.domain_3 = Domain.objects.create(name="domain3.com.br", weight=1, domain_pool=second_pool)
        cls.domain_4 = Domain.objects.create(name="domain4.com.br", weight=2, domain_pool=second_pool)

    def test_domain_etl(self):
        domain1_data = DomainETL.run(self.domain_1.id, skip_load=True)
        self.assertEqual(domain1_data["domain_name"], self.domain_1.name)
        self.assertEqual(domain1_data["domain_weight"], self.domain_1.weight)
        self.assertEqual(domain1_data["domain_pool_id"], self.domain_1.domain_pool.id)

        domain2_data = DomainETL.run(self.domain_2.id, skip_load=True)
        self.assertEqual(domain2_data["domain_name"], self.domain_2.name)
        self.assertEqual(domain2_data["domain_weight"], self.domain_2.weight)
        self.assertEqual(domain2_data["domain_pool_id"], self.domain_2.domain_pool.id)

        domain3_data = DomainETL.run(self.domain_3.id, skip_load=True)
        self.assertEqual(domain3_data["domain_name"], self.domain_3.name)
        self.assertEqual(domain3_data["domain_weight"], self.domain_3.weight)
        self.assertEqual(domain3_data["domain_pool_id"], self.domain_3.domain_pool.id)

        domain4_data = DomainETL.run(self.domain_4.id, skip_load=True)
        self.assertEqual(domain4_data["domain_name"], self.domain_4.name)
        self.assertEqual(domain4_data["domain_weight"], self.domain_4.weight)
        self.assertEqual(domain4_data["domain_pool_id"], self.domain_4.domain_pool.id)
