import os
import sys
import matplotlib


#import matplotlib.pyplot as plt
#plt.plot([[1,2,3,4],[4,3,2,1], [2,2,3,3]])
#plt.ylabel('some numbers')
#plt.show()


help(matplotlib)

class Plotter(object):
    def __init__(self):
        print("Plotter constructor")

    def __del__(self):
        print("Plotter destructor")




def main():
    pass


if __name__ == "__main__":
    main()