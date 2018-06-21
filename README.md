# symm
A package to measure the symmetry of 1D data and find the optimal symmetry axis in this data

# Usage
Given data points as an array of tuples (x,y). Then just call

    from symm.symmetry import Symmetry

    data_xy = [(1,2), (2,3), (3,4), ...]
    
    symm = Symmetry(data_xy)
    
    # Calculate the symmetry given a axis at x_0 = 3
    print("Data symmetry is %s at symmetry axis 3" % symm.symmetry(3))
    
    # Find the optimal symmetry axis
    axis = symm.optimize_symmetry()
    print("Optimal symmetry axis at %s with symmetry-measure of %s" %(axis.x, axis.fun))
    
    # Remove some data-points in order to achieve better symmetry
    symm_improved = symm.make_symmetric()
    new_axis = symm_improved.optimize_symmetry()



# Symmetry measurement
Given a function f: R -> R. The symmetry of this function with respect to the symmetry axis x_0 in R is defined as 

 || f ||_sym(x_0) := 1/||f||L² * sqrt( Integral(-infty, infty) |f(x_0 - x) - f(x_0 + x)|² dx),
 
 where ||f||L² is the L^2-Norm, defined as 
 (|| f ||L²)^2 := Integral(-infty, infty) | f(x) |² dx

For discrete functions, one defines analogously
 
 || f ||_sym(x_0) := 1/||f||l² * sqrt( sum_k=0^N | f(x_0 - x_k) - f(x_0 + x_k) |²) 
 
 where f is interpolated in between, such that one can evaluate f(x_0 - x_k), f(x_0 + x_k), resp. In this case, the ||f||l² norm is just the usual L^2 norm, but using the interpolated function. Alternatively, one could also use the plain l2 norm in sequence space, see https://en.wikipedia.org/wiki/Sequence_space#ℓp_spaces, by setting all elements larger than N to zero.
 
 In this library, we interpolate using the scipy package with a Spline of order 3 in the region of points, and outside we set the function to 0.
 
The optimization routine to find the best position of the symmetry axis x_0 uses the scipy minimize function using the Nelder-Mead algorithm.

Furthermore, if the data is not distributed symmetrically itself around the optimal symmetry axis, then one can make the data 'symmetrically' distributed around any axis, using the function ```make_symmetric(x_axis)```.
The function will just delete as many elements, such that the number left to the axis and right to the axis is the same, i.e. we assume that the spacing between the data points is always the same.
