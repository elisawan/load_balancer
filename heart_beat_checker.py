import time
from threading import Timer


class HeartBeatChecker:
    heart_beat_interval = 10

    def __init__(self, load_balancer):
        self.load_balancer = load_balancer

    def check(self):
        print(time.time())
        for i, provider in enumerate(self.load_balancer.providers):
            if not provider.provider.check():
                provider.exclude()
                provider.is_alive = False
            else:
                if provider.is_alive:  # was already alive
                    provider.include()
                provider.is_alive = True
        Timer(interval=self.heart_beat_interval, function=self.check).start()
