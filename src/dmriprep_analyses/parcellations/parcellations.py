"""
Definition of the :class:`NativeParcellation` class.
"""
import logging
from pathlib import Path
from typing import Callable, Union

import numpy as np
import pandas as pd
from analyses_utils.data.bids import build_relative_path
from analyses_utils.entities.analysis.logger import get_console_handler
from analyses_utils.entities.derivatives.dmriprep import DmriprepDerivatives
from analyses_utils.entities.session import Session
from brain_parts.parcellation.parcellations import (
    Parcellation as parcellation_manager,
)

from dmriprep_analyses.dmriprep_analysis import DmriprepAnalysis
from dmriprep_analyses.registrations.registrations import NativeRegistration
from dmriprep_analyses.tensors.dipy.dipy_tensor_estimation import (
    DipyTensorEstimation,
)
from dmriprep_analyses.tensors.fsl.fsl_tensor_estimation import (
    FslTensorEstimation,
)
from dmriprep_analyses.tensors.mrtrix.mrtrix_tensor_estimation import (
    MrtrixTensorEstimation,
)


class NativeParcellation(DmriprepAnalysis):
    TENSOR_RECONSTRUCTURION_SOFTWARES = {
        "dipy": DipyTensorEstimation,
        "fsl": FslTensorEstimation,
        "mrtrix": MrtrixTensorEstimation,
    }

    def __init__(
        self,
        derivatives: DmriprepDerivatives = None,
        base_dir: Union[Path, str] = None,
        participant_label: str = None,
        sessions_base: str = None,
        tensor_reconstruction_software: str = "dipy",
    ):
        super().__init__(
            derivatives, base_dir, participant_label, sessions_base
        )
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(get_console_handler())
        self.registration_manager = NativeRegistration(self.derivatives)
        self.tensor_estimation = self.TENSOR_RECONSTRUCTURION_SOFTWARES.get(
            tensor_reconstruction_software
        )(self.derivatives)
        self.parcellation_manager = parcellation_manager()

    def generate_rows(
        self,
        tensor_type: str,
        session: Union[str, list] = None,
    ) -> pd.MultiIndex:
        """
        Generate target DataFrame's multiindex for participant's rows.

        Parameters
        ----------
        participant_label : str
            Specific participants' labels
        session : Union[str, list]
            Specific session(s)' labels

        Returns
        -------
        pd.MultiIndex
            A MultiIndex comprised of participant's label
            and its corresponding sessions.
        """

        sessions = [
            Session(
                self.derivatives.participant, session.replace("ses-", "")
            ).date
            for session in self.listify_sessions(session)
        ]
        metrics = self.tensor_estimation.METRICS.get(tensor_type)
        return pd.MultiIndex.from_product(
            [[self.participant_label], sessions, metrics]
        )

    def build_output_name(
        self,
        parcellation_scheme: str,
        parcellation_type: str,
        tensor_type: str,
        parcellation_image: Union[Path, str],
        measure: Callable = np.nanmean,
    ) -> Path:
        """
        Reconstruct output "table"'s path

        Parameters
        ----------
        parcellation_scheme : str
            Parcellation scheme to parcellate by
        parcellation_type : str
            Either "Whole_brain" or "gm_cropped"
        tensor_type : str
            Tensor reconstruction method
        parcellation_image : Union[Path, str]
            Subject-specific parcellation image
        measure : Callable, optional
            Measure to parcellate by, by default np.nanmean

        Returns
        -------
        Path
            Path to output table.
        """
        measure = measure.__name__
        acquisition = self.tensor_estimation.TENSOR_TYPES.get(tensor_type).get(
            "acq"
        )
        entities = {
            "atlas": parcellation_scheme,
            "suffix": "dseg",
            "acquisition": acquisition,
            "extension": ".pickle",
            "measure": measure,
        }
        parts = parcellation_type.split("_")
        entities["label"] = "".join([parts[0], parts[1].capitalize()])
        base_target = self.derivatives.path.parent / build_relative_path(
            parcellation_image, entities
        )
        return (
            base_target.parent
            / self.tensor_estimation.TENSORS_BASE
            / base_target.name
        )

    def parcellate_single_tensor(
        self,
        parcellation_scheme: str,
        tensor_type: str,
        session: str,
        parcellation_type: str = "whole_brain",
        measure: Callable = np.nanmean,
        force: bool = False,
    ) -> pd.DataFrame:
        """
        Parcellate tensor-derived metrics

        Parameters
        ----------
        parcellation_scheme : str
            Parcellation scheme to parcellate by
        tensor_type : str
            Tensor reconstruction method
        participant_label : str
            Specific participant's label
        parcellation_type : str, optional
            Either "gm_cropped" or "whole_brain", by default "gm_cropped"
        session : Union[str, list], optional
            Specific session's label, by default None
        measure : Callable, optional
            Measure for parcellation, by default np.nanmean
        force : bool, optional
            Whether to re-write existing files, by default False

        Returns
        -------
        pd.DataFrame
            A DataFrame with (participant_label,session,tensor_type,metrics)
            as index and (parcellation_scheme,label) as columns
        """
        rows = self.generate_rows(tensor_type, session)
        tensors = self.tensor_estimation.run(session, tensor_type)
        parcellation_images = self.registration_manager.run(
            parcellation_scheme,
            session,
            force=force,
        )
        data = pd.DataFrame(index=rows)

        session_date = Session(
            self.derivatives.participant, session.replace("ses-", "")
        ).date
        parcellation = parcellation_images.get(session).get(parcellation_type)
        output_file = self.build_output_name(
            parcellation_scheme,
            parcellation_type,
            tensor_type,
            parcellation,
            measure,
        )
        if output_file.exists() and not force:
            return pd.read_pickle(output_file)
        for metric, metric_image in (
            tensors.get(session).get(tensor_type).items()
        ):
            key = metric.split("_")[-1]

            tmp_data = self.parcellation_manager.parcellate_image(
                parcellation_scheme,
                parcellation,
                metric_image,
                key,
                measure=measure,
            )
            data.loc[
                (self.participant_label, session_date, key),
                tmp_data.index,
            ] = tmp_data.loc[tmp_data.index]
        data.to_pickle(output_file)
        return data

    def parcellate_single_subject(
        self,
        parcellation_scheme: str,
        parcellation_type: str = "whole_brain",
        session: Union[str, list] = None,
        tensor_types: Union[str, list] = None,
        measure: Callable = np.nanmean,
        force: bool = False,
    ) -> pd.DataFrame:
        """
        Perform all parcellation available for a single subject

        Parameters
        ----------
        parcellation_scheme : str
            Parcellation scheme to parcellate by
        participant_label : str
            A single participant's label
        parcellation_type : str, optional
            Either "whole_brain" or "gm_cropped", by default "whole_brain"
        session : Union[str, list], optional
            A specific session's label, by default None
        measure : Callable, optional
            Measure to parcellate by, by default np.nanmean
        force : bool, optional
            Whether to re-write existing files, by default False

        Returns
        -------
        pd.DataFrame
            All subject's availble parcellated data
        """
        data = pd.DataFrame()
        for session in self.listify_sessions(session):
            session_data = pd.DataFrame()
            for tensor_type in self.tensor_estimation.listify_tensor_type(
                tensor_types
            ):
                # try:
                tensor_data = self.parcellate_single_tensor(
                    parcellation_scheme,
                    tensor_type,
                    session,
                    parcellation_type,
                    measure,
                    force,
                )
                tensor_data = pd.concat([tensor_data], keys=[tensor_type])
                session_data = pd.concat([session_data, tensor_data])
            data = pd.concat([data, session_data])
        # except (TypeError, FileNotFoundError):
        #     warnings.warn(
        #         f"Encountered an error when trying to parcellate subject {participant_label}'s data..."  # noqa
        #     )
        return data
