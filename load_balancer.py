import random
from threading import Timer, Thread
from time import sleep

from heart_beat_checker import HeartBeatChecker
from provider_state_enum import ProviderStateEnum
from provider_managed import ProviderManaged


class LoadBalancer:

	max_registered_providers = 10
	max_parallel_request = 2
	max_tentatives_to_get_available_providers = 2

	def __init__(self):
		self.providers = []  # List[ProviderWithState]
		self.last_used_provider = 0
		self.heart_beat_checker = HeartBeatChecker(load_balancer=self)
		self.timer = Timer(interval=self.heart_beat_checker.heart_beat_interval, function=self.heart_beat_checker.check).start()

	def register(self, provider):
		if len(self.providers) >= LoadBalancer.max_registered_providers:
			raise ValueError('Load balancer has reached capacity, provider cannot be registered.')
		self.providers.append(ProviderManaged(provider=provider))

	def get(self, mode):
		try:
			provider = self.get_active_provider(mode)
		except ValueError as e:
			print(e)
			return
		provider.bounded_semaphore.acquire()
		print('{}_{}'.format(provider.provider_id, provider.bounded_semaphore._value))
		Thread(target=self.__get, kwargs={'provider': provider}).start()
		return

	def __get(self, provider):
		provider.get()

	def get_active_provider(self, mode):
		num_providers = len(self.providers)
		provider_index = None
		for _ in range(self.max_tentatives_to_get_available_providers):
			for _ in range(num_providers):
				if mode == 'random':
					if provider_index is None:
						provider_index = random.randint(0, num_providers - 1)
					else:
						provider_index = (provider_index + 1) % num_providers
				else:
					self.last_used_provider = (self.last_used_provider + 1) % num_providers
					provider_index = self.last_used_provider
				if self.providers[provider_index].state == ProviderStateEnum.active:
					return self.providers[provider_index]
			sleep(3)
		raise ValueError('Failed to process request: no active providers')

