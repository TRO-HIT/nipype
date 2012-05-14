from nipype.interfaces.base import CommandLine, CommandLineInputSpec, TraitedSpec, File, Directory, traits, isdefined, InputMultiPath, OutputMultiPath
import os
from nipype.interfaces.slicer.base import SlicerCommandLine


class BRAINSResampleInputSpec(CommandLineInputSpec):
    inputVolume = File(desc="Image To Warp", exists=True, argstr="--inputVolume %s")
    referenceVolume = File(desc="Reference image used only to define the output space. If not specified, the warping is done in the same space as the image to warp.", exists=True, argstr="--referenceVolume %s")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Resulting deformed image", argstr="--outputVolume %s")
    pixelType = traits.Enum("float", "short", "ushort", "int", "uint", "uchar", "binary", desc="Specifies the pixel type for the input/output images.  The \"binary\" pixel type uses a modified algorithm whereby the image is read in as unsigned char, a signed distance map is created, signed distance map is resampled, and then a thresholded image of type unsigned char is written to disk.", argstr="--pixelType %s")
    deformationVolume = File(desc="Displacement Field to be used to warp the image", exists=True, argstr="--deformationVolume %s")
    warpTransform = File(desc="Filename for the BRAINSFit transform used in place of the deformation field", exists=True, argstr="--warpTransform %s")
    interpolationMode = traits.Enum("NearestNeighbor", "Linear", "ResampleInPlace", "BSpline", "WindowedSinc", "Hamming", "Cosine", "Welch", "Lanczos", "Blackman", desc="Type of interpolation to be used when applying transform to moving volume.  Options are Linear, ResampleInPlace, NearestNeighbor, BSpline, or WindowedSinc", argstr="--interpolationMode %s")
    inverseTransform = traits.Bool(desc="True/False is to compute inverse of given transformation. Default is false", argstr="--inverseTransform ")
    defaultValue = traits.Float(desc="Default voxel value", argstr="--defaultValue %f")
    gridSpacing = InputMultiPath(traits.Int, desc="Add warped grid to output image to help show the deformation that occured with specified spacing.   A spacing of 0 in a dimension indicates that grid lines should be rendered to fall exactly (i.e. do not allow displacements off that plane).  This is useful for makeing a 2D image of grid lines from the 3D space ", sep=",", argstr="--gridSpacing %s")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class BRAINSResampleOutputSpec(TraitedSpec):
    outputVolume = File(desc="Resulting deformed image", exists=True)


class BRAINSResample(SlicerCommandLine):
    """title: Resample Image (BRAINS)

category: Registration

description: 
	  This program collects together three common image processing tasks that all involve resampling an image volume: Resampling to a new resolution and spacing, applying a transformation (using an ITK transform IO mechanisms) and Warping (using a vector image deformation field).  Full documentation available here: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.0/Modules/BRAINSResample.
  

version: 3.0.0

documentation-url: http://www.slicer.org/slicerWiki/index.php/Modules:BRAINSResample

license: https://www.nitrc.org/svn/brains/BuildScripts/trunk/License.txt 

contributor: This tool was developed by Vincent Magnotta, Greg Harris, and Hans Johnson.

acknowledgements: The development of this tool was supported by funding from grants NS050568 and NS40068 from the National Institute of Neurological Disorders and Stroke and grants MH31593, MH40856, from the National Institute of Mental Health.  

"""

    input_spec = BRAINSResampleInputSpec
    output_spec = BRAINSResampleOutputSpec
    _cmd = " BRAINSResample "
    _outputs_filenames = {'outputVolume':'outputVolume.nii'}


