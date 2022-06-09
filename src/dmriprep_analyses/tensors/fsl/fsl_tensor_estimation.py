from pathlib import Path
from typing import Union

from analyses_utils.entities.derivatives.dmriprep import DmriprepDerivatives

from dmriprep_analyses.tensors.fsl.utils.templates import (
    KWARGS_MAPPING,
    TENSOR_DERIVED_METRICS,
)
from dmriprep_analyses.tensors.fsl.workflows.reconst import ReconstDtiFlow

# from dmriprep_analyses.tensors.mrtrix.workflows.reconst import ReconstDtiFlow
from dmriprep_analyses.tensors.tensor_estimation import TensorEstimation


class FslTensorEstimation(TensorEstimation):
    """
    Class for tensor estimation using dipy.

    Parameters
    ----------
    TensorEstimation : TensorEstimation
        TensorEstimation object.
    """

    TENSORS_BASE = "fsl"
    INPUT_KEY = "dwi"
    #: Templates
    METRICS = TENSOR_DERIVED_METRICS.copy()

    #: Tensor Workflows
    TENSOR_FITTING_KWARGS = KWARGS_MAPPING

    TENSOR_WORKFLOWS = dict(
        diffusion_tensor=ReconstDtiFlow,
    )
    TENSOR_TYPES = dict(
        diffusion_tensor={"acq": "dt", "kwargs": {}},
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
