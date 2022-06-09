TENSOR_DERIVED_METRICS = dict(
    diffusion_tensor=dict(
        adc="md",
        fa="fa",
        ad="ad",
        rd="rd",
        cl="cl",
        cp="cp",
        cs="cs",
        evec="evecs",
        eval="evals",
        tensor="tensor",
    ),
)

KWARGS_MAPPING = dict(
    coreg_dwi_image="in_file",
    coreg_dwi_bval="bvalues",
    coreg_dwi_bvec="bvectors",
    coreg_dwi_brain_mask="mask_file",
)
