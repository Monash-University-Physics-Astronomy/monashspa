from .optical_tweezers import trap_k_theory as __trap_k_theory

def model_1(r, w, I):
    # scale parameters
    r = r*1e-3
    w = w*1e-4
    I = I*1e11
    
    # set parameters we are not exposing
    eccentricity = 1.1
    alpha = 1.25

    return __trap_k_theory(r, w, alpha, eccentricity, I)