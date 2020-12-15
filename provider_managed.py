from threading import BoundedSemaphore

from provider import Provider
from provider_state_enum import ProviderStateEnum


class ProviderManaged(Provider):

    max_parallel_requests = 2

    def __init__(self, provider):
        super().__init__(provider.provider_id)
        self.provider = provider
        self.state = ProviderStateEnum.active
        self.bounded_semaphore = BoundedSemaphore(value=self.max_parallel_requests)
        self.is_alive = True

    def exclude(self):
        self.state = ProviderStateEnum.inactive

    def include(self):
        self.state = ProviderStateEnum.active

    def get(self):
        super().get()
        print("release")
        self.bounded_semaphore.release()
