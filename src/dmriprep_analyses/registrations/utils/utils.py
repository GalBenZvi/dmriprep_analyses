QUERIES = dict(
    mni2native={
        "main_key": "subject_specific",
        "sub_key": "mni_to_native_transform",
    },
    native2mni={
        "main_key": "subject_specific",
        "sub_key": "native_to_mni_transform",
    },
    anat_reference={
        "main_key": "subject_specific",
        "sub_key": "native_T1w",
    },
    probseg={
        "main_key": "subject_specific",
        "sub_key": "native_gm",
    },
    dwi_reference={"sub_key": "coreg_dwi_image"},
    dwi2anat={"sub_key": "native_to_anat_transform"},
    anat2dwi={"sub_key": "anat_to_native_transform"},
)

#: anatomical registration kets
ANAT_REG_KEYS = ["mni2native", "anat_reference", "probseg"]
#: diffusion registration keys
DWI_REG_KEYS = ["dwi_reference", "dwi2anat", "anat2dwi"]
#: Naming
DEFAULT_PARCELLATION_NAMING = dict(suffix="dseg", desc="")

#: Types of transformations
TRANSFORMS = ["mni2native", "native2mni"]

#: Default probability segmentations' threshold
PROBSEG_THRESHOLD = 0.01
