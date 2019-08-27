import functools


def meu_decorator(f):
    @functools.wraps(f)
    def processa_f(*args, **kwargs):
        print("antes de exec f")
        f(*args, **kwargs)
        print("depois de exec f")
    return processa_f


@meu_decorator
def minha_funcao():
    print('Minha funcao.')


@meu_decorator
def soma(x, y):
    print("soma =", format(x+y))


if __name__ == "__main__":
    minha_funcao()
    soma(10, 12)
