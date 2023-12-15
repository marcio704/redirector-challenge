import json
import logging

from .models import Domain


logger = logging.getLogger(__name__)


class DomainETL:
    DESTINATION_FILE = "../domains.jsonl"

    @classmethod
    def run(cls, domain_id: int, skip_load=False) -> dict:
        domain = cls.extract(domain_id)
        domain_data = cls.transform(domain)

        if skip_load:
            return domain_data

        cls.load(domain_data)

    @staticmethod
    def extract(domain_id: int) -> Domain:
        return Domain.objects.get(pk=domain_id)

    @staticmethod
    def transform(domain: Domain) -> dict:
        return {
            "domain_pool_id": domain.domain_pool.id,
            "domain_name": domain.name,
            "domain_weight": domain.weight,
        }

    @classmethod
    def load(cls, domain_data: dict) -> None:
        """
        This is saving the domain_data on a local .jsonl file for the sake of simplicity.
        For production environment, I'd recommend saving the domain_data on a distributed DynamoDB instead.
        This data will be read by the Lambda Flask microservice.
        See the architectural diagram on README.md file.
        :param domain_data:
        :return:
        """
        logger.info(f"Saving into DynamoDB: {domain_data}")

        with open(cls.DESTINATION_FILE, 'a', encoding='utf-8') as file:
            # Ensure the file ends with a newline character
            if file.tell() > 0:
                file.write('\n')

            # Write the new JSON row to the file
            json.dump(domain_data, file, ensure_ascii=False)
            file.write('\n')
