from collections import defaultdict
import numpy as np

def train_state_regression(orders):
    """
    Simple deterministic regression:
    average order total per state
    """
    totals = defaultdict(list)

    for o in orders:
        if "state" in o and "total" in o:
            totals[o["state"]].append(float(o["total"]))

    model = {}
    for state, values in totals.items():
        model[state] = round(float(np.mean(values)), 2)

    return model


def predict_total(state, model):
    return model.get(state.upper())
