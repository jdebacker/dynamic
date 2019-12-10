'''
------------------------------------------------------------------------
This script takes a Frisch elasticity parameter and then estimates the
parameters of the elliptical utility fuction that correspond to a
constant Frisch elasticity function with the input Frisch elasticity.
------------------------------------------------------------------------
'''
# Import packages
import numpy as np
import scipy.optimize as opt


def sumsq(params, *objs):
    '''
    This function generates the sum of squared deviations between the
    constant Frisch elasticity function and the elliptical utility
    function.

    Args:
        params (tuple): parameters to estimate, (b, k, upsilon)
        objs (tuple): other parameters of utility function,
            (theta, l_tilde, n_grid)

    Returns:
        ssqdev (scalar): sum of squared errors

    '''
    theta, l_tilde, n_grid = objs
    b, k, upsilon = params
    CFE = ((n_grid / l_tilde) ** (1 + theta)) / (1 + theta)
    ellipse = (b * ((1 - ((n_grid / l_tilde) ** upsilon)) **
                    (1 / upsilon)) + k)
    errors = CFE - ellipse
    ssqdev = (errors ** 2).sum()
    return ssqdev


def sumsq_MU(params, *objs):
    '''
    This function generates the sum of squared deviations between the
    marginals of the constant Frisch elasticity function and the
    elliptical utility function
        Args:
            params (tuple): parameters to estimate, (b, k, upsilon)
            objs (tuple): other parameters of utility function,
                (theta, l_tilde, n_grid)

        Returns:
            ssqdev (scalar): sum of squared errors

    '''
    theta, l_tilde, n_grid = objs
    b, upsilon = params
    CFE_MU = (1.0 / l_tilde) * ((n_grid / l_tilde) ** theta)
    ellipse_MU = (b * (1.0 / l_tilde) * ((1.0 - (n_grid / l_tilde) **
                                          upsilon) **
                                         ((1.0 / upsilon) - 1.0)) *
                  (n_grid / l_tilde) ** (upsilon - 1.0))
    errors = CFE_MU - ellipse_MU
    ssqdev = (errors ** 2).sum()
    return ssqdev


def estimation(frisch, l_tilde):
    '''
    This function estimates the parameters of an elliptical utility
    funcion that fits a constant frisch elasticty function.

    Args:
        frisch (scalar):  Frisch elasticity of labor supply
        l_tilde (scalar): maximum amount of labor supply

    Returns:
        b_MU_til (scalar): estimated b from ellipitical utility function
        upsilon_MU_til (scalar): estimated upsilon from ellipitical
            utility function

    '''

    '''
    ------------------------------------------------------------------------
    Set parameters
    ------------------------------------------------------------------------
    '''
    theta = 1 / frisch
    N = 101
    graph = False
    '''
    ------------------------------------------------------------------------
    Estimate parameters of ellipitical utility function
    ------------------------------------------------------------------------
    '''
    # Initial guesses
    b_init = .6701
    # k_init = -.6548
    upsilon_init = 2.3499
    # don't estimate near edge of range of labor supply
    n_grid = np.linspace(0.01, 0.8, num=N)

    # Estimating using levels of utility function
    # ellipse_params_init = np.array([b_init, k_init, upsilon_init])
    # ellipse_objs = (theta, l_tilde, n_grid)
    # bnds = ((None, None), (None, None), (1e-12, None))
    # ellipse_params_til = opt.minimize(sumsq, ellipse_params_init,
    #                     args=(ellipse_objs), method="L-BFGS-B", bounds=bnds,
    #                     tol=1e-15)
    # (b_til, k_til, upsilon_til) = ellipse_params_til.x

    # elapsed_time = time.clock() - start_time

    # Estimate params using marginal utilities
    ellipse_MU_params_init = np.array([b_init, upsilon_init])
    ellipse_MU_objs = (theta, l_tilde, n_grid)
    bnds_MU = ((None, None), (None, None))
    ellipse_MU_params_til = opt.minimize(sumsq_MU,
                                         ellipse_MU_params_init,
                                         args=(ellipse_MU_objs),
                                         method="L-BFGS-B",
                                         bounds=bnds_MU, tol=1e-15)
    (b_MU_til, upsilon_MU_til) = ellipse_MU_params_til.x

    return b_MU_til, upsilon_MU_til