class VBRAINSDemonWarpInputSpec(CommandLineInputSpec):
    movingVolume = InputMultiPath(File(exists=True), desc="Required: input moving image", argstr="--movingVolume %s...")
    fixedVolume = InputMultiPath(File(exists=True), desc="Required: input fixed (target) image", argstr="--fixedVolume %s...")
    inputPixelType = traits.Enum("float", "short", "ushort", "int", "uchar", desc="Input volumes will be typecast to this format: float|short|ushort|int|uchar", argstr="--inputPixelType %s")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Required: output resampled moving image (will have the same physical space as the fixedVolume).", argstr="--outputVolume %s")
    outputDeformationFieldVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Output deformation field vector image (will have the same physical space as the fixedVolume).", argstr="--outputDeformationFieldVolume %s")
    outputPixelType = traits.Enum("float", "short", "ushort", "int", "uchar", desc="outputVolume will be typecast to this format: float|short|ushort|int|uchar", argstr="--outputPixelType %s")
    interpolationMode = traits.Enum("NearestNeighbor", "Linear", "ResampleInPlace", "BSpline", "WindowedSinc", "Hamming", "Cosine", "Welch", "Lanczos", "Blackman", desc="Type of interpolation to be used when applying transform to moving volume.  Options are Linear, ResampleInPlace, NearestNeighbor, BSpline, or WindowedSinc", argstr="--interpolationMode %s")
    registrationFilterType = traits.Enum("Demons", "FastSymmetricForces", "Diffeomorphic", "LogDemons", "SymmetricLogDemons", desc="Registration Filter Type: Demons|FastSymmetricForces|Diffeomorphic|LogDemons|SymmetricLogDemons", argstr="--registrationFilterType %s")
    smoothDeformationFieldSigma = traits.Float(desc="A gaussian smoothing value to be applied to the deformation feild at each iteration.", argstr="--smoothDeformationFieldSigma %f")
    numberOfPyramidLevels = traits.Int(desc="Number of image pyramid levels to use in the multi-resolution registration.", argstr="--numberOfPyramidLevels %d")
    minimumFixedPyramid = InputMultiPath(traits.Int, desc="The shrink factor for the first level of the fixed image pyramid. (i.e. start at 1/16 scale, then 1/8, then 1/4, then 1/2, and finally full scale)", sep=",", argstr="--minimumFixedPyramid %s")
    minimumMovingPyramid = InputMultiPath(traits.Int, desc="The shrink factor for the first level of the moving image pyramid. (i.e. start at 1/16 scale, then 1/8, then 1/4, then 1/2, and finally full scale)", sep=",", argstr="--minimumMovingPyramid %s")
    arrayOfPyramidLevelIterations = InputMultiPath(traits.Int, desc="The number of iterations for each pyramid level", sep=",", argstr="--arrayOfPyramidLevelIterations %s")
    histogramMatch = traits.Bool(desc="Histogram Match the input images.  This is suitable for images of the same modality that may have different absolute scales, but the same overall intensity profile.", argstr="--histogramMatch ")
    numberOfHistogramBins = traits.Int(desc="The number of histogram levels", argstr="--numberOfHistogramBins %d")
    numberOfMatchPoints = traits.Int(desc="The number of match points for histrogramMatch", argstr="--numberOfMatchPoints %d")
    medianFilterSize = InputMultiPath(traits.Int, desc="Median filter radius in all 3 directions.  When images have a lot of salt and pepper noise, this step can improve the registration.", sep=",", argstr="--medianFilterSize %s")
    initializeWithDeformationField = File(desc="Initial deformation field vector image file name", exists=True, argstr="--initializeWithDeformationField %s")
    initializeWithTransform = File(desc="Initial Transform filename", exists=True, argstr="--initializeWithTransform %s")
    makeBOBF = traits.Bool(desc="Flag to make Brain-Only Background-Filled versions of the input and target volumes.", argstr="--makeBOBF ")
    fixedBinaryVolume = File(desc="Mask filename for desired region of interest in the Fixed image.", exists=True, argstr="--fixedBinaryVolume %s")
    movingBinaryVolume = File(desc="Mask filename for desired region of interest in the Moving image.", exists=True, argstr="--movingBinaryVolume %s")
    lowerThresholdForBOBF = traits.Int(desc="Lower threshold for performing BOBF", argstr="--lowerThresholdForBOBF %d")
    upperThresholdForBOBF = traits.Int(desc="Upper threshold for performing BOBF", argstr="--upperThresholdForBOBF %d")
    backgroundFillValue = traits.Int(desc="Replacement value to overwrite background when performing BOBF", argstr="--backgroundFillValue %d")
    seedForBOBF = InputMultiPath(traits.Int, desc="coordinates in all 3 directions for Seed when performing BOBF", sep=",", argstr="--seedForBOBF %s")
    neighborhoodForBOBF = InputMultiPath(traits.Int, desc="neighborhood in all 3 directions to be included when performing BOBF", sep=",", argstr="--neighborhoodForBOBF %s")
    outputDisplacementFieldPrefix = traits.Str(desc="Displacement field filename prefix for writing separate x, y, and z component images", argstr="--outputDisplacementFieldPrefix %s")
    outputCheckerboardVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Genete a checkerboard image volume between the fixedVolume and the deformed movingVolume.", argstr="--outputCheckerboardVolume %s")
    checkerboardPatternSubdivisions = InputMultiPath(traits.Int, desc="Number of Checkerboard subdivisions in all 3 directions", sep=",", argstr="--checkerboardPatternSubdivisions %s")
    outputNormalized = traits.Bool(desc="Flag to warp and write the normalized images to output.  In normalized images the image values are fit-scaled to be between 0 and the maximum storage type value.", argstr="--outputNormalized ")
    outputDebug = traits.Bool(desc="Flag to write debugging images after each step.", argstr="--outputDebug ")
    weightFactors = InputMultiPath(traits.Float, desc="Weight fatctors for each input images", sep=",", argstr="--weightFactors %s")
    gradient_type = traits.Enum("0", "1", "2", desc="Type of gradient used for computing the demons force (0 is symmetrized, 1 is fixed image, 2 is moving image)", argstr="--gradient_type %s")
    upFieldSmoothing = traits.Float(desc="Smoothing sigma for the update field at each iteration", argstr="--upFieldSmoothing %f")
    max_step_length = traits.Float(desc="Maximum length of an update vector (0: no restriction)", argstr="--max_step_length %f")
    use_vanilla_dem = traits.Bool(desc="Run vanilla demons algorithm", argstr="--use_vanilla_dem ")
    gui = traits.Bool(desc="Display intermediate image volumes for debugging", argstr="--gui ")
    promptUser = traits.Bool(desc="Prompt the user to hit enter each time an image is sent to the DebugImageViewer", argstr="--promptUser ")
    numberOfBCHApproximationTerms = traits.Int(desc="Number of terms in the BCH expansion", argstr="--numberOfBCHApproximationTerms %d")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class VBRAINSDemonWarpOutputSpec(TraitedSpec):
    outputVolume = File(desc="Required: output resampled moving image (will have the same physical space as the fixedVolume).", exists=True)
    outputDeformationFieldVolume = File(desc="Output deformation field vector image (will have the same physical space as the fixedVolume).", exists=True)
    outputCheckerboardVolume = File(desc="Genete a checkerboard image volume between the fixedVolume and the deformed movingVolume.", exists=True)


