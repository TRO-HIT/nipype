# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from ..epi import TOPUP


def test_TOPUP_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        config=dict(
            argstr='--config=%s',
            usedefault=True,
        ),
        encoding_direction=dict(
            argstr='--datain=%s',
            mandatory=True,
            requires=['readout_times'],
            xor=['encoding_file'],
        ),
        encoding_file=dict(
            argstr='--datain=%s',
            mandatory=True,
            xor=['encoding_direction'],
        ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        estmov=dict(argstr='--estmov=%d', ),
        fwhm=dict(argstr='--fwhm=%f', ),
        in_file=dict(
            argstr='--imain=%s',
            mandatory=True,
        ),
        interp=dict(argstr='--interp=%s', ),
        max_iter=dict(argstr='--miter=%d', ),
        minmet=dict(argstr='--minmet=%d', ),
        numprec=dict(argstr='--numprec=%s', ),
        out_base=dict(
            argstr='--out=%s',
            hash_files=False,
            name_source=['in_file'],
            name_template='%s_base',
        ),
        out_corrected=dict(
            argstr='--iout=%s',
            hash_files=False,
            name_source=['in_file'],
            name_template='%s_corrected',
        ),
        out_field=dict(
            argstr='--fout=%s',
            hash_files=False,
            name_source=['in_file'],
            name_template='%s_field',
        ),
        out_jac_prefix=dict(
            argstr='--jacout=%s',
            hash_files=False,
            usedefault=True,
        ),
        out_logfile=dict(
            argstr='--logout=%s',
            hash_files=False,
            keep_extension=True,
            name_source=['in_file'],
            name_template='%s_topup.log',
        ),
        out_mat_prefix=dict(
            argstr='--rbmout=%s',
            hash_files=False,
            usedefault=True,
        ),
        out_warp_prefix=dict(
            argstr='--dfout=%s',
            hash_files=False,
            usedefault=True,
        ),
        output_type=dict(),
        readout_times=dict(
            mandatory=True,
            requires=['encoding_direction'],
            xor=['encoding_file'],
        ),
        reg_lambda=dict(argstr='--lambda=%0.f', ),
        regmod=dict(argstr='--regmod=%s', ),
        regrid=dict(argstr='--regrid=%d', ),
        scale=dict(argstr='--scale=%d', ),
        splineorder=dict(argstr='--splineorder=%d', ),
        ssqlambda=dict(argstr='--ssqlambda=%d', ),
        subsamp=dict(argstr='--subsamp=%d', ),
        warp_res=dict(argstr='--warpres=%f', ),
    )
    inputs = TOPUP.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_TOPUP_outputs():
    output_map = dict(
        out_corrected=dict(),
        out_enc_file=dict(),
        out_field=dict(),
        out_fieldcoef=dict(),
        out_jacs=dict(),
        out_logfile=dict(),
        out_mats=dict(),
        out_movpar=dict(),
        out_warps=dict(),
    )
    outputs = TOPUP.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
