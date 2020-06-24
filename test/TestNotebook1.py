import numpy as np
import fire

def hello(name="world"):
    print("hello {}".format(name), np.random.rand(1)[0])
if __name__ == '__main__': 
    fire.Fire(hello)