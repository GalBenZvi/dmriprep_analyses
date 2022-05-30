import logging
from pathlib import Path
from typing import Union

from analyses_utils.entities.derivatives.dmriprep import DmriprepDerivatives
from analyses_utils.entities.participant import Participant

from dmriprep_analyses.utils.messages import BASE_DIR_AND_PARTICIPANT_REQUIRED
from dmriprep_analyses.utils.messages import MUTUALLY_EXCLUSIVE

SIMPLE_LOGGING_FORMAT = "%(name)s - %(levelname)s\n\t%(message)s"


def validate_instantiation(
    derivatives: DmriprepDerivatives = None,
    base_dir: Union[Path, str] = None,
    sessions_base: str = None,
    participant_label: str = None,
):
    """
    Validates the instansitation of *DmriprepAnalyses* class.
    *participant_label* and *derivatives* are mutually exclusive.
    """
    if participant_label and derivatives:
        raise ValueError(
            MUTUALLY_EXCLUSIVE.format(
                in1="participant_label", in2="derivatives"
            )
        )
    if not derivatives:
        if not (base_dir and participant_label):
            raise ValueError(BASE_DIR_AND_PARTICIPANT_REQUIRED)
        return DmriprepDerivatives(
            Participant(
                label=participant_label,
                base_dir=base_dir,
                sessions_base=sessions_base,
            )
        )
    return derivatives


def get_console_handler() -> logging.StreamHandler:
    """
    Returns a console handler for logging.
    """
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(SIMPLE_LOGGING_FORMAT))
    return console_handler


def apply_bids_filters(original: dict, replacements: dict) -> dict:
    """
    Change an *original* bids-filters' query according to *replacements*

    Parameters
    ----------
    original : dict
        Original filters
    replacements : dict
        Replacement entities

    Returns
    -------
    dict
        Combined entities for bids query
    """
    combined_filters = original.copy()
    if isinstance(replacements, dict):
        for key, value in replacements.items():
            combined_filters[key] = value
    return combined_filters