class VBRAINSDemonWarp(SlicerCommandLine):
    """title: Vector Demon Registration (BRAINS)

category: Registration

description: 
    This program finds a deformation field to warp a moving image onto a fixed image.  The images must be of the same signal kind, and contain an image of the same kind of object.  This program uses the Thirion Demons warp software in ITK, the Insight Toolkit.  Additional information is available at: http://www.nitrc.org/projects/brainsdemonwarp.

  

version: 3.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:BRAINSDemonWarp

license: https://www.nitrc.org/svn/brains/BuildScripts/trunk/License.txt 

contributor: This tool was developed by Hans J. Johnson and Greg Harris.

acknowledgements: The development of this tool was supported by funding from grants NS050568 and NS40068 from the National Institute of Neurological Disorders and Stroke and grants MH31593, MH40856, from the National Institute of Mental Health.  

"""

    input_spec = VBRAINSDemonWarpInputSpec
    output_spec = VBRAINSDemonWarpOutputSpec
    _cmd = " VBRAINSDemonWarp "
    _outputs_filenames = {'outputVolume':'outputVolume.nii','outputCheckerboardVolume':'outputCheckerboardVolume.nii','outputDeformationFieldVolume':'outputDeformationFieldVolume.nrrd'}


class BRAINSFitInputSpec(CommandLineInputSpec):
    fixedVolume = File(desc="The fixed image for registration by mutual information optimization.", exists=True, argstr="--fixedVolume %s")
    movingVolume = File(desc="The moving image for registration by mutual information optimization.", exists=True, argstr="--movingVolume %s")
    bsplineTransform = traits.Either(traits.Bool, File(), hash_files=False, desc="(optional) Filename to which save the estimated transform. NOTE: You must set at least one output object (either a deformed image or a transform.  NOTE: USE THIS ONLY IF THE FINAL TRANSFORM IS BSpline", argstr="--bsplineTransform %s")
    linearTransform = traits.Either(traits.Bool, File(), hash_files=False, desc="(optional) Filename to which save the estimated transform. NOTE: You must set at least one output object (either a deformed image or a transform.  NOTE: USE THIS ONLY IF THE FINAL TRANSFORM IS ---NOT--- BSpline", argstr="--linearTransform %s")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="(optional) Output image for registration. NOTE: You must select either the outputTransform or the outputVolume option.", argstr="--outputVolume %s")
    initialTransform = File(desc="Filename of transform used to initialize the registration.  This CAN NOT be used with either CenterOfHeadLAlign, MomentsAlign, GeometryAlign, or initialTransform file.", exists=True, argstr="--initialTransform %s")
    initializeTransformMode = traits.Enum("Off", "useMomentsAlign", "useCenterOfHeadAlign", "useGeometryAlign", "useCenterOfROIAlign", desc="Determine how to initialize the transform center.  GeometryAlign on assumes that the center of the voxel lattice of the images represent similar structures.  MomentsAlign assumes that the center of mass of the images represent similar structures.  useCenterOfHeadAlign attempts to use the top of head and shape of neck to drive a center of mass estimate.  Off assumes that the physical space of the images are close, and that centering in terms of the image Origins is a good starting point.  This flag is mutually exclusive with the initialTransform flag.", argstr="--initializeTransformMode %s")
    useRigid = traits.Bool(desc="Perform a rigid registration as part of the sequential registration steps.  This family of options superceeds the use of transformType if any of them are set.", argstr="--useRigid ")
    useScaleVersor3D = traits.Bool(desc="Perform a ScaleVersor3D registration as part of the sequential registration steps.  This family of options superceeds the use of transformType if any of them are set.", argstr="--useScaleVersor3D ")
    useScaleSkewVersor3D = traits.Bool(desc="Perform a ScaleSkewVersor3D registration as part of the sequential registration steps.  This family of options superceeds the use of transformType if any of them are set.", argstr="--useScaleSkewVersor3D ")
    useAffine = traits.Bool(desc="Perform an Affine registration as part of the sequential registration steps.  This family of options superceeds the use of transformType if any of them are set.", argstr="--useAffine ")
    useBSpline = traits.Bool(desc="Perform a BSpline registration as part of the sequential registration steps.  This family of options superceeds the use of transformType if any of them are set.", argstr="--useBSpline ")
    useComposite = traits.Bool(desc="Perform a Composite registration as part of the sequential registration steps.  This family of options superceeds the use of transformType if any of them are set.", argstr="--useComposite ")
    numberOfSamples = traits.Int(desc="The number of voxels sampled for mutual information computation.  Increase this for a slower, more careful fit.  You can also limit the sampling focus with ROI masks and ROIAUTO mask generation.", argstr="--numberOfSamples %d")
    splineGridSize = InputMultiPath(traits.Int, desc="The number of subdivisions of the BSpline Grid to be centered on the image space.  Each dimension must have at least 3 subdivisions for the BSpline to be correctly computed. ", sep=",", argstr="--splineGridSize %s")
    numberOfIterations = InputMultiPath(traits.Int, desc="The maximum number of iterations to try before failing to converge.  Use an explicit limit like 500 or 1000 to manage risk of divergence", sep=",", argstr="--numberOfIterations %s")
    maskProcessingMode = traits.Enum("NOMASK", "ROIAUTO", "ROI", desc="What mode to use for using the masks.  If ROIAUTO is choosen, then the mask is implicitly defined using a otsu forground and hole filling algorithm. The Region Of Interest mode (choose ROI) uses the masks to define what parts of the image should be used for computing the transform.", argstr="--maskProcessingMode %s")
    fixedBinaryVolume = File(desc="Fixed Image binary mask volume, ONLY FOR MANUAL ROI mode.", exists=True, argstr="--fixedBinaryVolume %s")
    movingBinaryVolume = File(desc="Moving Image binary mask volume, ONLY FOR MANUAL ROI mode.", exists=True, argstr="--movingBinaryVolume %s")
    outputFixedVolumeROI = traits.Either(traits.Bool, File(), hash_files=False, desc="The ROI automatically found in fixed image, ONLY FOR ROIAUTO mode.", argstr="--outputFixedVolumeROI %s")
    outputMovingVolumeROI = traits.Either(traits.Bool, File(), hash_files=False, desc="The ROI automatically found in moving image, ONLY FOR ROIAUTO mode.", argstr="--outputMovingVolumeROI %s")
    outputVolumePixelType = traits.Enum("float", "short", "ushort", "int", "uint", "uchar", desc="The output image Pixel Type is the scalar datatype for representation of the Output Volume.", argstr="--outputVolumePixelType %s")
    backgroundFillValue = traits.Float(desc="Background fill value for output image.", argstr="--backgroundFillValue %f")
    maskInferiorCutOffFromCenter = traits.Float(desc="For use with --useCenterOfHeadAlign (and --maskProcessingMode ROIAUTO): the cut-off below the image centers, in millimeters, ", argstr="--maskInferiorCutOffFromCenter %f")
    scaleOutputValues = traits.Bool(desc="If true, and the voxel values do not fit within the minimum and maximum values of the desired outputVolumePixelType, then linearly scale the min/max output image voxel values to fit within the min/max range of the outputVolumePixelType.", argstr="--scaleOutputValues ")
    interpolationMode = traits.Enum("NearestNeighbor", "Linear", "ResampleInPlace", "BSpline", "WindowedSinc", "Hamming", "Cosine", "Welch", "Lanczos", "Blackman", desc="Type of interpolation to be used when applying transform to moving volume.  Options are Linear, NearestNeighbor, BSpline, WindowedSinc, or ResampleInPlace.  The ResampleInPlace option will create an image with the same discrete voxel values and will adjust the origin and direction of the physical space interpretation.", argstr="--interpolationMode %s")
    minimumStepLength = InputMultiPath(traits.Float, desc="Each step in the optimization takes steps at least this big.  When none are possible, registration is complete.", sep=",", argstr="--minimumStepLength %s")
    translationScale = traits.Float(desc="How much to scale up changes in position compared to unit rotational changes in radians -- decrease this to put more rotation in the search pattern.", argstr="--translationScale %f")
    reproportionScale = traits.Float(desc="ScaleVersor3D 'Scale' compensation factor.  Increase this to put more rescaling in a ScaleVersor3D or ScaleSkewVersor3D search pattern.  1.0 works well with a translationScale of 1000.0", argstr="--reproportionScale %f")
    skewScale = traits.Float(desc="ScaleSkewVersor3D Skew compensation factor.  Increase this to put more skew in a ScaleSkewVersor3D search pattern.  1.0 works well with a translationScale of 1000.0", argstr="--skewScale %f")
    maxBSplineDisplacement = traits.Float(desc=" Sets the maximum allowed displacements in image physical coordinates for BSpline control grid along each axis.  A value of 0.0 indicates that the problem should be unbounded.  NOTE:  This only constrains the BSpline portion, and does not limit the displacement from the associated bulk transform.  This can lead to a substantial reduction in computation time in the BSpline optimizer.,       ", argstr="--maxBSplineDisplacement %f")
    histogramMatch = traits.Bool(desc="Histogram Match the input images.  This is suitable for images of the same modality that may have different absolute scales, but the same overall intensity profile. Do NOT use if registering images from different modailties.", argstr="--histogramMatch ")
    numberOfHistogramBins = traits.Int(desc="The number of histogram levels", argstr="--numberOfHistogramBins %d")
    numberOfMatchPoints = traits.Int(desc="the number of match points", argstr="--numberOfMatchPoints %d")
    strippedOutputTransform = traits.Either(traits.Bool, File(), hash_files=False, desc="File name for the rigid component of the estimated affine transform. Can be used to rigidly register the moving image to the fixed image. NOTE:  This value is overwritten if either bsplineTransform or linearTransform is set.", argstr="--strippedOutputTransform %s")
    transformType = InputMultiPath(traits.Str, desc="Specifies a list of registration types to be used.  The valid types are, Rigid, ScaleVersor3D, ScaleSkewVersor3D, Affine, and BSpline.  Specifiying more than one in a comma separated list will initialize the next stage with the previous results. If registrationClass flag is used, it overrides this parameter setting.", sep=",", argstr="--transformType %s")
    outputTransform = traits.Either(traits.Bool, File(), hash_files=False, desc="(optional) Filename to which save the (optional) estimated transform. NOTE: You must select either the outputTransform or the outputVolume option.", argstr="--outputTransform %s")
    fixedVolumeTimeIndex = traits.Int(desc="The index in the time series for the 3D fixed image to fit, if 4-dimensional.", argstr="--fixedVolumeTimeIndex %d")
    movingVolumeTimeIndex = traits.Int(desc="The index in the time series for the 3D moving image to fit, if 4-dimensional.", argstr="--movingVolumeTimeIndex %d")
    medianFilterSize = InputMultiPath(traits.Int, desc="The radius for the optional MedianImageFilter preprocessing in all 3 directions.", sep=",", argstr="--medianFilterSize %s")
    removeIntensityOutliers = traits.Float(desc="The half percentage to decide outliers of image intensities. The default value is zero, which means no outlier removal. If the value of 0.005 is given, the moduel will throw away 0.005 % of both tails, so 0.01% of intensities in total would be ignored in its statistic calculation. ", argstr="--removeIntensityOutliers %f")
    useCachingOfBSplineWeightsMode = traits.Enum("ON", "OFF", desc="This is a 5x speed advantage at the expense of requiring much more memory.  Only relevant when transformType is BSpline.", argstr="--useCachingOfBSplineWeightsMode %s")
    useExplicitPDFDerivativesMode = traits.Enum("AUTO", "ON", "OFF", desc="Using mode AUTO means OFF for BSplineDeformableTransforms and ON for the linear transforms.  The ON alternative uses more memory to sometimes do a better job.", argstr="--useExplicitPDFDerivativesMode %s")
    ROIAutoDilateSize = traits.Float(desc="This flag is only relavent when using ROIAUTO mode for initializing masks.  It defines the final dilation size to capture a bit of background outside the tissue region.  At setting of 10mm has been shown to help regularize a BSpline registration type so that there is some background constraints to match the edges of the head better.", argstr="--ROIAutoDilateSize %f")
    ROIAutoClosingSize = traits.Float(desc="This flag is only relavent when using ROIAUTO mode for initializing masks.  It defines the hole closing size in mm.  It is rounded up to the nearest whole pixel size in each direction. The default is to use a closing size of 9mm.  For mouse data this value may need to be reset to 0.9 or smaller.", argstr="--ROIAutoClosingSize %f")
    relaxationFactor = traits.Float(desc="Internal debugging parameter, and should probably never be used from the command line.  This will be removed in the future.", argstr="--relaxationFactor %f")
    maximumStepLength = traits.Float(desc="Internal debugging parameter, and should probably never be used from the command line.  This will be removed in the future.", argstr="--maximumStepLength %f")
    failureExitCode = traits.Int(desc="If the fit fails, exit with this status code.  (It can be used to force a successfult exit status of (0) if the registration fails due to reaching the maximum number of iterations.", argstr="--failureExitCode %d")
    writeTransformOnFailure = traits.Bool(desc="Flag to save the final transform even if the numberOfIterations are reached without convergence. (Intended for use when --failureExitCode 0 )", argstr="--writeTransformOnFailure ")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use. (default is auto-detected)", argstr="--numberOfThreads %d")
    forceMINumberOfThreads = traits.Int(desc="Force the the maximum number of threads to use for non thread safe MI metric.", argstr="--forceMINumberOfThreads %d")
    debugLevel = traits.Int(desc="Display debug messages, and produce debug intermediate results.  0=OFF, 1=Minimal, 10=Maximum debugging.", argstr="--debugLevel %d")
    costFunctionConvergenceFactor = traits.Float(desc=" From itkLBFGSBOptimizer.h: Set/Get the CostFunctionConvergenceFactor. Algorithm terminates when the reduction in cost function is less than (factor * epsmcj) where epsmch is the machine precision. Typical values for factor: 1e+12 for low accuracy; 1e+7 for moderate accuracy and 1e+1 for extremely high accuracy.  1e+9 seems to work well.,       ", argstr="--costFunctionConvergenceFactor %f")
    projectedGradientTolerance = traits.Float(desc=" From itkLBFGSBOptimizer.h: Set/Get the ProjectedGradientTolerance. Algorithm terminates when the project gradient is below the tolerance. Default lbfgsb value is 1e-5, but 1e-4 seems to work well.,       ", argstr="--projectedGradientTolerance %f")
    gui = traits.Bool(desc="Display intermediate image volumes for debugging.  NOTE:  This is not part of the standard build sytem, and probably does nothing on your installation.", argstr="--gui ")
    promptUser = traits.Bool(desc="Prompt the user to hit enter each time an image is sent to the DebugImageViewer", argstr="--promptUser ")
    NEVER_USE_THIS_FLAG_IT_IS_OUTDATED_00 = traits.Bool(desc="DO NOT USE THIS FLAG", argstr="--NEVER_USE_THIS_FLAG_IT_IS_OUTDATED_00 ")
    NEVER_USE_THIS_FLAG_IT_IS_OUTDATED_01 = traits.Bool(desc="DO NOT USE THIS FLAG", argstr="--NEVER_USE_THIS_FLAG_IT_IS_OUTDATED_01 ")
    NEVER_USE_THIS_FLAG_IT_IS_OUTDATED_02 = traits.Bool(desc="DO NOT USE THIS FLAG", argstr="--NEVER_USE_THIS_FLAG_IT_IS_OUTDATED_02 ")
    permitParameterVariation = InputMultiPath(traits.Int, desc="A bit vector to permit linear transform parameters to vary under optimization.  The vector order corresponds with transform parameters, and beyond the end ones fill in as a default.  For instance, you can choose to rotate only in x (pitch) with 1,0,0;  this is mostly for expert use in turning on and off individual degrees of freedom in rotation, translation or scaling without multiplying the number of transform representations; this trick is probably meaningless when tried with the general affine transform.", sep=",", argstr="--permitParameterVariation %s")
    costMetric = traits.Enum("MMI", "MSE", "NC", "MC", desc="The cost metric to be used during fitting. Defaults to MMI. Options are MMI (Mattes Mutual Information), MSE (Mean Square Error), NC (Normalized Correlation), MC (Match Cardinality for binary images)", argstr="--costMetric %s")


