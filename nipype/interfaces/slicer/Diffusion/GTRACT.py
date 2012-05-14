from nipype.interfaces.base import CommandLine, CommandLineInputSpec, TraitedSpec, File, Directory, traits, isdefined, InputMultiPath, OutputMultiPath
import os
from nipype.interfaces.slicer.base import SlicerCommandLine


class gtractResampleDWIInPlaceInputSpec(CommandLineInputSpec):
    inputVolume = File(desc="Required: input image is a 4D NRRD image.", exists=True, argstr="--inputVolume %s")
    inputTransform = File(desc="Required: transform file derived from rigid registration of b0 image to reference structural image.", exists=True, argstr="--inputTransform %s")
    debugLevel = traits.Int(desc="Display debug messages, and produce debug intermediate results.  0=OFF, 1=Minimal, 10=Maximum debugging.", argstr="--debugLevel %d")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Required: output image (NRRD file) that has been transformed into the space of the structural image.", argstr="--outputVolume %s")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class gtractResampleDWIInPlaceOutputSpec(TraitedSpec):
    outputVolume = File(desc="Required: output image (NRRD file) that has been transformed into the space of the structural image.", exists=True)


class gtractResampleDWIInPlace(SlicerCommandLine):
    """title: Resample DWI In Place

category: Diffusion.GTRACT

description: Resamples DWI image to structural image.

version: 4.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:GTRACT

license: http://mri.radiology.uiowa.edu/copyright/GTRACT-Copyright.txt

contributor: This tool was developed by Vincent Magnotta and Greg Harris.

acknowledgements: Funding for this version of the GTRACT program was provided by NIH/NINDS R01NS050568-01A2S1

"""

    input_spec = gtractResampleDWIInPlaceInputSpec
    output_spec = gtractResampleDWIInPlaceOutputSpec
    _cmd = " gtractResampleDWIInPlace "
    _outputs_filenames = {'outputVolume':'outputVolume.nii'}


class gtractCopyImageOrientationInputSpec(CommandLineInputSpec):
    inputVolume = File(desc="Required: input file containing the signed short image to reorient without resampling.", exists=True, argstr="--inputVolume %s")
    inputReferenceVolume = File(desc="Required: input file containing orietation that will be cloned.", exists=True, argstr="--inputReferenceVolume %s")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Required: name of output NRRD or Nifti file containing the reoriented image in reference image space.", argstr="--outputVolume %s")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class gtractCopyImageOrientationOutputSpec(TraitedSpec):
    outputVolume = File(desc="Required: name of output NRRD or Nifti file containing the reoriented image in reference image space.", exists=True)


class gtractCopyImageOrientation(SlicerCommandLine):
    """title: Copy Image Orientation

category: Diffusion.GTRACT

description: This program will copy the orientation from the reference image into the moving image. Currently, the registration process requires that the diffusion weighted images and the anatomical images have the same image orientation (i.e. Axial, Coronal, Sagittal). It is suggested that you copy the image orientation from the diffusion weighted images and apply this to the anatomical image. This image can be subsequently removed after the registration step is complete. We anticipate that this limitation will be removed in future versions of the registration programs.

version: 4.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:GTRACT

license: http://mri.radiology.uiowa.edu/copyright/GTRACT-Copyright.txt

contributor: This tool was developed by Vincent Magnotta and Greg Harris.

acknowledgements: Funding for this version of the GTRACT program was provided by NIH/NINDS R01NS050568-01A2S1

"""

    input_spec = gtractCopyImageOrientationInputSpec
    output_spec = gtractCopyImageOrientationOutputSpec
    _cmd = " gtractCopyImageOrientation "
    _outputs_filenames = {'outputVolume':'outputVolume.nrrd'}


class gtractCostFastMarchingInputSpec(CommandLineInputSpec):
    inputTensorVolume = File(desc="Required: input tensor image file name", exists=True, argstr="--inputTensorVolume %s")
    inputAnisotropyVolume = File(desc="Required: input anisotropy image file name", exists=True, argstr="--inputAnisotropyVolume %s")
    inputStartingSeedsLabelMapVolume = File(desc="Required: input starting seeds LabelMap image file name", exists=True, argstr="--inputStartingSeedsLabelMapVolume %s")
    startingSeedsLabel = traits.Int(desc="Label value for Starting Seeds", argstr="--startingSeedsLabel %d")
    outputCostVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Output vcl_cost image", argstr="--outputCostVolume %s")
    outputSpeedVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Output speed image", argstr="--outputSpeedVolume %s")
    anisotropyWeight = traits.Float(desc="Anisotropy weight used for vcl_cost function calculations", argstr="--anisotropyWeight %f")
    stoppingValue = traits.Float(desc="Terminiating value for vcl_cost function estimation", argstr="--stoppingValue %f")
    seedThreshold = traits.Float(desc="Anisotropy threshold used for seed selection", argstr="--seedThreshold %f")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class gtractCostFastMarchingOutputSpec(TraitedSpec):
    outputCostVolume = File(desc="Output vcl_cost image", exists=True)
    outputSpeedVolume = File(desc="Output speed image", exists=True)


