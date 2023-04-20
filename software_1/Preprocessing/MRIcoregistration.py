import SimpleITK as sitk
import numpy as np

def register_slices(image):

    # Cria uma imagem de referência (fixa) usando a primeira fatia da imagem
    fixed_image = sitk.GetImageFromArray(image[0][0].pixel_array)
    fixed_image = sitk.Cast(fixed_image, sitk.sitkFloat32)

    # Inicializa uma lista para armazenar as matrizes de transformação para cada fatia
    transforms = []

    # Faz o registro para cada fatia da imagem
    for i in range(1, len(image[:])):
        for j in range(len(image[0][:])):
            # Cria uma imagem móvel usando a fatia atual
            moving_image = sitk.GetImageFromArray(np.array(image[i][j].pixel_array))
            moving_image = sitk.Cast(moving_image, sitk.sitkFloat32)

            # Cria uma transformação inicial usando a matriz de transformação da fatia anterior
            if i == 1:
                initial_transform = sitk.CenteredTransformInitializer(fixed_image, moving_image, sitk.Euler2DTransform(),
                                                                      sitk.CenteredTransformInitializerFilter.GEOMETRY)
            else:
                initial_transform = sitk.Transform(initial_transform)

            # Cria o objeto de registro e configura os parâmetros
            registration_method = sitk.ImageRegistrationMethod()
            registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
            registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
            registration_method.SetMetricSamplingPercentage(0.01)
            registration_method.SetInterpolator(sitk.sitkLinear)
            registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100,
                                                              convergenceMinimumValue=1e-6, convergenceWindowSize=10)
            registration_method.SetOptimizerScalesFromPhysicalShift()
            registration_method.SetInitialTransform(initial_transform)

            transforms.append(registration_method.Execute(fixed_image, moving_image))

    k=0

    for i in range(1, len(image[:])):
        for j in range(len(image[0][:])):

            # Cria a transformação a partir da matriz de transformação da fatia correspondente
            transform = sitk.Euler2DTransform()
            transform.SetParameters(sitk.VectorDouble(transforms[k].GetParameters()))

            # Aplica a transformação à fatia atual
            resampled = sitk.Resample(sitk.GetImageFromArray(np.array(image[i][j].pixel_array)), fixed_image, transform, sitk.sitkLinear, 0.0)
            image[i][j].pixel_array = sitk.GetArrayFromImage(resampled)

            k = k + 1

    # Retorna a lista de fatias registradas
    return image