class BRAINSFitOutputSpec(TraitedSpec):
    bsplineTransform = File(desc="(optional) Filename to which save the estimated transform. NOTE: You must set at least one output object (either a deformed image or a transform.  NOTE: USE THIS ONLY IF THE FINAL TRANSFORM IS BSpline", exists=True)
    linearTransform = File(desc="(optional) Filename to which save the estimated transform. NOTE: You must set at least one output object (either a deformed image or a transform.  NOTE: USE THIS ONLY IF THE FINAL TRANSFORM IS ---NOT--- BSpline", exists=True)
    outputVolume = File(desc="(optional) Output image for registration. NOTE: You must select either the outputTransform or the outputVolume option.", exists=True)
    outputFixedVolumeROI = File(desc="The ROI automatically found in fixed image, ONLY FOR ROIAUTO mode.", exists=True)
    outputMovingVolumeROI = File(desc="The ROI automatically found in moving image, ONLY FOR ROIAUTO mode.", exists=True)
    strippedOutputTransform = File(desc="File name for the rigid component of the estimated affine transform. Can be used to rigidly register the moving image to the fixed image. NOTE:  This value is overwritten if either bsplineTransform or linearTransform is set.", exists=True)
    outputTransform = File(desc="(optional) Filename to which save the (optional) estimated transform. NOTE: You must select either the outputTransform or the outputVolume option.", exists=True)


