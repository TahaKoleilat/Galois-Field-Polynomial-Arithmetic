def polynomialDegree(x):
    return x.bit_length() - 1

def polynomialExtendedEuclid(x, y,irreduciblePolynomial):
    A = (x, 1, 0)
    B = (y, 0, 1)
    while True:
        quotient, remainder = polynomialDivision(A[0], B[0])
        if remainder == 0: 
            return B
        A, B = B, (remainder, A[1] ^ polynomialMultiply(quotient, B[1],irreduciblePolynomial), A[2] ^ polynomialMultiply(quotient, B[2],irreduciblePolynomial))
    
def polynomialAdd(x, y, irreduciblePolynomial):
    output = x ^ y #Subtraction is same as addition here since we are dealing with Galois Field 2^m
    degree = polynomialDegree(irreduciblePolynomial)
    if(polynomialDegree(output) > degree): #in case the result needs to be reduced
        output = moduloReduction(output,irreduciblePolynomial)
    return output

def polynomialSubtract(x, y, irreduciblePolynomial):
    output = x ^ y #Subtraction is same as addition here since we are dealing with Galois Field 2^m
    degree = polynomialDegree(irreduciblePolynomial)
    if(polynomialDegree(output) > degree): #in case the result needs to be reduced
        output = moduloReduction(output,irreduciblePolynomial)
    return output

def polynomialDivision(x, y):
    quotient = 0
    bitLength = y.bit_length()
    remainder = x
    while(1):
        multiplyTerm = remainder.bit_length() - bitLength #How much to shift
        if multiplyTerm < 0: #Cant divide further
            return (quotient, remainder) #return both the quotient and the remainder
        quotient = quotient ^ (1 << multiplyTerm) #add (which is equivalent to xor) the term with its power
        remainder = remainder ^ (y << multiplyTerm) #subtract to get remainder

def polynomialMultiply(x, y, irreduciblePolynomial):
    output = 0; 
    degree = polynomialDegree(irreduciblePolynomial)
    if(polynomialDegree(y) > degree): #in case y needs to be reduced
        y= moduloReduction(y,irreduciblePolynomial)
    if(polynomialDegree(x) > degree): #in case x needs to be reduced
        x= moduloReduction(x,irreduciblePolynomial)
    while(x and y):
        if x & 1: #if least significant bit of x is 1 then add y else nothing is done
            output = output ^ y #adding the multiplied terms
        x = x >> 1 #to compute the other powers of x
        y = y << 1 #shift by 1 bit which is equivalent to multiplying by x
        if (y >> degree) & 1: #if MSB of y is 1 then we should reduce the polynomial
            y =  y ^ irreduciblePolynomial
    return output

def moduloReduction(x, irreduciblePolynomial):
    quotient, remainder = polynomialDivision(x,irreduciblePolynomial) #reduce the polynomial in case it's degree is higher than the degree of the irreducible polynomial
    return remainder

def polynomialMultiplicativeInverse(x, irreduciblePolynomial):
    remainder, inverse, temp = polynomialExtendedEuclid(x, irreduciblePolynomial,irreduciblePolynomial)
    if(remainder == 1):
        return inverse
    return "Inverse does not exist"

