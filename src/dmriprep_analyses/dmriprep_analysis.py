import datetime
from pathlib import Path
from typing import Union

from analyses_utils.entities.analysis.analysis import Analysis
from analyses_utils.entities.derivatives.dmriprep import DmriprepDerivatives

from dmriprep_analyses.utils.utils import validate_instantiation


class DmriprepAnalysis(Analysis):
    def __init__(
        self,
        derivatives: DmriprepDerivatives = None,
        base_dir: Union[Path, str] = None,
        participant_label: str = None,
        sessions_base: str = None,
    ) -> None:
        """
        Initializes the DmriprepAnalysis class.

        Parameters
        ----------
        derivatives : DmriprepDerivatives, optional
            An intansiated DmriprepDerivatives object , by default None
        base_dir : Union[Path, str], optional
            Base directory to be used for
            Participant object instansiation , by default None
        participant_label : str, optional
            Participant's label , by default None
        sessions_base : str, optional
            Where to look for available sessions
            under participant's label , by default None
        """
        derivatives = validate_instantiation(
            derivatives, base_dir, sessions_base, participant_label
        )
        super().__init__(derivatives)
        timestamp = datetime.datetime.today().strftime("%Y-%m-%d_%H%M%S")
        self.init_logger(
            name=self.LOGGER_FILE_FORMAT.format(
                name=__name__, timestamp=timestamp
            )
        )
