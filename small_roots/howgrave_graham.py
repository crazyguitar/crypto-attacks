import logging

from sage.all import Matrix
from sage.all import ZZ


def modular_univariate(f, modulus, m, t, bound):
    """
    Computes small modular roots of a univariate polynomial.
    More information: May A., "New RSA Vulnerabilities Using Lattice Reduction Methods"
    :param f: the polynomial
    :param modulus: the modulus
    :param m: the amount of normal shifts to use
    :param t: the amount of additional shifts to use
    :param bound: an approximate bound on the roots
    :return: a generator generating small roots of the polynomial
    """
    f = f.monic().change_ring(ZZ)
    x = f.parent().gen()
    d = f.degree()

    lattice = Matrix(d * m + t)
    row = 0
    logging.debug("Generating normal shifts...")
    for i in range(m):
        for j in range(d):
            shift = (x * bound) ** j * modulus ** (m - i) * f(x * bound) ** i
            for col in range(row + 1):
                lattice[row, col] = shift[col]

            row += 1

    logging.debug("Generating additional shifts...")
    for i in range(t):
        shift = (x * bound) ** i * f(x * bound) ** m
        for col in range(row + 1):
            lattice[row, col] = shift[col]

        row += 1

    logging.debug("Executing the LLL algorithm...")
    basis = lattice.LLL()

    logging.debug("Reconstructing polynomials...")
    for row in range(basis.nrows()):
        new_polynomial = 0
        for col in range(basis.ncols()):
            new_polynomial += (basis[row, col] // bound ** col) * x ** col

        for root in new_polynomial.roots():
            yield int(root[0])