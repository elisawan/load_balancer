from load_balancer import LoadBalancer
from provider import Provider

provider1 = Provider(provider_id='1')
provider2 = Provider(provider_id='2')

load_balancer = LoadBalancer()
load_balancer.register(provider=provider1)
load_balancer.register(provider=provider2)

load_balancer.get('random')
load_balancer.get('random')
load_balancer.get('random')
load_balancer.get('random')
load_balancer.get('round_robin')
load_balancer.get('round_robin')
load_balancer.get('round_robin')
load_balancer.get('random')
load_balancer.get('random')

