# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/viterbi.py


def viterbi(
    observations: list[int],
    states: list[str],
    start_prob: dict[str, float],
    trans_prob: dict[str, dict[str, float]],
    emit_prob: dict[str, dict[int, float]],
) -> list[str]:
    """
    Viterbi algorithm for finding the most likely sequence of hidden states.

    >>> states = ["Healthy", "Fever"]
    >>> observations = [0, 1, 2]  # normal, cold, dizzy
    >>> start_p = {"Healthy": 0.6, "Fever": 0.4}
    >>> trans_p = {"Healthy": {"Healthy": 0.7, "Fever": 0.3}, "Fever": {"Healthy": 0.4, "Fever": 0.6}}
    >>> emit_p = {"Healthy": {0: 0.5, 1: 0.4, 2: 0.1}, "Fever": {0: 0.1, 1: 0.3, 2: 0.6}}
    >>> viterbi(observations, states, start_p, trans_p, emit_p)
    ['Healthy', 'Healthy', 'Fever']
    """
    n = len(observations)
    if n == 0:
        return []

    # Initialization
    V = [{}]
    path = {}
    for s in states:
        V[0][s] = start_prob[s] * emit_prob[s][observations[0]]
        path[s] = [s]

    # Recursion
    for t in range(1, n):
        V.append({})
        new_path = {}
        for s in states:
            prob, state = max(
                (V[t - 1][s0] * trans_prob[s0][s] * emit_prob[s][observations[t]], s0)
                for s0 in states
            )
            V[t][s] = prob
            new_path[s] = path[state] + [s]
        path = new_path

    # Termination
    prob, state = max((V[n - 1][s], s) for s in states)
    return path[state]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    states = ["Healthy", "Fever"]
    observations = [0, 1, 2]
    start_p = {"Healthy": 0.6, "Fever": 0.4}
    trans_p = {
        "Healthy": {"Healthy": 0.7, "Fever": 0.3},
        "Fever": {"Healthy": 0.4, "Fever": 0.6},
    }
    emit_p = {
        "Healthy": {0: 0.5, 1: 0.4, 2: 0.1},
        "Fever": {0: 0.1, 1: 0.3, 2: 0.6},
    }

    result = viterbi(observations, states, start_p, trans_p, emit_p)
    print(f"  Observations: {observations}")
    print(f"  Most likely states: {result}")
