# encoding=utf-8


class A:
    action = '[action A]'

    def __init__(self):
        print 'new A'
        return

    def a(self):
        print 'A.a ' + self.action

    def b(self):
        print 'A.b ' + self.action

    @staticmethod
    def c(p):
        print 'here is static method from a ' + p


class B(A):
    def __init__(self):
        print 'in new B'
        self.action = '[action B]'
        print 'out new B'

    def a(self):
        print 'B.a ' + self.action


a = A()
b = B()

a.a()
a.b()
b.a()
b.b()
b.c('f')
