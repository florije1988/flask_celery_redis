# -*- coding: utf-8 -*-
__author__ = 'florije'

from nothing import add

if __name__ == '__main__':
    for i in range(100):
        for j in range(100):
            kk = add.delay(i, j)
            kk.ready()
            kk.get()