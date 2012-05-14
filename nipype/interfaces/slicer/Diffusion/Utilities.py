from nipype.interfaces.base import CommandLine, CommandLineInputSpec, TraitedSpec, File, Directory, traits, isdefined, InputMultiPath, OutputMultiPath
import os
from nipype.interfaces.slicer.base import SlicerCommandLine


class ResampleDTIInputSpec(CommandLineInputSpec):
    inputVolume = File(position="0", desc="Input volume to be resampled", exists=True, argstr="--inputVolume %s")
    outputVolume = traits.Either(traits.Bool, File(), position="1", hash_files=False, desc="Resampled Volume", argstr="--outputVolume %s")
    Reference = File(desc="Reference Volume (spacing,size,orientation,origin)", exists=True, argstr="--Reference %s")
    transformationFile = File(exists=True, argstr="--transformationFile %s")
    defField = File(desc="File containing the deformation field (3D vector image containing vectors with 3 components)", exists=True, argstr="--defField %s")
    hfieldtype = traits.Enum("displacement", "h-Field", desc="Set if the deformation field is an -Field", argstr="--hfieldtype %s")
    interpolation = traits.Enum("linear", "nn", "ws", "bs", desc="Sampling algorithm (linear , nn (nearest neighborhoor), ws (WindowedSinc), bs (BSpline) )", argstr="--interpolation %s")
    correction = traits.Enum("zero", "none", "abs", "nearest", desc="Correct the tensors if computed tensor is not semi-definite positive", argstr="--correction %s")
    transform_tensor_method = traits.Enum("PPD", "FS", desc="Chooses between 2 methods to transform the tensors: Finite Strain (FS), faster but less accurate, or Preservation of the Principal Direction (PPD)", argstr="--transform_tensor_method %s")
    transform_order = traits.Enum("input-to-output", "output-to-input", desc="Select in what order the transforms are read", argstr="--transform_order %s")
    notbulk = traits.Bool(desc="The transform following the BSpline transform is not set as a bulk transform for the BSpline transform", argstr="--notbulk ")
    spaceChange = traits.Bool(desc="Space Orientation between transform and image is different (RAS/LPS) (warning: if the transform is a Transform Node in Slicer3, do not select)", argstr="--spaceChange ")
    rotation_point = traits.List(desc="Center of rotation (only for rigid and affine transforms)", argstr="--rotation_point %s")
    centered_transform = traits.Bool(desc="Set the center of the transformation to the center of the input image (only for rigid and affine transforms)", argstr="--centered_transform ")
    image_center = traits.Enum("input", "output", desc="Image to use to center the transform (used only if \"Centered Transform\" is selected)", argstr="--image_center %s")
    Inverse_ITK_Transformation = traits.Bool(desc="Inverse the transformation before applying it from output image to input image (only for rigid and affine transforms)", argstr="--Inverse_ITK_Transformation ")
    spacing = InputMultiPath(traits.Float, desc="Spacing along each dimension (0 means use input spacing)", sep=",", argstr="--spacing %s")
    size = InputMultiPath(traits.Float, desc="Size along each dimension (0 means use input size)", sep=",", argstr="--size %s")
    origin = traits.List(desc="Origin of the output Image", argstr="--origin %s")
    direction_matrix = InputMultiPath(traits.Float, desc="9 parameters of the direction matrix by rows (ijk to LPS if LPS transform, ijk to RAS if RAS transform)", sep=",", argstr="--direction_matrix %s")
    number_of_thread = traits.Int(desc="Number of thread used to compute the output image", argstr="--number_of_thread %d")
    default_pixel_value = traits.Float(desc="Default pixel value for samples falling outside of the input region", argstr="--default_pixel_value %f")
    window_function = traits.Enum("h", "c", "w", "l", "b", desc="Window Function , h = Hamming , c = Cosine , w = Welch , l = Lanczos , b = Blackman", argstr="--window_function %s")
    spline_order = traits.Int(desc="Spline Order (Spline order may be from 0 to 5)", argstr="--spline_order %d")
    transform_matrix = InputMultiPath(traits.Float, desc="12 parameters of the transform matrix by rows ( --last 3 being translation-- )", sep=",", argstr="--transform_matrix %s")
    transform = traits.Enum("rt", "a", desc="Transform algorithm, rt = Rigid Transform, a = Affine Transform", argstr="--transform %s")


