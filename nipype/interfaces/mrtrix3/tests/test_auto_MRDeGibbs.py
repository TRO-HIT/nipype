# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from ..preprocess import MRDeGibbs


def test_MRDeGibbs_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        axes=dict(
            argstr='-axes %s',
            maxlen=2,
            minlen=2,
            sep=',',
            usedefault=True,
        ),
        bval_scale=dict(argstr='-bvalue_scaling %s', ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        grad_file=dict(
            argstr='-grad %s',
            extensions=None,
            xor=['grad_fsl'],
        ),
        grad_fsl=dict(
            argstr='-fslgrad %s %s',
            xor=['grad_file'],
        ),
        in_bval=dict(extensions=None, ),
        in_bvec=dict(
            argstr='-fslgrad %s %s',
            extensions=None,
        ),
        in_file=dict(
            argstr='%s',
            extensions=None,
            mandatory=True,
            position=-2,
        ),
        maxW=dict(
            argstr='-maxW %d',
            usedefault=True,
        ),
        minW=dict(
            argstr='-minW %d',
            usedefault=True,
        ),
        nshifts=dict(
            argstr='-nshifts %d',
            usedefault=True,
        ),
        nthreads=dict(
            argstr='-nthreads %d',
            nohash=True,
        ),
        out_file=dict(
            argstr='%s',
            extensions=None,
            keep_extension=True,
            name_source='in_file',
            name_template='%s_unr',
            position=-1,
        ),
    )
    inputs = MRDeGibbs.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_MRDeGibbs_outputs():
    output_map = dict(out_file=dict(extensions=None, ), )
    outputs = MRDeGibbs.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value