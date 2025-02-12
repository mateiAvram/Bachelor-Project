import numpy as np
from scipy.stats import beta
import scipy.optimize as opt

def beta_percentiles(mode, low_bound, high_bound):
    def mode_equation(a):
        b = (a - 1) / mode + 2 - a
        return (a - 1) / (a + b - 2) - mode

    def range_equation(params):
        a, b = params
        low_eq = beta.ppf(0.15, a, b) - low_bound
        high_eq = beta.ppf(0.85, a, b) - high_bound
        return [low_eq, high_eq]
    
    # Solve for a
    a_initial_guess = 2
    a_solution = opt.root_scalar(mode_equation, bracket=[1.1, 10], method='bisect').root
    
    # Solve for b given a
    b_solution = (a_solution - 1) / mode + 2 - a_solution
    
    # Refine a and b together
    a, b = opt.fsolve(range_equation, [a_solution, b_solution])
    
    return a, b

def transform_range(val, min_val, max_val):
    return (val - min_val) / (max_val - min_val)

def inverse_transform_range(val, min_val, max_val):
    return val * (max_val - min_val) + min_val

def find_beta_params(mode, data_range, min_val=0, max_val=100):
    transformed_mode = transform_range(mode, min_val, max_val)
    transformed_low_bound = transform_range(data_range[0], min_val, max_val)
    transformed_high_bound = transform_range(data_range[1], min_val, max_val)
    
    a, b = beta_percentiles(transformed_mode, transformed_low_bound, transformed_high_bound)
    return a, b

# Example usage
mode = int(input('Mode: '))
lower_bound = int(input('Lower Bound: '))
higher_bound = int(input('Higher Bound: '))
data_range = [lower_bound, higher_bound]
a, b = find_beta_params(mode, data_range)
print(f"a: {a}, b: {b}")