class ResampleDTIOutputSpec(TraitedSpec):
    outputVolume = File(position="1", desc="Resampled Volume", exists=True)


class ResampleDTI(SlicerCommandLine):
    """title: Resample DTI Volume

category: Diffusion.Utilities

description: 
Resampling an image is a very important task in image analysis. It is especially important in the frame of image registration. This module implements DT image resampling through the use of itk Transforms. The resampling is controlled by the Output Spacing. "Resampling" is performed in space coordinates, not pixel/grid coordinates. It is quite important to ensure that image spacing is properly set on the images involved. The interpolator is required since the mapping from one space to the other will often require evaluation of the intensity of the image at non-grid positions.


version: 0.1

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.0/Modules/ResampleDTI

contributor: Francois Budin

acknowledgements: 
This work is part of the National Alliance for Medical Image Computing (NAMIC), funded by the National Institutes of Health through the NIH Roadmap for Medical Research, Grant U54 EB005149. Information on the National Centers for Biomedical Computing can be obtained from http://nihroadmap.nih.gov/bioinformatics


"""

    input_spec = ResampleDTIInputSpec
    output_spec = ResampleDTIOutputSpec
    _cmd = " ResampleDTI "
    _outputs_filenames = {'outputVolume':'outputVolume.nii'}


class DiffusionTensorEstimationInputSpec(CommandLineInputSpec):
    inputVolume = File(position="0", desc="Input DWI volume", exists=True, argstr="--inputVolume %s")
    mask = File(desc="Mask where the tensors will be computed", exists=True, argstr="--mask %s")
    outputTensor = traits.Either(traits.Bool, File(), position="1", hash_files=False, desc="Estimated DTI volume", argstr="--outputTensor %s")
    outputBaseline = traits.Either(traits.Bool, File(), position="2", hash_files=False, desc="Estimated baseline volume", argstr="--outputBaseline %s")
    enumeration = traits.Enum("LS", "WLS", desc="LS: Least Squares, WLS: Weighted Least Squares", argstr="--enumeration %s")
    shiftNeg = traits.Bool(desc="Shift eigenvalues so all are positive (accounts for bad tensors related to noise or acquisition error)", argstr="--shiftNeg ")


class DiffusionTensorEstimationOutputSpec(TraitedSpec):
    outputTensor = File(position="1", desc="Estimated DTI volume", exists=True)
    outputBaseline = File(position="2", desc="Estimated baseline volume", exists=True)


class DiffusionTensorEstimation(SlicerCommandLine):
    """title: 
  Diffusion Tensor Estimation
  

category: 
  Diffusion.Utilities
  

description: 
  Performs a tensor model estimation from diffusion weighted images. 

There are three estimation methods available: least squares, weigthed least squares and non-linear estimation. The first method is the traditional method for tensor estimation and the fastest one. Weighted least squares takes into account the noise characteristics of the MRI images to weight the DWI samples used in the estimation based on its intensity magnitude. The last method is the more complex.
  

version: 0.1.0.$Revision: 1892 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.0/Modules/DiffusionTensorEstimation

license: slicer3

contributor: Raul San Jose

acknowledgements: This command module is based on the estimation functionality provided by the Teem library. This work is part of the National Alliance for Medical Image Computing (NAMIC), funded by the National Institutes of Health through the NIH Roadmap for Medical Research, Grant U54 EB005149. 

"""

    input_spec = DiffusionTensorEstimationInputSpec
    output_spec = DiffusionTensorEstimationOutputSpec
    _cmd = " DiffusionTensorEstimation "
    _outputs_filenames = {'outputTensor':'outputTensor.nii','outputBaseline':'outputBaseline.nii'}


