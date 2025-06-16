from abc import ABC, abstractmethod
import pysb

from .sampled import Range, Prior, Fixed

class BaseEstimator(ABC):
    """Base class for parameter estimators in pysb-fit."""

    def __init__(self, model: pysb.Model):
        self.model = model
        self.sampled_parameters = None
        self.parameters_mask = None
        self.sampling_values = None
        self.transforms = None
        self._assemble_sampled_parameters()
        self._set_fixed_parameters()
        return

    def _include_range(self, *args):
        pass

    def _assemble_sampled_parameters(self):
        param_list = []
        params_values = dict()
        transforms = []
        for annotation in self.model.annotations:
            if isinstance(annotation, (Range, Prior)):
                if annotation.predicate == self._estimator_predicate:
                    param_list.append(annotation.subject)
                    params_values[annotation.subject.name] = annotation.object
                    transforms.append(annotation._transform)

                else:
                    self._include_range(self, annotation, param_list, params_values, transforms)


        self.sampled_parameters = param_list
        self.sampling_values = params_values
        self.transforms = transforms
        parameter_names = self.parameter_names
        self.parameters_mask = [
            param.name in parameter_names for param in self.model.parameters
        ]
        return
    
    def _set_fixed_parameters(self):
        for annotation in self.model.annotations:
            if isinstance(annotation, Fixed):
                annotation.subject.value = annotation.object
        return      

    @property
    def parameter_names(self):
        return [param.name for param in self.sampled_parameters]

    @abstractmethod
    def fit(self):
        return


class OptimizerMixin:
    _estimator_type = "optimizer"
    _estimator_predicate = "parameter-range"


class MonteCarloMixin:
    _estimator_type = "monte carlo"
    _estimator_predicate = "parameter-prior"

    def _include_range(self, annotation, param_list, param_values, transforms):
        if isinstance(annotation, Range):
            if annotation.as_prior:
                loc = annotation._lower
                scale = (annotation._upper - annotation._lower)
                prior_dict = {"norm": {"loc": loc, "scale": scale}}
                param_list.append(annotation.subject)
                param_values[annotation.subject.name] = prior_dict
                transforms.append(annotation._transform)
        return
