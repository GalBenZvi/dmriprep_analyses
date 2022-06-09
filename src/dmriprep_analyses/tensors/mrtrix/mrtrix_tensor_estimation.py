from pathlib import Path
from typing import List, Union

from analyses_utils.entities.derivatives.dmriprep import DmriprepDerivatives

from dmriprep_analyses.tensors.mrtrix.utils.templates import (
    KWARGS_MAPPING,
    TENSOR_DERIVED_METRICS,
)
from dmriprep_analyses.tensors.mrtrix.workflows.reconst import ReconstDtiFlow
from dmriprep_analyses.tensors.tensor_estimation import TensorEstimation


class MrtrixTensorEstimation(TensorEstimation):
    """
    Class for tensor estimation using dipy.

    Parameters
    ----------
    TensorEstimation : TensorEstimation
        TensorEstimation object.
    """

    TENSORS_BASE = "mrtrix3"
    INPUT_KEY = "in_file"
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

    def build_output_dictionary(
        self, source: Path, tensor_type: str, outputs: List[str] = None
    ) -> dict:
        """
        Based on a *source* DWI, reconstruct output names for tensor-derived
        metric available under *tensor_type*.

        Parameters
        ----------
        source : Path
            The source DWI file.
        tensor_type : str
            The tensor estimation method (either "dt" or "dk")
        outputs : list, optional
            Requested tensor-derived outputs, by default All available

        Returns
        -------
        dict
            A dictionary with keys of available/requested outputs and their
            corresponding paths
        """
        outputs = outputs or self.METRICS.get(tensor_type)
        target = {}
        entities = {
            "acquisition": self.TENSOR_TYPES.get(tensor_type).get("acq"),
            **self.TENSOR_ENTITIES,
        }
        for output in outputs:
            if self.validate_requested_output(tensor_type, output):
                output_entities = entities.copy()
                if output == "tensor":
                    output_entities["extension"] = ".mif"
                kwargs = dict(
                    output=output,
                    parent=self.derivatives.path.parent,
                    source=source,
                    entities=output_entities,
                )
                base_target = Path(self._gen_output_name(**kwargs))
                if self.TENSORS_BASE:
                    base_target = (
                        base_target.parent
                        / self.TENSORS_BASE
                        / base_target.name
                    )
                    base_target.parent.mkdir(exist_ok=True)
                target[f"out_{output}"] = base_target
        return target
