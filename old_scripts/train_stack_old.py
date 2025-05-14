import random
import time
import threading
import logging

class TrainStack:
    def __init__(self, max_trains=5, max_carts=10):
        self.trains = []  # This will be a list of trains
        self.max_trains = max_trains
        self.max_carts = max_carts
        self.lock = threading.Lock()

    def _create_cart(self, data, index):
        # Cart will store data and metadata like timestamp, version, and historical data
        return {
            'data': data,
            'timestamp': time.time(),
            'version': index,
            'history': [],  # Store historical data for drift analysis
            'metadata': {
                'index': index,
                'parity': None  # Will be set when parity is calculated
            }
        }

    def _generate_parity(self, carts):
        # Parity is XOR of all data values for redundancy
        parity = 0
        for cart in carts:
            parity ^= cart['data']  # Assuming data is integer for simplicity
        return parity

    def _update_parity(self, train):
        carts = train['carts']
        train['parity'] = self._generate_parity(carts)

    def _mirror_data(self, train):
        # Creates a mirrored copy of the train
        mirrored_train = {
            'carts': [cart.copy() for cart in train['carts']],
            'parity': train['parity']
        }
        return mirrored_train

    def add_train(self, data):
        with self.lock:
            if len(self.trains) >= self.max_trains:
                self.trains.pop(0)  # Remove the oldest train if max reached

            new_train = {'carts': [], 'parity': None}
            for i in range(self.max_carts):
                cart = self._create_cart(data, i)
                new_train['carts'].append(cart)
            
            self._update_parity(new_train)
            self.trains.append(new_train)

    def pop_train(self):
        with self.lock:
            if self.trains:
                return self.trains.pop(0)
            return None

    def get_train(self, index):
        with self.lock:
            if index < len(self.trains):
                return self.trains[index]
            return None

    def shift_cart(self, train_index, cart_index, new_data):
        with self.lock:
            train = self.get_train(train_index)
            if train and cart_index < len(train['carts']):
                train['carts'][cart_index]['data'] = new_data
                self._update_parity(train)  # Recalculate parity after data shift
                return True
            return False

    def apply_drift(self):
        with self.lock:
            for train in self.trains:
                for cart in train['carts']:
                    # Apply more aggressive drift (20% - 50%) for higher variation
                    drift_percentage = random.uniform(20.0, 50.0)  # Increased drift range (20% - 50%)
                    previous_value = cart['data']
                    cart['data'] += cart['data'] * drift_percentage  # Apply the drift percentage to current value

                    # Record the drift change in history
                    cart['history'].append(previous_value)

                    # Recalculate the severity
                    severity = self.analyze_drift(cart, drift_percentage)
                    cart['metadata']['severity'] = severity
                self._update_parity(train)  # Recalculate parity after drift

    def analyze_drift(self, cart, drift_amount):
        """ Analyze the drift to check for large abnormal changes. """
        historical_drift = [abs(cart['data'] - value) for value in cart['history']]  # Drift over time

        max_drift = max(historical_drift)  # Get the largest drift observed
        average_drift = sum(historical_drift) / len(historical_drift)  # Average drift

        # Calculate the severity based on historical data
        if max_drift > 25:  # Adjust threshold for larger drift to be categorized as "bad"
            severity = 'Bad'
        elif average_drift > 15:  # Increase threshold for "moderate"
            severity = 'Moderate'
        else:
            severity = 'Low'

        logging.debug(f"Calculated drift: {drift_amount}, Max Drift: {max_drift}, Average Drift: {average_drift}")
        return severity
