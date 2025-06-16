import pysb
import numpy as np


class Range(pysb.Annotation):
    """Parameter range to sample using optimization."""

    def __init__(
        self,
        param: pysb.Parameter,
        lower: float,
        upper: float,
        transform: str | None = None,
        as_prior: bool = True,
    ):
        self._lower = lower
        self._upper = upper
        self._transform = transform
        self._as_prior = as_prior
        super().__init__(param, (lower, upper), "parameter-range")
        return

    @property
    def as_prior(self):
        return self._as_prior

class Prior(pysb.Annotation):
    """Parameter prior probability distribution for Bayesian Monte Carlo methods."""

    def __init__(
        self,
        param: pysb.Parameter,
        dist: str,
        loc: float = 0.0,
        scale: float = 1.0,
        transform: str | None = None,
    ):
        self._dist = dist
        self._loc = loc
        self._scale = scale
        self._transform = transform
        super().__init__(param, {dist: {"loc": loc, "scale": scale}}, "parameter-prior")
        return


class Fixed(pysb.Annotation):
    """Fix to a certain value and don't include it in parameter estimations."""

    def __init__(self, param: pysb.Parameter, value: float = None):
        if value is None:
            self._value = param.value
        else:
            self._value = value
        super().__init__(param, self._value, "parameter-fixed")
        return