class gtractCostFastMarching(SlicerCommandLine):
    """title: Cost Fast Marching

category: Diffusion.GTRACT

description:  This program will use a fast marching fiber tracking algorithm to identify fiber tracts from a tensor image. This program is the first portion of the algorithm. The user must first run gtractFastMarchingTracking to generate the actual fiber tracts.  This algorithm is roughly based on the work by G. Parker et al. from IEEE Transactions On Medical Imaging, 21(5): 505-512, 2002. An additional feature of including anisotropy into the vcl_cost function calculation is included.  

version: 4.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:GTRACT

license: http://mri.radiology.uiowa.edu/copyright/GTRACT-Copyright.txt

contributor: This tool was developed by Vincent Magnotta and Greg Harris. The original code here was developed by Daisy Espino.

acknowledgements: Funding for this version of the GTRACT program was provided by NIH/NINDS R01NS050568-01A2S1

"""

    input_spec = gtractCostFastMarchingInputSpec
    output_spec = gtractCostFastMarchingOutputSpec
    _cmd = " gtractCostFastMarching "
    _outputs_filenames = {'outputCostVolume':'outputCostVolume.nrrd','outputSpeedVolume':'outputSpeedVolume.nrrd'}


class gtractCoRegAnatomyInputSpec(CommandLineInputSpec):
    inputVolume = File(desc="Required: input vector image file name. It is recommended that the input volume is the skull stripped baseline image of the DWI scan.", exists=True, argstr="--inputVolume %s")
    inputAnatomicalVolume = File(desc="Required: input anatomical image file name. It is recommended that that the input anatomical image has been skull stripped and has the same orientation as the DWI scan.", exists=True, argstr="--inputAnatomicalVolume %s")
    vectorIndex = traits.Int(desc="Vector image index in the moving image (within the DWI) to be used for registration.", argstr="--vectorIndex %d")
    inputRigidTransform = File(desc="Required (for B-Spline type co-registration): input rigid transform file name. Used as a starting point for the anatomical B-Spline registration.", exists=True, argstr="--inputRigidTransform %s")
    outputTransformName = traits.Either(traits.Bool, File(), hash_files=False, desc="Required: filename for the  fit transform.", argstr="--outputTransformName %s")
    transformType = traits.Enum("Rigid", "Bspline", desc="Transform Type: Rigid|Bspline", argstr="--transformType %s")
    numberOfIterations = traits.Int(desc="Number of iterations in the selected 3D fit", argstr="--numberOfIterations %d")
    gridSize = InputMultiPath(traits.Int, desc="Number of grid subdivisions in all 3 directions", sep=",", argstr="--gridSize %s")
    borderSize = traits.Int(desc="Size of border", argstr="--borderSize %d")
    numberOfHistogramBins = traits.Int(desc="Number of histogram bins", argstr="--numberOfHistogramBins %d")
    spatialScale = traits.Int(desc="Scales the number of voxels in the image by this value to specify the number of voxels used in the registration", argstr="--spatialScale %d")
    convergence = traits.Float(desc="Convergence Factor", argstr="--convergence %f")
    gradientTolerance = traits.Float(desc="Gradient Tolerance", argstr="--gradientTolerance %f")
    maxBSplineDisplacement = traits.Float(desc=" Sets the maximum allowed displacements in image physical coordinates for BSpline control grid along each axis.  A value of 0.0 indicates that the problem should be unbounded.  NOTE:  This only constrains the BSpline portion, and does not limit the displacement from the associated bulk transform.  This can lead to a substantial reduction in computation time in the BSpline optimizer.,       ", argstr="--maxBSplineDisplacement %f")
    maximumStepSize = traits.Float(desc="Maximum permitted step size to move in the selected 3D fit", argstr="--maximumStepSize %f")
    minimumStepSize = traits.Float(desc="Minimum required step size to move in the selected 3D fit without converging -- decrease this to make the fit more exacting", argstr="--minimumStepSize %f")
    translationScale = traits.Float(desc="How much to scale up changes in position compared to unit rotational changes in radians -- decrease this to put more translation in the fit", argstr="--translationScale %f")
    relaxationFactor = traits.Float(desc="Fraction of gradient from Jacobian to attempt to move in the selected 3D fit", argstr="--relaxationFactor %f")
    numberOfSamples = traits.Int(desc="Number of voxels sampled for mutual information computation in the selected 3D fit", argstr="--numberOfSamples %d")
    useMomentsAlign = traits.Bool(desc="MomentsAlign assumes that the center of mass of the images represent similar structures.  Perform a MomentsAlign registration as part of the sequential registration steps.   This option MUST come first, and CAN NOT be used with either CenterOfHeadLAlign, GeometryAlign, or initialTransform file.  This family of options superceeds the use of transformType if any of them are set.", argstr="--useMomentsAlign ")
    useGeometryAlign = traits.Bool(desc="GeometryAlign on assumes that the center of the voxel lattice of the images represent similar structures. Perform a GeometryCenterAlign registration as part of the sequential registration steps.   This option MUST come first, and CAN NOT be used with either MomentsAlign, CenterOfHeadAlign, or initialTransform file.  This family of options superceeds the use of transformType if any of them are set.", argstr="--useGeometryAlign ")
    useCenterOfHeadAlign = traits.Bool(desc="CenterOfHeadAlign attempts to find a hemisphere full of foreground voxels from the superior direction as an estimate of where the center of a head shape would be to drive a center of mass estimate.  Perform a CenterOfHeadAlign registration as part of the sequential registration steps.   This option MUST come first, and CAN NOT be used with either MomentsAlign, GeometryAlign, or initialTransform file.  This family of options superceeds the use of transformType if any of them are set.", argstr="--useCenterOfHeadAlign ")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class gtractCoRegAnatomyOutputSpec(TraitedSpec):
    outputTransformName = File(desc="Required: filename for the  fit transform.", exists=True)


