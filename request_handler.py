from load_balancer import LoadBalancer


class RequestHandler:

	@staticmethod
	def random_invocation():
		load_balancer = LoadBalancer()
		for i in range(100):
			print(load_balancer.get_random())

	@staticmethod
	def round_robin_invocation():
		load_balancer = LoadBalancer()
		for i in range(100):
			print(load_balancer.get_round_robin())

