import shutil

from nipype.interfaces import fsl


class ReconstDtiFlow:
    """
    Class for tensor reconstruction based on the diffusion tensor model.
    """

    def run(
        self,
        dwi: str,
        bvecs: str,
        bvals: str,
        mask: str,
        out_fa: str,
        out_l1: str,
        out_l2: str,
        out_l3: str,
        out_md: str,
        out_mo: str,
        out_s0: str,
        out_v1: str,
        out_v2: str,
        out_v3: str,
    ):
        """
        Initialize the class.
        """

        dti = fsl.DTIFit(dwi=dwi, bvecs=bvecs, bvals=bvals, mask=mask)
        dti.run()
        outputs = dti.aggregate_outputs().__dict__
        for key, target in zip(
            ['V1', 'V2', 'V3', 'L1', 'L2', 'L3', 'MD', 'FA', 'MO', 'S0'],
            [
                out_v1,
                out_v2,
                out_v3,
                out_l1,
                out_l2,
                out_l3,
                out_md,
                out_fa,
                out_mo,
                out_s0,
            ],
        ):
            shutil.move(outputs.get(key), target)
