"""
Chaos Machine -- a pseudorandom number generator based on chaotic dynamical systems.

The machine maintains a buffer of floating-point values in (0, 1) and a
corresponding parameter space. Data is fed in via push() which perturbs all
buffer entries using logistic-map-like transitions. Output is extracted via
pull() which evolves one entry and applies an XOR-shift to produce a 32-bit
integer.

The combination of logistic maps + XOR-shift creates a cryptographically
inspired (but NOT cryptographically secure) PRNG.

source: https://github.com/TheAlgorithms/Python/blob/master/hashes/chaos_machine.py
"""

# Chaos Machine (K, t, m)
K = [0.33, 0.44, 0.55, 0.44, 0.33]
t = 3
m = 5

# Buffer Space (with Parameters Space)
buffer_space: list[float] = []
params_space: list[float] = []

# Machine Time
machine_time = 0


def push(seed: int) -> None:
    """
    Push data into the chaos machine, perturbing all buffer entries.

    Uses logistic-map-like transitions with orbit and trajectory changes.
    Each buffer entry is evolved using the seed and neighboring entries.
    """
    global buffer_space, params_space, machine_time, K, m, t

    for key, value in enumerate(buffer_space):
        e = float(seed / value)
        value = (buffer_space[(key + 1) % m] + e) % 1
        r = (params_space[key] + e) % 1 + 3
        buffer_space[key] = round(float(r * value * (1 - value)), 10)
        params_space[key] = r

    assert max(buffer_space) < 1
    assert max(params_space) < 4
    machine_time += 1


def pull() -> int:
    """
    Pull a 32-bit pseudorandom integer from the chaos machine.

    Evolves one buffer entry through t iterations of the logistic map,
    then combines two buffer entries via XOR-shift to produce output.
    """
    global buffer_space, params_space, machine_time, K, m, t

    def xorshift(x: int, y: int) -> int:
        x ^= y >> 13
        y ^= x << 17
        x ^= y >> 5
        return x

    key = machine_time % m

    for _ in range(t):
        r = params_space[key]
        value = buffer_space[key]
        buffer_space[key] = round(float(r * value * (1 - value)), 10)
        params_space[key] = (machine_time * 0.01 + r * 1.01) % 1 + 3

    x = int(buffer_space[(key + 2) % m] * (10**10))
    y = int(buffer_space[(key - 2) % m] * (10**10))
    machine_time += 1
    return xorshift(x, y) % 0xFFFFFFFF


def reset() -> None:
    """
    Reset the chaos machine to initial state.

    Copies K into buffer_space, zeroes params_space, resets machine_time.
    """
    global buffer_space, params_space, machine_time, K, m, t
    buffer_space = list(K)
    params_space = [0] * m
    machine_time = 0


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # Demo: push random data, then pull outputs
    import random

    reset()
    message = random.sample(range(0xFFFFFFFF), 100)
    for chunk in message:
        push(chunk)

    print("Chaos Machine output (5 pulls):")
    for _ in range(5):
        print(f"  {format(pull(), '#010x')}")