class gtractCoRegAnatomy(SlicerCommandLine):
    """title: Coregister B0 to Anatomy B-Spline

category: Diffusion.GTRACT

description: This program will register a Nrrd diffusion weighted 4D vector image to a fixed anatomical image. Two registration methods are supported for alignment with anatomical images: Rigid and B-Spline. The rigid registration performs a rigid body registration with the anatomical images and should be done as well to initialize the B-Spline transform. The B-SPline transform is the deformable transform, where the user can control the amount of deformation based on the number of control points as well as the maximum distance that these points can move. The B-Spline registration places a low dimensional grid in the image, which is deformed. This allows for some susceptibility related distortions to be removed from the diffusion weighted images. In general the amount of motion in the slice selection and read-out directions direction should be kept low. The distortion is in the phase encoding direction in the images. It is recommended that skull stripped (i.e. image containing only brain with skull removed) images shoud be used for image co-registration with the B-Spline transform.

version: 4.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:GTRACT

license: http://mri.radiology.uiowa.edu/copyright/GTRACT-Copyright.txt

contributor: This tool was developed by Vincent Magnotta and Greg Harris.

acknowledgements: Funding for this version of the GTRACT program was provided by NIH/NINDS R01NS050568-01A2S1

"""

    input_spec = gtractCoRegAnatomyInputSpec
    output_spec = gtractCoRegAnatomyOutputSpec
    _cmd = " gtractCoRegAnatomy "
    _outputs_filenames = {'outputTransformName':'outputTransformName.mat'}


class gtractTransformToDeformationFieldInputSpec(CommandLineInputSpec):
    inputTransform = File(desc="Input Transform File Name", exists=True, argstr="--inputTransform %s")
    inputReferenceVolume = File(desc="Required: input image file name to exemplify the anatomical space over which to vcl_express the transform as a displacement field.", exists=True, argstr="--inputReferenceVolume %s")
    outputDeformationFieldVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Output deformation field", argstr="--outputDeformationFieldVolume %s")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class gtractTransformToDeformationFieldOutputSpec(TraitedSpec):
    outputDeformationFieldVolume = File(desc="Output deformation field", exists=True)


class gtractTransformToDeformationField(SlicerCommandLine):
    """title: Create Deformation Field

category: Diffusion.GTRACT

description: This program will compute forward deformation from the given Transform. The size of the DF is equal to MNI space

version: 4.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:GTRACT

license: http://mri.radiology.uiowa.edu/copyright/GTRACT-Copyright.txt

contributor: This tool was developed by Vincent Magnotta, Madhura Ingalhalikar, and Greg Harris 

acknowledgements: Funding for this version of the GTRACT program was provided by NIH/NINDS R01NS050568-01A2S1

"""

    input_spec = gtractTransformToDeformationFieldInputSpec
    output_spec = gtractTransformToDeformationFieldOutputSpec
    _cmd = " gtractTransformToDeformationField "
    _outputs_filenames = {'outputDeformationFieldVolume':'outputDeformationFieldVolume.nii'}


class gtractTensorInputSpec(CommandLineInputSpec):
    inputVolume = File(desc="Required: input image 4D NRRD image. Must contain data based on at least 6 distinct diffusion directions. The inputVolume is allowed to have multiple b0 and gradient direction images. Averaging of the b0 image is done internally in this step. Prior averaging of the DWIs is not required.", exists=True, argstr="--inputVolume %s")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Required: name of output NRRD file containing the Tensor vector image", argstr="--outputVolume %s")
    medianFilterSize = InputMultiPath(traits.Int, desc="Median filter radius in all 3 directions", sep=",", argstr="--medianFilterSize %s")
    maskProcessingMode = traits.Enum("NOMASK", "ROIAUTO", "ROI", desc="ROIAUTO:  mask is implicitly defined using a otsu forground and hole filling algorithm. ROI: Uses the masks to define what parts of the image should be used for computing the transform. NOMASK: no mask used", argstr="--maskProcessingMode %s")
    maskVolume = File(desc="Mask Image, if maskProcessingMode is ROI", exists=True, argstr="--maskVolume %s")
    backgroundSuppressingThreshold = traits.Int(desc="Image threshold to suppress background. This sets a threshold used on the b0 image to remove background voxels from processing. Typically, values of 100 and 500 work well for Siemens and GE DTI data, respectively. Check your data particularly in the globus pallidus to make sure the brain tissue is not being eliminated with this threshold.", argstr="--backgroundSuppressingThreshold %d")
    resampleIsotropic = traits.Bool(desc="Flag to resample to isotropic voxels. Enabling this feature is recommended if fiber tracking will be performed.", argstr="--resampleIsotropic ")
    size = traits.Float(desc="Isotropic voxel size to resample to", argstr="--size %f")
    b0Index = traits.Int(desc="Index in input vector index to extract", argstr="--b0Index %d")
    applyMeasurementFrame = traits.Bool(desc="Flag to apply the measurement frame to the gradient directions", argstr="--applyMeasurementFrame ")
    ignoreIndex = InputMultiPath(traits.Int, desc="Ignore diffusion gradient index. Used to remove specific gradient directions with artifacts.", sep=",", argstr="--ignoreIndex %s")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class gtractTensorOutputSpec(TraitedSpec):
    outputVolume = File(desc="Required: name of output NRRD file containing the Tensor vector image", exists=True)