class BRAINSFit(SlicerCommandLine):
    """title: General Registration (BRAINS)

category: Registration

description: Register a three-dimensional volume to a reference volume (Mattes Mutual Information by default). Full documentation avalable here: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.0/Modules/BRAINSFit. Method described in BRAINSFit: Mutual Information Registrations of Whole-Brain 3D Images, Using the Insight Toolkit, Johnson H.J., Harris G., Williams K., The Insight Journal, 2007. http://hdl.handle.net/1926/1291

version: 3.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:BRAINSFit

license: https://www.nitrc.org/svn/brains/BuildScripts/trunk/License.txt 

contributor: Hans J. Johnson, hans-johnson -at- uiowa.edu, http://wwww.psychiatry.uiowa.edu

acknowledgements: Hans Johnson(1,3,4); Kent Williams(1); Gregory Harris(1), Vincent Magnotta(1,2,3);  Andriy Fedorov(5) 1=University of Iowa Department of Psychiatry, 2=University of Iowa Department of Radiology, 3=University of Iowa Department of Biomedical Engineering, 4=University of Iowa Department of Electrical and Computer Engineering, 5=Surgical Planning Lab, Harvard

"""

    input_spec = BRAINSFitInputSpec
    output_spec = BRAINSFitOutputSpec
    _cmd = " BRAINSFit "
    _outputs_filenames = {'outputVolume':'outputVolume.nii','bsplineTransform':'bsplineTransform.mat','outputTransform':'outputTransform.mat','outputFixedVolumeROI':'outputFixedVolumeROI.nii','strippedOutputTransform':'strippedOutputTransform.mat','outputMovingVolumeROI':'outputMovingVolumeROI.nii','linearTransform':'linearTransform.mat'}


