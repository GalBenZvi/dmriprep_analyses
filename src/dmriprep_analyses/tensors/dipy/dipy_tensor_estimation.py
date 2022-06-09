from pathlib import Path
from typing import Union

from analyses_utils.entities.derivatives.dmriprep import DmriprepDerivatives
from dipy.workflows.reconst import ReconstDkiFlow, ReconstDtiFlow

from dmriprep_analyses.tensors.dipy.utils.templates import (
    KWARGS_MAPPING,
    TENSOR_DERIVED_METRICS,
)
from dmriprep_analyses.tensors.tensor_estimation import TensorEstimation
from dmriprep_analyses.tensors.utils.functions import estimate_sigma


class DipyTensorEstimation(TensorEstimation):
    """
    Class for tensor estimation using dipy.

    Parameters
    ----------
    TensorEstimation : TensorEstimation
        TensorEstimation object.
    """

    TENSORS_BASE = "dipy"
    INPUT_KEY = "input_files"
    #: Templates
    METRICS = TENSOR_DERIVED_METRICS.copy()

    #: Tensor Workflows
    TENSOR_FITTING_KWARGS = KWARGS_MAPPING

    TENSOR_WORKFLOWS = dict(
        diffusion_tensor=ReconstDtiFlow,
        diffusion_kurtosis=ReconstDkiFlow,
        restore_tensor=ReconstDtiFlow,
    )
    TENSOR_TYPES = dict(
        diffusion_tensor={"acq": "dt", "kwargs": {"fit_method": "NLLS"}},
        diffusion_kurtosis={"acq": "dk", "kwargs": {"fit_method": "NLLS"}},
        restore_tensor={
            "acq": "rt",
            "kwargs": {"fit_method": "restore", "sigma": estimate_sigma},
        },
    )

    def __init__(
        self,
        derivatives: DmriprepDerivatives = None,
        base_dir: Union[Path, str] = None,
        participant_label: str = None,
        sessions_base: str = None,
    ):
        super().__init__(
            derivatives, base_dir, participant_label, sessions_base
        )
