import os


class ReconstDtiFlow:
    """
    Class for tensor reconstruction based on the diffusion tensor model.
    """

    DWI2TENSOR_TEMPLATE = "dwi2tensor"
    TENSOR2METRICS_TEMPLATE = "tensor2metric"

    def run(
        self,
        in_file: str,
        bvectors: str,
        bvalues: str,
        mask_file: str,
        out_adc: str,
        out_fa: str,
        out_ad: str,
        out_rd: str,
        out_cl: str,
        out_cp: str,
        out_cs: str,
        out_evec: str,
        out_eval: str,
        out_tensor: str,
    ):
        """
        Initialize the class.
        """
        self.dwi2tensor(in_file, bvectors, bvalues, mask_file, out_tensor)
        self.tensor2metrics(
            out_tensor,
            out_adc,
            out_fa,
            out_ad,
            out_rd,
            out_cl,
            out_cp,
            out_cs,
            out_evec,
            out_eval,
        )

    def dwi2tensor(self, in_file, bvectors, bvalues, mask_file, out_file):
        """
        Run dwi2tensor.
        """
        cmd = f"{self.DWI2TENSOR_TEMPLATE} -mask {mask_file} -fslgrad {bvectors} {bvalues} {in_file} {out_file}"  # noqa
        os.system(cmd)

    def tensor2metrics(
        self,
        tensor: str,
        out_adc: str,
        out_fa: str,
        out_ad: str,
        out_rd: str,
        out_cl: str,
        out_cp: str,
        out_cs: str,
        out_evec: str,
        out_eval: str,
    ):
        """
        Run tensor2metric.
        """
        cmd = f"{self.TENSOR2METRICS_TEMPLATE} -adc {out_adc} -fa {out_fa} -ad {out_ad} -rd {out_rd} -cl {out_cl} -cp {out_cp} -cs {out_cs} -vector {out_evec} -value {out_eval} {tensor}"  # noqa
        os.system(cmd)