class gtractTensor(SlicerCommandLine):
    """title: Tensor Estimation

category: Diffusion.GTRACT

description: This step will convert a b-value averaged diffusion tensor image to a 3x3 tensor voxel image. This step takes the diffusion tensor image data and generates a tensor representation of the data based on the signal intensity decay, b values applied, and the diffusion difrections. The apparent diffusion coefficient for a given orientation is computed on a pixel-by-pixel basis by fitting the image data (voxel intensities) to the Stejskal-Tanner equation. If at least 6 diffusion directions are used, then the diffusion tensor can be computed. This program uses itk::DiffusionTensor3DReconstructionImageFilter. The user can adjust background threshold, median filter, and isotropic resampling.

version: 4.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:GTRACT

license: http://mri.radiology.uiowa.edu/copyright/GTRACT-Copyright.txt

contributor: This tool was developed by Vincent Magnotta and Greg Harris.

acknowledgements: Funding for this version of the GTRACT program was provided by NIH/NINDS R01NS050568-01A2S1

"""

    input_spec = gtractTensorInputSpec
    output_spec = gtractTensorOutputSpec
    _cmd = " gtractTensor "
    _outputs_filenames = {'outputVolume':'outputVolume.nrrd'}


class extractNrrdVectorIndexInputSpec(CommandLineInputSpec):
    inputVolume = File(desc="Required: input file containing the vector that will be extracted", exists=True, argstr="--inputVolume %s")
    vectorIndex = traits.Int(desc="Index in the vector image to extract", argstr="--vectorIndex %d")
    setImageOrientation = traits.Enum("AsAcquired", "Axial", "Coronal", "Sagittal", desc="Sets the image orientation of the extracted vector (Axial, Coronal, Sagittal)", argstr="--setImageOrientation %s")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Required: name of output NRRD file containing the vector image at the given index", argstr="--outputVolume %s")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class extractNrrdVectorIndexOutputSpec(TraitedSpec):
    outputVolume = File(desc="Required: name of output NRRD file containing the vector image at the given index", exists=True)


class extractNrrdVectorIndex(SlicerCommandLine):
    """title: Extract Nrrd Index

category: Diffusion.GTRACT

description: This program will extract a 3D image (single vector) from a vector 3D image at a given vector index.

version: 4.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:GTRACT

license: http://mri.radiology.uiowa.edu/copyright/GTRACT-Copyright.txt

contributor: This tool was developed by Vincent Magnotta and Greg Harris.

acknowledgements: Funding for this version of the GTRACT program was provided by NIH/NINDS R01NS050568-01A2S1

"""

    input_spec = extractNrrdVectorIndexInputSpec
    output_spec = extractNrrdVectorIndexOutputSpec
    _cmd = " extractNrrdVectorIndex "
    _outputs_filenames = {'outputVolume':'outputVolume.nii'}


class gtractInvertBSplineTransformInputSpec(CommandLineInputSpec):
    inputReferenceVolume = File(desc="Required: input image file name to exemplify the anatomical space to interpolate over.", exists=True, argstr="--inputReferenceVolume %s")
    inputTransform = File(desc="Required: input B-Spline transform file name", exists=True, argstr="--inputTransform %s")
    outputTransform = traits.Either(traits.Bool, File(), hash_files=False, desc="Required: output transform file name", argstr="--outputTransform %s")
    landmarkDensity = InputMultiPath(traits.Int, desc="Number of landmark subdivisions in all 3 directions", sep=",", argstr="--landmarkDensity %s")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class gtractInvertBSplineTransformOutputSpec(TraitedSpec):
    outputTransform = File(desc="Required: output transform file name", exists=True)


