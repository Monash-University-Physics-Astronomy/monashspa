# Copyright 2019 School of Physics & Astronomy, Monash University
#
# This file is part of monashspa.
#
# monashspa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# monashspa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with monashspa.  If not, see <http://www.gnu.org/licenses/>.

import os

import numpy as np
import pandas
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftfreq
from scipy.interpolate import interp1d
from warnings import warn



def pet_rebuild(filepath, filter_name=None, npoints=None, call_show=True):
    """Perform inverse radon transform on acquired PET data and plots results

    Arguments:
        filepath: A string containing the path to the txt file containing the 
                  PET data
    
    Keyword Arguments:
        filter_name: A string containing the name of the filter to use during
                     reconstruction. Defaults to :code:`None` (no
                     reconstruction). Options are:
                        - None: don't reconstruct
                        - 'none': Reconstruct with no filter
                        - 'ramp': Reconstruct using the Ram-Lak filter
                        - 'Shepp-Logan': Reconstruct using the Shepp-Logan filter
                        - 'cosine': Reconstruct using the cosine filter
                        - 'hamming': Reconstruct using the hamming filter
                        - 'hann': Reconstruct using the hann filter

        npoints: The number of points to reconstruct

        call_show: Whether to call :code:`matplotlib.pyplot.show()` at the end
                   of the function (prior to returning). Defaults to :code:`True`.
                   Set this to :code:`False` if you are not using Spyder/IPython
                   and wish your entire script to complete before showing any 
                   plots. Note, you will need to explicitly call 
                   :code:`matplotlib.pyplot.show()` if you set this to :code:`False`. 
    
    Returns:
        A 2D numpy array containing the coincidence counts (rows correspond to
        each linear stage position and columns to each rotation stage position)

    """
    
    
    ####  define iradon
    def iradon_local(radon_image, theta=None, output_size=None,
               filter="ramp", interpolation="linear", circle=None):
        """
        Inverse radon transform.
        Reconstruct an image from the radon transform, using the filtered
        back projection algorithm.
        Parameters
        ----------
        radon_image : array_like, dtype=float
            Image containing radon transform (sinogram). Each column of
            the image corresponds to a projection along a different angle. The
            tomography rotation axis should lie at the pixel index
            ``radon_image.shape[0] // 2`` along the 0th dimension of
            ``radon_image``.
        theta : array_like, dtype=float, optional
            Reconstruction angles (in degrees). Default: m angles evenly spaced
            between 0 and 180 (if the shape of `radon_image` is (N, M)).
        output_size : int
            Number of rows and columns in the reconstruction.
        filter : str, optional (default ramp)
            Filter used in frequency domain filtering. Ramp filter used by default.
            Filters available: ramp, shepp-logan, cosine, hamming, hann.
            Assign None to use no filter.
        interpolation : str, optional (default 'linear')
            Interpolation method used in reconstruction. Methods available:
            'linear', 'nearest', and 'cubic' ('cubic' is slow).
        circle : boolean, optional
            Assume the reconstructed image is zero outside the inscribed circle.
            Also changes the default output_size to match the behaviour of
            ``radon`` called with ``circle=True``.
            The default behavior (None) is equivalent to False.
        Returns
        -------
        reconstructed : ndarray
            Reconstructed image. The rotation axis will be located in the pixel
            with indices
            ``(reconstructed.shape[0] // 2, reconstructed.shape[1] // 2)``.
        References
        ----------
        .. [1] AC Kak, M Slaney, "Principles of Computerized Tomographic
               Imaging", IEEE Press 1988.
        .. [2] B.R. Ramesh, N. Srinivasa, K. Rajgopal, "An Algorithm for Computing
               the Discrete Radon Transform With Some Applications", Proceedings of
               the Fourth IEEE Region 10 International Conference, TENCON '89, 1989
        Notes
        -----
        It applies the Fourier slice theorem to reconstruct an image by
        multiplying the frequency domain of the filter with the FFT of the
        projection data. This algorithm is called filtered back projection.
        """
        if radon_image.ndim != 2:
            raise ValueError('The input image must be 2-D')
        if theta is None:
            m, n = radon_image.shape
            theta = np.linspace(0, 180, n, endpoint=False)
        else:
            theta = np.asarray(theta)
        if len(theta) != radon_image.shape[1]:
            raise ValueError("The given ``theta`` does not match the number of "
                             "projections in ``radon_image``.")
        interpolation_types = ('linear', 'nearest', 'cubic')
        if interpolation not in interpolation_types:
            raise ValueError("Unknown interpolation: %s" % interpolation)
        if not output_size:
            # If output size not specified, estimate from input radon image
            if circle:
                output_size = radon_image.shape[0]
            else:
                output_size = int(np.floor(np.sqrt((radon_image.shape[0]) ** 2
                                                   / 2.0)))
        if circle is None:
            warn('The default of `circle` in `skimage.transform.iradon` '
                 'will change to `True` in version 0.15.')
            circle = False
        if circle:
            radon_image = _sinogram_circle_to_square(radon_image)

        th = (np.pi / 180.0) * theta
        # resize image to next power of two (but no less than 64) for
        # Fourier analysis; speeds up Fourier and lessens artifacts
        projection_size_padded = \
            max(64, int(2 ** np.ceil(np.log2(2 * radon_image.shape[0]))))
        pad_width = ((0, projection_size_padded - radon_image.shape[0]), (0, 0))
        img = np.pad(radon_image, pad_width, mode='constant', constant_values=0)

        # Construct the Fourier filter
        n1 = np.arange(0, projection_size_padded / 2 + 1, dtype=int)
        n2 = np.arange(projection_size_padded / 2 - 1, 0, -1, dtype=int)
        n = np.concatenate((n1, n2))
        f = np.zeros(projection_size_padded)
        f[0] = 0.25
        f[1::2] = -1 / (np.pi * n[1::2])**2

        omega = 2 * np.pi * fftfreq(projection_size_padded)
        fourier_filter = 2 * np.real(fft(f))         # ramp filter
        if filter == "ramp":
            pass
        elif filter == "shepp-logan":
            # Start from first element to avoid divide by zero
            fourier_filter[1:] *= np.sin(omega[1:] / 2) / (omega[1:] / 2)
        elif filter == "cosine":
            freq = (0.5 * np.arange(0, projection_size_padded)
                    / projection_size_padded)
            cosine_filter = np.fft.fftshift(np.sin(2 * np.pi * np.abs(freq)))
            fourier_filter *= cosine_filter
        elif filter == "hamming":
            hamming_filter = np.fft.fftshift(np.hamming(projection_size_padded))
            fourier_filter *= hamming_filter
        elif filter == "hann":
            hanning_filter = np.fft.fftshift(np.hanning(projection_size_padded))
            fourier_filter *= hanning_filter
        elif filter is None:
            fourier_filter[:] = 1
        else:
            raise ValueError("Unknown filter: %s" % filter)
        # Apply filter in Fourier domain
        projection = fft(img, axis=0) * fourier_filter[:, np.newaxis]
        radon_filtered = np.real(ifft(projection, axis=0))

        # Resize filtered image back to original size
        radon_filtered = radon_filtered[:radon_image.shape[0], :]
        reconstructed = np.zeros((output_size, output_size))
        # Determine the center of the projections (= center of sinogram)
        mid_index = np.ceil(radon_image.shape[0] / 2)

        [X, Y] = np.mgrid[1:output_size+1, 1:output_size+1]
        xpr = X - int(output_size) // 2
        ypr = Y - int(output_size) // 2
        
        # pad the filtered image
        padded_size = 2*np.ceil(output_size/np.sqrt(2)) + 1
        if radon_image.shape[0] < padded_size:
            num_extra_rows = padded_size - radon_image.shape[0]
            pad_width = ((int(np.ceil(num_extra_rows/2)),int(np.floor(num_extra_rows/2))), (0,0))
            radon_filtered = np.pad(radon_filtered, pad_width, mode='constant', constant_values=0)
            mid_index += np.ceil(num_extra_rows/2)

        # Reconstruct image by interpolation
        for i in range(len(theta)):
            t = ypr * np.cos(th[i]) - xpr * np.sin(th[i])
            x = np.arange(1, radon_filtered.shape[0]+1) - mid_index
            if interpolation == 'linear':
                backprojected = np.interp(t, x, radon_filtered[:, i],
                                          left=0, right=0)
            else:
                interpolant = interp1d(x, radon_filtered[:, i], kind=interpolation,
                                       bounds_error=False, fill_value=0)
                backprojected = interpolant(t)
            reconstructed += backprojected
        if circle:
            radius = output_size // 2
            reconstruction_circle = (xpr ** 2 + ypr ** 2) <= radius ** 2
            reconstructed[~reconstruction_circle] = 0.

        return reconstructed * np.pi / (2 * len(th))

    def _sinogram_circle_to_square(sinogram):
        diagonal = int(np.ceil(np.sqrt(2) * sinogram.shape[0]))
        pad = diagonal - sinogram.shape[0]
        old_center = sinogram.shape[0] // 2
        new_center = diagonal // 2
        pad_before = new_center - old_center
        pad_width = ((pad_before, pad - pad_before), (0, 0))
        return np.pad(sinogram, pad_width, mode='constant', constant_values=0)
    
    ###### end iradon_local reference

    # TODO: consider replacing with our own csv reading wrapper
    #df = pandas.read_csv(filepath, skiprows=1, sep=',\t', engine='python', parse_dates=[0])
    df = pandas.read_csv(filepath,skiprows=1,sep=',\t',engine='python',date_format='%d/%m/%Y %I:%M:%S %p')

    # acquisition_time = df[df.columns[0]].values
    rotations = df[df.columns[1]].values
    positions = df[df.columns[2]].values
    coincidence_counts = df[df.columns[3]].values

    # determine number of points in each axis of the scan
    unique_angles = np.unique(rotations)
    unique_positions = np.unique(positions)

    # reshape coincident counts array
    #
    # Note: The array dimensions are swapped between MATLAB and Python.
    #       This avoids the need to transpose as you do in MATLAB because 
    #       of the different scan order during reshape between MATLAB and 
    #       Python. See: https://docs.scipy.org/doc/numpy-1.15.0/user/numpy-for-matlab-users.html#notes
    coincidence_counts.shape = (len(unique_positions), len(unique_angles))

    plt.figure()
    plt.imshow(coincidence_counts, extent=[np.min(unique_angles), np.max(unique_angles), np.max(unique_positions), np.min(unique_positions)], interpolation='none')
    plt.xlabel(r'$\theta$')
    plt.ylabel('x')
    plt.title('Sinogram of {filename}'.format(filename=os.path.basename(filepath)))

    # do the inverse transform
    if filter_name is not None:
        if npoints is None:
            raise RuntimeError('When calling pet_rebuild with a filter, you must specify the number of points to reconstruct')

        # convert string none to actual None
        if filter_name == 'none':
            filter_name = None
        inverse = iradon_local(coincidence_counts, unique_angles, output_size=npoints, filter=filter_name, interpolation='linear', circle=False)

        plt.figure()
        plt.imshow(inverse, extent=[0, 1, 0, 1], interpolation='none')
        plt.title('Reconstruction of {filename}'.format(filename=os.path.basename(filepath)))

    if call_show:
        plt.show()
        
        

    return coincidence_counts