class BRAINSDemonWarpInputSpec(CommandLineInputSpec):
    movingVolume = File(desc="Required: input moving image", exists=True, argstr="--movingVolume %s")
    fixedVolume = File(desc="Required: input fixed (target) image", exists=True, argstr="--fixedVolume %s")
    inputPixelType = traits.Enum("float", "short", "ushort", "int", "uchar", desc="Input volumes will be typecast to this format: float|short|ushort|int|uchar", argstr="--inputPixelType %s")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Required: output resampled moving image (will have the same physical space as the fixedVolume).", argstr="--outputVolume %s")
    outputDeformationFieldVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Output deformation field vector image (will have the same physical space as the fixedVolume).", argstr="--outputDeformationFieldVolume %s")
    outputPixelType = traits.Enum("float", "short", "ushort", "int", "uchar", desc="outputVolume will be typecast to this format: float|short|ushort|int|uchar", argstr="--outputPixelType %s")
    interpolationMode = traits.Enum("NearestNeighbor", "Linear", "ResampleInPlace", "BSpline", "WindowedSinc", "Hamming", "Cosine", "Welch", "Lanczos", "Blackman", desc="Type of interpolation to be used when applying transform to moving volume.  Options are Linear, ResampleInPlace, NearestNeighbor, BSpline, or WindowedSinc", argstr="--interpolationMode %s")
    registrationFilterType = traits.Enum("Demons", "FastSymmetricForces", "Diffeomorphic", "LogDemons", "SymmetricLogDemons", desc="Registration Filter Type: Demons|FastSymmetricForces|Diffeomorphic|LogDemons|SymmetricLogDemons", argstr="--registrationFilterType %s")
    smoothDeformationFieldSigma = traits.Float(desc="A gaussian smoothing value to be applied to the deformation feild at each iteration.", argstr="--smoothDeformationFieldSigma %f")
    numberOfPyramidLevels = traits.Int(desc="Number of image pyramid levels to use in the multi-resolution registration.", argstr="--numberOfPyramidLevels %d")
    minimumFixedPyramid = InputMultiPath(traits.Int, desc="The shrink factor for the first level of the fixed image pyramid. (i.e. start at 1/16 scale, then 1/8, then 1/4, then 1/2, and finally full scale)", sep=",", argstr="--minimumFixedPyramid %s")
    minimumMovingPyramid = InputMultiPath(traits.Int, desc="The shrink factor for the first level of the moving image pyramid. (i.e. start at 1/16 scale, then 1/8, then 1/4, then 1/2, and finally full scale)", sep=",", argstr="--minimumMovingPyramid %s")
    arrayOfPyramidLevelIterations = InputMultiPath(traits.Int, desc="The number of iterations for each pyramid level", sep=",", argstr="--arrayOfPyramidLevelIterations %s")
    histogramMatch = traits.Bool(desc="Histogram Match the input images.  This is suitable for images of the same modality that may have different absolute scales, but the same overall intensity profile.", argstr="--histogramMatch ")
    numberOfHistogramBins = traits.Int(desc="The number of histogram levels", argstr="--numberOfHistogramBins %d")
    numberOfMatchPoints = traits.Int(desc="The number of match points for histrogramMatch", argstr="--numberOfMatchPoints %d")
    medianFilterSize = InputMultiPath(traits.Int, desc="Median filter radius in all 3 directions.  When images have a lot of salt and pepper noise, this step can improve the registration.", sep=",", argstr="--medianFilterSize %s")
    initializeWithDeformationField = File(desc="Initial deformation field vector image file name", exists=True, argstr="--initializeWithDeformationField %s")
    initializeWithTransform = File(desc="Initial Transform filename", exists=True, argstr="--initializeWithTransform %s")
    maskProcessingMode = traits.Enum("NOMASK", "ROIAUTO", "ROI", "BOBF", desc="What mode to use for using the masks: NOMASK|ROIAUTO|ROI|BOBF.  If ROIAUTO is choosen, then the mask is implicitly defined using a otsu forground and hole filling algorithm. Where the Region Of Interest mode uses the masks to define what parts of the image should be used for computing the deformation field.  Brain Only Background Fill uses the masks to pre-process the input images by clipping and filling in the background with a predefined value.", argstr="--maskProcessingMode %s")
    fixedBinaryVolume = File(desc="Mask filename for desired region of interest in the Fixed image.", exists=True, argstr="--fixedBinaryVolume %s")
    movingBinaryVolume = File(desc="Mask filename for desired region of interest in the Moving image.", exists=True, argstr="--movingBinaryVolume %s")
    lowerThresholdForBOBF = traits.Int(desc="Lower threshold for performing BOBF", argstr="--lowerThresholdForBOBF %d")
    upperThresholdForBOBF = traits.Int(desc="Upper threshold for performing BOBF", argstr="--upperThresholdForBOBF %d")
    backgroundFillValue = traits.Int(desc="Replacement value to overwrite background when performing BOBF", argstr="--backgroundFillValue %d")
    seedForBOBF = InputMultiPath(traits.Int, desc="coordinates in all 3 directions for Seed when performing BOBF", sep=",", argstr="--seedForBOBF %s")
    neighborhoodForBOBF = InputMultiPath(traits.Int, desc="neighborhood in all 3 directions to be included when performing BOBF", sep=",", argstr="--neighborhoodForBOBF %s")
    outputDisplacementFieldPrefix = traits.Str(desc="Displacement field filename prefix for writing separate x, y, and z component images", argstr="--outputDisplacementFieldPrefix %s")
    outputCheckerboardVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="Genete a checkerboard image volume between the fixedVolume and the deformed movingVolume.", argstr="--outputCheckerboardVolume %s")
    checkerboardPatternSubdivisions = InputMultiPath(traits.Int, desc="Number of Checkerboard subdivisions in all 3 directions", sep=",", argstr="--checkerboardPatternSubdivisions %s")
    outputNormalized = traits.Bool(desc="Flag to warp and write the normalized images to output.  In normalized images the image values are fit-scaled to be between 0 and the maximum storage type value.", argstr="--outputNormalized ")
    outputDebug = traits.Bool(desc="Flag to write debugging images after each step.", argstr="--outputDebug ")
    gradient_type = traits.Enum("0", "1", "2", desc="Type of gradient used for computing the demons force (0 is symmetrized, 1 is fixed image, 2 is moving image)", argstr="--gradient_type %s")
    upFieldSmoothing = traits.Float(desc="Smoothing sigma for the update field at each iteration", argstr="--upFieldSmoothing %f")
    max_step_length = traits.Float(desc="Maximum length of an update vector (0: no restriction)", argstr="--max_step_length %f")
    use_vanilla_dem = traits.Bool(desc="Run vanilla demons algorithm", argstr="--use_vanilla_dem ")
    gui = traits.Bool(desc="Display intermediate image volumes for debugging", argstr="--gui ")
    promptUser = traits.Bool(desc="Prompt the user to hit enter each time an image is sent to the DebugImageViewer", argstr="--promptUser ")
    numberOfBCHApproximationTerms = traits.Int(desc="Number of terms in the BCH expansion", argstr="--numberOfBCHApproximationTerms %d")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class BRAINSDemonWarpOutputSpec(TraitedSpec):
    outputVolume = File(desc="Required: output resampled moving image (will have the same physical space as the fixedVolume).", exists=True)
    outputDeformationFieldVolume = File(desc="Output deformation field vector image (will have the same physical space as the fixedVolume).", exists=True)
    outputCheckerboardVolume = File(desc="Genete a checkerboard image volume between the fixedVolume and the deformed movingVolume.", exists=True)


class BRAINSDemonWarp(SlicerCommandLine):
    """title: Demon Registration (BRAINS)

category: Registration

description: 
    This program finds a deformation field to warp a moving image onto a fixed image.  The images must be of the same signal kind, and contain an image of the same kind of object.  This program uses the Thirion Demons warp software in ITK, the Insight Toolkit.  Additional information is available at: http://www.nitrc.org/projects/brainsdemonwarp.

  

version: 3.0.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Modules:BRAINSDemonWarp

license: https://www.nitrc.org/svn/brains/BuildScripts/trunk/License.txt 

contributor: This tool was developed by Hans J. Johnson and Greg Harris.

acknowledgements: The development of this tool was supported by funding from grants NS050568 and NS40068 from the National Institute of Neurological Disorders and Stroke and grants MH31593, MH40856, from the National Institute of Mental Health.  

"""

    input_spec = BRAINSDemonWarpInputSpec
    output_spec = BRAINSDemonWarpOutputSpec
    _cmd = " BRAINSDemonWarp "
    _outputs_filenames = {'outputVolume':'outputVolume.nii','outputCheckerboardVolume':'outputCheckerboardVolume.nii','outputDeformationFieldVolume':'outputDeformationFieldVolume.nrrd'}