class gtractInvertBSplineTransform(SlicerCommandLine):
    """title: B-Spline Transform Inversion

category: Diffusion.GTRACT

description: This program will invert a B-Spline transform using a thin-plate spline approximation.

version: 4.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:GTRACT

license: http://mri.radiology.uiowa.edu/copyright/GTRACT-Copyright.txt

contributor: This tool was developed by Vincent Magnotta and Greg Harris.

acknowledgements: Funding for this version of the GTRACT program was provided by NIH/NINDS R01NS050568-01A2S1

"""

    input_spec = gtractInvertBSplineTransformInputSpec
    output_spec = gtractInvertBSplineTransformOutputSpec
    _cmd = " gtractInvertBSplineTransform "
    _outputs_filenames = {'outputTransform':'outputTransform.mat'}


class gtractConcatDwiInputSpec(CommandLineInputSpec):
    inputVolume = InputMultiPath(File(exists=True), desc="Required: input file containing the first diffusion weighted image", argstr="--inputVolume %s...")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Required: name of output NRRD file containing the combined diffusion weighted images.", argstr="--outputVolume %s")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class gtractConcatDwiOutputSpec(TraitedSpec):
    outputVolume = File(desc="Required: name of output NRRD file containing the combined diffusion weighted images.", exists=True)


class gtractConcatDwi(SlicerCommandLine):
    """title: Concat DWI Images

category: Diffusion.GTRACT

description: This program will concatenate two DTI runs together.

version: 4.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:GTRACT

license: http://mri.radiology.uiowa.edu/copyright/GTRACT-Copyright.txt

contributor: This tool was developed by Vincent Magnotta and Greg Harris.

acknowledgements: Funding for this version of the GTRACT program was provided by NIH/NINDS R01NS050568-01A2S1

"""

    input_spec = gtractConcatDwiInputSpec
    output_spec = gtractConcatDwiOutputSpec
    _cmd = " gtractConcatDwi "
    _outputs_filenames = {'outputVolume':'outputVolume.nrrd'}


class gtractInvertDeformationFieldInputSpec(CommandLineInputSpec):
    baseImage = File(desc="Required: base image used to define the size of the inverse field", exists=True, argstr="--baseImage %s")
    deformationImage = File(desc="Required: Deformation field image", exists=True, argstr="--deformationImage %s")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Required: Output deformation field", argstr="--outputVolume %s")
    subsamplingFactor = traits.Int(desc="Subsampling factor for the deformation field", argstr="--subsamplingFactor %d")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class gtractInvertDeformationFieldOutputSpec(TraitedSpec):
    outputVolume = File(desc="Required: Output deformation field", exists=True)


class gtractInvertDeformationField(SlicerCommandLine):
    """title: Invert Deformation Field

category: Diffusion.GTRACT

description: This program will invert a deformatrion field. The size of the deformation field is defined by an example image provided by the user

version: 4.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:GTRACT

license: http://mri.radiology.uiowa.edu/copyright/GTRACT-Copyright.txt

contributor: This tool was developed by Vincent Magnotta.

acknowledgements: Funding for this version of the GTRACT program was provided by NIH/NINDS R01NS050568-01A2S1

"""

    input_spec = gtractInvertDeformationFieldInputSpec
    output_spec = gtractInvertDeformationFieldOutputSpec
    _cmd = " gtractInvertDeformationField "
    _outputs_filenames = {'outputVolume':'outputVolume.nrrd'}


class gtractAverageBvaluesInputSpec(CommandLineInputSpec):
    inputVolume = File(desc="Required: input image file name containing multiple baseline gradients to average", exists=True, argstr="--inputVolume %s")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Required: name of output NRRD file containing directly averaged baseline images", argstr="--outputVolume %s")
    directionsTolerance = traits.Float(desc="Tolerance for matching identical gradient direction pairs", argstr="--directionsTolerance %f")
    averageB0only = traits.Bool(desc="Average only baseline gradients. All other gradient directions are not averaged, but retained in the outputVolume", argstr="--averageB0only ")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class gtractAverageBvaluesOutputSpec(TraitedSpec):
    outputVolume = File(desc="Required: name of output NRRD file containing directly averaged baseline images", exists=True)


class gtractAverageBvalues(SlicerCommandLine):
    """title: Average B-Values

category: Diffusion.GTRACT

description: This program will directly average together the baseline gradients (b value equals 0) within a DWI scan. This is usually used after gtractCoregBvalues.

version: 4.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:GTRACT

license: http://mri.radiology.uiowa.edu/copyright/GTRACT-Copyright.txt

contributor: This tool was developed by Vincent Magnotta and Greg Harris.

acknowledgements: Funding for this version of the GTRACT program was provided by NIH/NINDS R01NS050568-01A2S1

"""

    input_spec = gtractAverageBvaluesInputSpec
    output_spec = gtractAverageBvaluesOutputSpec
    _cmd = " gtractAverageBvalues "
    _outputs_filenames = {'outputVolume':'outputVolume.nrrd'}


class gtractClipAnisotropyInputSpec(CommandLineInputSpec):
    inputVolume = File(desc="Required: input image file name", exists=True, argstr="--inputVolume %s")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Required: name of output NRRD file containing the clipped anisotropy image", argstr="--outputVolume %s")
    clipFirstSlice = traits.Bool(desc="Clip the first slice of the anisotropy image", argstr="--clipFirstSlice ")
    clipLastSlice = traits.Bool(desc="Clip the last slice of the anisotropy image", argstr="--clipLastSlice ")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class gtractClipAnisotropyOutputSpec(TraitedSpec):
    outputVolume = File(desc="Required: name of output NRRD file containing the clipped anisotropy image", exists=True)


