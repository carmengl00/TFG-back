import json

from slots.tests.requests.mutations import DELETE_RESERVED_SLOT
from slots.models import ReservedSlot
import pytest
from mixer.backend.django import mixer
from base.factory_test_case import TestBase

@pytest.mark.django_db()
class TestResourcesMutations(TestBase):
    def test_delete_reserved_slot(self):
        reservedSlot = mixer.blend(
            ReservedSlot,
        )
        variables = {
            "id": str(reservedSlot.id),
        }
        response = self.post(query=DELETE_RESERVED_SLOT, variables=variables, user=self.user)
        data = json.loads(response.content.decode())
        resource = data.get("data").get("deleteReservedSlot")
        assert resource is True