class DiffusionWeightedMaskingInputSpec(CommandLineInputSpec):
    inputVolume = File(position="0", desc="Input DWI volume", exists=True, argstr="--inputVolume %s")
    outputBaseline = traits.Either(traits.Bool, File(), position="2", hash_files=False, desc="Estimated baseline volume", argstr="--outputBaseline %s")
    thresholdMask = traits.Either(traits.Bool, File(), position="3", hash_files=False, desc="Otsu Threshold Mask", argstr="--thresholdMask %s")
    otsuomegathreshold = traits.Float(desc="Control the sharpness of the threshold in the Otsu computation. 0: lower threshold, 1: higher threhold", argstr="--otsuomegathreshold %f")
    removeislands = traits.Bool(desc="Remove Islands in Threshold Mask?", argstr="--removeislands ")


class DiffusionWeightedMaskingOutputSpec(TraitedSpec):
    outputBaseline = File(position="2", desc="Estimated baseline volume", exists=True)
    thresholdMask = File(position="3", desc="Otsu Threshold Mask", exists=True)


class DiffusionWeightedMasking(SlicerCommandLine):
    """title: 
  Mask from Diffusion Weighted Images
  

category: 
  Diffusion.Utilities
  

description: <p>Performs a mask calculation from a diffusion weighted (DW) image.</p><p>Starting from a dw image, this module computes the baseline image averaging all the images without diffusion weighting and then applies the otsu segmentation algorithm in order to produce a mask. this mask can then be used when estimating the diffusion tensor (dt) image, not to estimate tensors all over the volume.</p>

version: 0.1.0.$Revision: 1892 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.0/Modules/DiffusionWeightedMasking

license: slicer3

contributor: Demian Wassermann

"""

    input_spec = DiffusionWeightedMaskingInputSpec
    output_spec = DiffusionWeightedMaskingOutputSpec
    _cmd = " DiffusionWeightedMasking "
    _outputs_filenames = {'outputBaseline':'outputBaseline.nii','thresholdMask':'thresholdMask.nii'}


class DiffusionTensorMathematicsInputSpec(CommandLineInputSpec):
    inputVolume = File(position="0", desc="Input DTI volume", exists=True, argstr="--inputVolume %s")
    outputScalar = traits.Either(traits.Bool, File(), position="2", hash_files=False, desc="Scalar volume derived from tensor", argstr="--outputScalar %s")
    enumeration = traits.Enum("Trace", "Determinant", "RelativeAnisotropy", "FractionalAnisotropy", "Mode", "LinearMeasure", "PlanarMeasure", "SphericalMeasure", "MinEigenvalue", "MidEigenvalue", "MaxEigenvalue", "MaxEigenvalueProjectionX", "MaxEigenvalueProjectionY", "MaxEigenvalueProjectionZ", "RAIMaxEigenvecX", "RAIMaxEigenvecY", "RAIMaxEigenvecZ", "D11", "D22", "D33", "ParallelDiffusivity", "PerpendicularDffusivity", desc="An enumeration of strings", argstr="--enumeration %s")


class DiffusionTensorMathematicsOutputSpec(TraitedSpec):
    outputScalar = File(position="2", desc="Scalar volume derived from tensor", exists=True)


class DiffusionTensorMathematics(SlicerCommandLine):
    """title: 
  Diffusion Tensor Scalar Measurements
  

category: 
  Diffusion.Utilities
  

description: 
  Compute a set of different scalar measurements from a tensor field, specially oriented for Diffusion Tensors where some rotationally invariant measurements, like Fractional Anisotropy, are highly used to describe the anistropic behaviour of the tensor.
  

version: 0.1.0.$Revision: 1892 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.0/Modules/DiffusionTensorMathematics

contributor: Raul San Jose

acknowledgements: LMI

"""

    input_spec = DiffusionTensorMathematicsInputSpec
    output_spec = DiffusionTensorMathematicsOutputSpec
    _cmd = " DiffusionTensorMathematics "
    _outputs_filenames = {'outputScalar':'outputScalar.nii'}