class gtractClipAnisotropy(SlicerCommandLine):
    """title: Clip Anisotropy

category: Diffusion.GTRACT

description: This program will zero the first and/or last slice of an anisotropy image, creating a clipped anisotropy image.

version: 4.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:GTRACT

license: http://mri.radiology.uiowa.edu/copyright/GTRACT-Copyright.txt

contributor: This tool was developed by Vincent Magnotta and Greg Harris.

acknowledgements: Funding for this version of the GTRACT program was provided by NIH/NINDS R01NS050568-01A2S1

"""

    input_spec = gtractClipAnisotropyInputSpec
    output_spec = gtractClipAnisotropyOutputSpec
    _cmd = " gtractClipAnisotropy "
    _outputs_filenames = {'outputVolume':'outputVolume.nrrd'}


class gtractResampleAnisotropyInputSpec(CommandLineInputSpec):
    inputAnisotropyVolume = File(desc="Required: input file containing the anisotropy image", exists=True, argstr="--inputAnisotropyVolume %s")
    inputAnatomicalVolume = File(desc="Required: input file containing the anatomical image whose characteristics will be cloned.", exists=True, argstr="--inputAnatomicalVolume %s")
    inputTransform = File(desc="Required: input Rigid OR Bspline transform file name", exists=True, argstr="--inputTransform %s")
    transformType = traits.Enum("Rigid", "B-Spline", desc="Transform type: Rigid, B-Spline", argstr="--transformType %s")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Required: name of output NRRD file containing the resampled transformed anisotropy image.", argstr="--outputVolume %s")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class gtractResampleAnisotropyOutputSpec(TraitedSpec):
    outputVolume = File(desc="Required: name of output NRRD file containing the resampled transformed anisotropy image.", exists=True)


class gtractResampleAnisotropy(SlicerCommandLine):
    """title: Resample Anisotropy

category: Diffusion.GTRACT

description: This program will resample a floating point image using either the Rigid or B-Spline transform. You may want to save the aligned B0 image after each of the anisotropy map co-registration steps with the anatomical image to check the registration quality with another tool.

version: 4.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:GTRACT

license: http://mri.radiology.uiowa.edu/copyright/GTRACT-Copyright.txt

contributor: This tool was developed by Vincent Magnotta and Greg Harris.

acknowledgements: Funding for this version of the GTRACT program was provided by NIH/NINDS R01NS050568-01A2S1

"""

    input_spec = gtractResampleAnisotropyInputSpec
    output_spec = gtractResampleAnisotropyOutputSpec
    _cmd = " gtractResampleAnisotropy "
    _outputs_filenames = {'outputVolume':'outputVolume.nrrd'}


class gtractAnisotropyMapInputSpec(CommandLineInputSpec):
    inputTensorVolume = File(desc="Required: input file containing the diffusion tensor image", exists=True, argstr="--inputTensorVolume %s")
    anisotropyType = traits.Enum("ADC", "FA", "RA", "VR", "AD", "RD", "LI", desc="Anisotropy Mapping Type: ADC, FA, RA, VR, AD, RD, LI", argstr="--anisotropyType %s")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Required: name of output NRRD file containing the selected kind of anisotropy scalar.", argstr="--outputVolume %s")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class gtractAnisotropyMapOutputSpec(TraitedSpec):
    outputVolume = File(desc="Required: name of output NRRD file containing the selected kind of anisotropy scalar.", exists=True)


class gtractAnisotropyMap(SlicerCommandLine):
    """title: Anisotropy Map

category: Diffusion.GTRACT

description: This program will generate a scalar map of anisotropy, given a tensor representation. Anisotropy images are used for fiber tracking, but the anisotropy scalars are not defined along the path. Instead, the tensor representation is included as point data allowing all of these metrics to be computed using only the fiber tract point data. The images can be saved in any ITK supported format, but it is suggested that you use an image format that supports the definition of the image origin. This includes NRRD, NifTI, and Meta formats. These images can also be used for scalar analysis including regional anisotropy measures or VBM style analysis.

version: 4.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:GTRACT

license: http://mri.radiology.uiowa.edu/copyright/GTRACT-Copyright.txt

contributor: This tool was developed by Vincent Magnotta and Greg Harris.

acknowledgements: Funding for this version of the GTRACT program was provided by NIH/NINDS R01NS050568-01A2S1

"""

    input_spec = gtractAnisotropyMapInputSpec
    output_spec = gtractAnisotropyMapOutputSpec
    _cmd = " gtractAnisotropyMap "
    _outputs_filenames = {'outputVolume':'outputVolume.nrrd'}


class gtractInvertRigidTransformInputSpec(CommandLineInputSpec):
    inputTransform = File(desc="Required: input rigid transform file name", exists=True, argstr="--inputTransform %s")
    outputTransform = traits.Either(traits.Bool, File(), hash_files=False, desc="Required: output transform file name", argstr="--outputTransform %s")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class gtractInvertRigidTransformOutputSpec(TraitedSpec):
    outputTransform = File(desc="Required: output transform file name", exists=True)


