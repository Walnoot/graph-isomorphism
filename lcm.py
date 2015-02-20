def factorize(x):
    factors = {}
    i = 2
    while x > 1:
        if x % i == 0:
            x //= i
            factors[i] = factors.get(i, 0) + 1
        else:
            i += 1
    return factors


def lcm(integers):
    assert len(integers) > 0
    if len(integers) == 1:
        return integers[0]
    else:
        factorizations = {}
        for l in integers:
            if l not in factorizations:
                factorizations[l] = factorize(l)
        factors = {}
        for factorization in factorizations:
            for factor in factorizations[factorization]:
                if factor not in factors or factorizations[factorization][factor] > factors[factor]:
                    factors[factor] = factorizations[factorization][factor]
        result = 1
        for f in factors:
            result *= f ** factors[f]
        return result


def gcd(a, b):
    return a * b // lcm([a, b])