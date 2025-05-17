import time

class TrainStack:
    def __init__(self, max_trains=10, max_carts=10):
        self.max_trains = max_trains
        self.max_carts = max_carts
        self.trains = []

    def _create_cart(self, data):
        return {
            "data": data,
            "timestamp": time.time(),
        }

    def add_train(self, data_list):
        if len(data_list) != self.max_carts:
            raise ValueError("data_list must have {} items".format(self.max_carts))
        train = [self._create_cart(data) for data in data_list]
        self.trains.append(train)
        if len(self.trains) > self.max_trains:
            self.trains.pop(0)

    def get_latest_data(self):
        if not self.trains:
            return None
        return self.trains[-1]
