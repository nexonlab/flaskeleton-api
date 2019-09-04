class Campus(object):

    def __init__(self, codigo:int):
        self.codigo = codigo

    def __repr__(self):
        return "<Campus codigo={codigo}>".format(codigo=self.codigo)