class gtractInvertRigidTransform(SlicerCommandLine):
    """title: Rigid Transform Inversion

category: Diffusion.GTRACT

description: This program will invert a Rigid transform.

version: 4.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:GTRACT

license: http://mri.radiology.uiowa.edu/copyright/GTRACT-Copyright.txt

contributor: This tool was developed by Vincent Magnotta and Greg Harris.

acknowledgements: Funding for this version of the GTRACT program was provided by NIH/NINDS R01NS050568-01A2S1

"""

    input_spec = gtractInvertRigidTransformInputSpec
    output_spec = gtractInvertRigidTransformOutputSpec
    _cmd = " gtractInvertRigidTransform "
    _outputs_filenames = {'outputTransform':'outputTransform.mat'}


class gtractResampleCodeImageInputSpec(CommandLineInputSpec):
    inputCodeVolume = File(desc="Required: input file containing the code image", exists=True, argstr="--inputCodeVolume %s")
    inputReferenceVolume = File(desc="Required: input file containing the standard image to clone the characteristics of.", exists=True, argstr="--inputReferenceVolume %s")
    inputTransform = File(desc="Required: input Rigid or Inverse-B-Spline transform file name", exists=True, argstr="--inputTransform %s")
    transformType = traits.Enum("Rigid", "Affine", "B-Spline", "Inverse-B-Spline", "None", desc="Transform type: Rigid or Inverse-B-Spline", argstr="--transformType %s")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Required: name of output NRRD file containing the resampled code image in acquisition space.", argstr="--outputVolume %s")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class gtractResampleCodeImageOutputSpec(TraitedSpec):
    outputVolume = File(desc="Required: name of output NRRD file containing the resampled code image in acquisition space.", exists=True)


class gtractResampleCodeImage(SlicerCommandLine):
    """title: Resample Code Image

category: Diffusion.GTRACT

description: This program will resample a short integer code image using either the Rigid or Inverse-B-Spline transform.  The reference image is the DTI tensor anisotropy image space, and the input code image is in anatomical space.

version: 4.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:GTRACT

license: http://mri.radiology.uiowa.edu/copyright/GTRACT-Copyright.txt

contributor: This tool was developed by Vincent Magnotta and Greg Harris.

acknowledgements: Funding for this version of the GTRACT program was provided by NIH/NINDS R01NS050568-01A2S1

"""

    input_spec = gtractResampleCodeImageInputSpec
    output_spec = gtractResampleCodeImageOutputSpec
    _cmd = " gtractResampleCodeImage "
    _outputs_filenames = {'outputVolume':'outputVolume.nrrd'}


class gtractResampleB0InputSpec(CommandLineInputSpec):
    inputVolume = File(desc="Required: input file containing the 4D image", exists=True, argstr="--inputVolume %s")
    inputAnatomicalVolume = File(desc="Required: input file containing the anatomical image defining the origin, spacing and size of the resampled image (template)", exists=True, argstr="--inputAnatomicalVolume %s")
    inputTransform = File(desc="Required: input Rigid OR Bspline transform file name", exists=True, argstr="--inputTransform %s")
    vectorIndex = traits.Int(desc="Index in the diffusion weighted image set for the B0 image", argstr="--vectorIndex %d")
    transformType = traits.Enum("Rigid", "B-Spline", desc="Transform type: Rigid, B-Spline", argstr="--transformType %s")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Required: name of output NRRD file containing the resampled input image.", argstr="--outputVolume %s")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class gtractResampleB0OutputSpec(TraitedSpec):
    outputVolume = File(desc="Required: name of output NRRD file containing the resampled input image.", exists=True)


class gtractResampleB0(SlicerCommandLine):
    """title: Resample B0

category: Diffusion.GTRACT

description: This program will resample a signed short image using either a Rigid or B-Spline transform. The user must specify a template image that will be used to define the origin, orientation, spacing, and size of the resampled image.

version: 4.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:GTRACT

license: http://mri.radiology.uiowa.edu/copyright/GTRACT-Copyright.txt

contributor: This tool was developed by Vincent Magnotta and Greg Harris.

acknowledgements: Funding for this version of the GTRACT program was provided by NIH/NINDS R01NS050568-01A2S1

"""

    input_spec = gtractResampleB0InputSpec
    output_spec = gtractResampleB0OutputSpec
    _cmd = " gtractResampleB0 "
    _outputs_filenames = {'outputVolume':'outputVolume.nrrd'}


class gtractImageConformityInputSpec(CommandLineInputSpec):
    inputVolume = File(desc="Required: input file containing the signed short image to reorient without resampling.", exists=True, argstr="--inputVolume %s")
    inputReferenceVolume = File(desc="Required: input file containing the standard image to clone the characteristics of.", exists=True, argstr="--inputReferenceVolume %s")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Required: name of output Nrrd or Nifti file containing the reoriented image in reference image space.", argstr="--outputVolume %s")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class gtractImageConformityOutputSpec(TraitedSpec):
    outputVolume = File(desc="Required: name of output Nrrd or Nifti file containing the reoriented image in reference image space.", exists=True)


