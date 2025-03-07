#implementing SIGW - PBH model: broad and flat power spectrum (see the power spectrum in de Luca 2207.08638,  and the GW density in Pi and Sasaki, 2005.12306v2)

import os
import numpy as np
import ptarcade.models_utils as aux

name = 'sigw_box'

smbhb = False

parameters = {
    'log10_fmin' : aux.prior("Uniform", -11, -5),
    'log10_fmax' : aux.prior("Uniform", -11, -5),
    'log10_A' : aux.prior("Uniform", -3,1),
    }

cwd = os.path.dirname(os.path.abspath(__file__))
spectrum_file = aux.spec_importer(cwd + '/models_data/sigw_box.h5')

def spectrum(f, log10_A, log10_fmin , log10_fmax):
    
    """Calculate GW energy density.

    Returns the GW energy density as a fraction of the closure density as a
    function of the parameters of the model:

    :param float f: Frequency in Hz. The power spectrum assumes a constant value at frequencies between f_min and f_max
    :param float log10_f_min: Minimum frequency in Hz in log10 space.
    :param float log10_f_max: Maximum frequency in Hz in log10 space.
    :param float log10_A: Dimensionless scaling factor in log10 space.
    :returns: GW energy density as a fraction of the closure density.
    :rtype: float
    """
    
    A = 10**log10_A

    prefactor = ( # assumes f_reheating > f 
        (aux.omega_r) * (aux.g_rho(f, is_freq=True) / aux.g_rho_0) *
        (aux.g_s_0 / aux.g_s(f, is_freq=True))**(4/3)
        )
    
    return aux.h**2 * A**2 * prefactor * 10**spectrum_file(np.log10(f), log10_fmin = log10_fmin, log10_fmax = log10_fmax)
