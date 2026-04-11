"""
Reynolds Number.

The Reynolds number is a dimensionless quantity used to predict flow patterns:
    Re = rho * v * L / mu  =  v * L / nu

where:
    rho = fluid density (kg/m^3)
    v   = flow velocity (m/s)
    L   = characteristic length (m)
    mu  = dynamic viscosity (Pa*s)
    nu  = kinematic viscosity (m^2/s)

Re < 2300:  laminar flow
Re > 4000:  turbulent flow
2300 < Re < 4000:  transitional flow

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/reynolds_number.py
"""


def reynolds_number(
    density: float, velocity: float, length: float, viscosity: float
) -> float:
    """
    Calculate Reynolds number from density and dynamic viscosity.

    >>> reynolds_number(1000, 1, 0.1, 0.001)
    100000.0
    >>> reynolds_number(1.225, 30, 1, 1.81e-5)
    2030386.74
    >>> reynolds_number(1000, 0.01, 0.05, 0.001)
    500.0
    >>> reynolds_number(0, 1, 1, 0.001)
    Traceback (most recent call last):
        ...
    ValueError: density must be positive
    >>> reynolds_number(1000, 1, 1, 0)
    Traceback (most recent call last):
        ...
    ValueError: viscosity must be positive
    """
    if density <= 0:
        raise ValueError("density must be positive")
    if velocity < 0:
        raise ValueError("velocity must be non-negative")
    if length <= 0:
        raise ValueError("length must be positive")
    if viscosity <= 0:
        raise ValueError("viscosity must be positive")

    return round(density * velocity * length / viscosity, 2)


def flow_regime(re: float) -> str:
    """
    Classify the flow regime based on Reynolds number.

    >>> flow_regime(1000)
    'laminar'
    >>> flow_regime(3000)
    'transitional'
    >>> flow_regime(5000)
    'turbulent'
    """
    if re < 2300:
        return "laminar"
    elif re > 4000:
        return "turbulent"
    return "transitional"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
