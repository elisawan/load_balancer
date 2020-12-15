import random
import time


class Provider:
    def __init__(self, provider_id):
        self.provider_id = provider_id

    def get(self):
        print('Provider get {}'.format(self.provider_id))
        time.sleep(10)
        return str(self.provider_id)

    def check(self):
        return random.randint(0, 1)