class gtractImageConformity(SlicerCommandLine):
    """title: Image Conformity

category: Diffusion.GTRACT

description: This program will straighten out the Direction and Origin to match the Reference Image.

version: 4.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:GTRACT

license: http://mri.radiology.uiowa.edu/copyright/GTRACT-Copyright.txt

contributor: This tool was developed by Vincent Magnotta and Greg Harris.

acknowledgements: Funding for this version of the GTRACT program was provided by NIH/NINDS R01NS050568-01A2S1

"""

    input_spec = gtractImageConformityInputSpec
    output_spec = gtractImageConformityOutputSpec
    _cmd = " gtractImageConformity "
    _outputs_filenames = {'outputVolume':'outputVolume.nrrd'}


class gtractCoregBvaluesInputSpec(CommandLineInputSpec):
    movingVolume = File(desc="Required: input moving image file name. In order to register gradients within a scan to its first gradient, set the movingVolume and fixedVolume as the same image.", exists=True, argstr="--movingVolume %s")
    fixedVolume = File(desc="Required: input fixed image file name. It is recommended that this image should either contain or be a b0 image.", exists=True, argstr="--fixedVolume %s")
    fixedVolumeIndex = traits.Int(desc="Index in the fixed image for registration. It is recommended that this image should be a b0 image.", argstr="--fixedVolumeIndex %d")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Required: name of output NRRD file containing moving images individually resampled and fit to the specified fixed image index.", argstr="--outputVolume %s")
    outputTransform = traits.Either(traits.Bool, File(), hash_files=False, desc="Registration 3D transforms concatenated in a single output file.  There are no tools that can use this, but can be used for debugging purposes.", argstr="--outputTransform %s")
    eddyCurrentCorrection = traits.Bool(desc="Flag to perform eddy current corection in addition to motion correction (recommended)", argstr="--eddyCurrentCorrection ")
    numberOfIterations = traits.Int(desc="Number of iterations in each 3D fit", argstr="--numberOfIterations %d")
    numberOfSpatialSamples = traits.Int(desc="Number of voxels sampled for mutual information computation in each 3D fit step", argstr="--numberOfSpatialSamples %d")
    relaxationFactor = traits.Float(desc="Fraction of gradient from Jacobian to attempt to move in each 3D fit step (adjust when eddyCurrentCorrection is enabled; suggested value = 0.25)", argstr="--relaxationFactor %f")
    maximumStepSize = traits.Float(desc="Maximum permitted step size to move in each 3D fit step (adjust when eddyCurrentCorrection is enabled; suggested value = 0.1)", argstr="--maximumStepSize %f")
    minimumStepSize = traits.Float(desc="Minimum required step size to move in each 3D fit step without converging -- decrease this to make the fit more exacting", argstr="--minimumStepSize %f")
    spatialScale = traits.Float(desc="How much to scale up changes in position compared to unit rotational changes in radians -- decrease this to put more rotation in the fit", argstr="--spatialScale %f")
    registerB0Only = traits.Bool(desc="Register the B0 images only", argstr="--registerB0Only ")
    debugLevel = traits.Int(desc="Display debug messages, and produce debug intermediate results.  0=OFF, 1=Minimal, 10=Maximum debugging.", argstr="--debugLevel %d")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class gtractCoregBvaluesOutputSpec(TraitedSpec):
    outputVolume = File(desc="Required: name of output NRRD file containing moving images individually resampled and fit to the specified fixed image index.", exists=True)
    outputTransform = File(desc="Registration 3D transforms concatenated in a single output file.  There are no tools that can use this, but can be used for debugging purposes.", exists=True)


class gtractCoregBvalues(SlicerCommandLine):
    """title: Coregister B-Values

category: Diffusion.GTRACT

description: This step should be performed after converting DWI scans from DICOM to NRRD format. This program will register all gradients in a NRRD diffusion weighted 4D vector image (moving image) to a specified index in a fixed image. It also supports co-registration with a T2 weighted image or field map in the same plane as the DWI data. The fixed image for the registration should be a b0 image. A mutual information metric cost function is used for the registration because of the differences in signal intensity as a result of the diffusion gradients. The full affine allows the registration procedure to correct for eddy current distortions that may exist in the data. If the eddyCurrentCorrection is enabled, relaxationFactor (0.25) and maximumStepSize (0.1) should be adjusted.

version: 4.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:GTRACT

license: http://mri.radiology.uiowa.edu/copyright/GTRACT-Copyright.txt

contributor: This tool was developed by Vincent Magnotta and Greg Harris.

acknowledgements: Funding for this version of the GTRACT program was provided by NIH/NINDS R01NS050568-01A2S1

"""

    input_spec = gtractCoregBvaluesInputSpec
    output_spec = gtractCoregBvaluesOutputSpec
    _cmd = " gtractCoregBvalues "
    _outputs_filenames = {'outputVolume':'outputVolume.nrrd','outputTransform':'outputTransform.mat'}
