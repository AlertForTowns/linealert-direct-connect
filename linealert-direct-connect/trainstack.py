import time
import threading

class TrainStack:
    def __init__(self, max_trains=10, max_carts=10):
        self.trains = []
        self.max_trains = max_trains
        self.max_carts = max_carts
        self.lock = threading.Lock()

    def _create_cart(self, data, index):
        return {
            'data': data,
            'timestamp': time.time(),
            'version': index,
            'metadata': {'index': index}
        }

    def add_train(self, data):
        with self.lock:
            if len(self.trains) >= self.max_trains:
                self.trains.pop(0)
            new_train = {'carts': [self._create_cart(data, i) for i in range(self.max_carts)]}
            self.trains.append(new_train)

    def get_recent_data(self):
        with self.lock:
            return [train['carts'][0]['data'] for train in self.trains if train['carts']]
