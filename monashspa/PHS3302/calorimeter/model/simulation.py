import copy
import numpy as np

class Simulation:
    '''A simulation is defined by a calorimeter. Then individual simulation runs can be created by
    running the same particle through the calorimter multiple times.'''
    def __init__(self, calorimeter):
        self._calorimeter = calorimeter

    def simulate(self, particle, number):
        '''Run a individual simulation. The ingoing particle is simulated going
        through the calorimeter "number" times. A 2D array is returned with the
        first axis the ionisation in the individual layers and the second corresponding to each
        new particle.'''
        ionisations = []

        for i in range(number):

            self._calorimeter.reset()
            particles = [copy.copy(particle)]
            step = 0
            while step < 10000:
                next = []
                for p in particles:
                    newparticles = self._calorimeter.step(p, 0.1)
                    next.extend(newparticles)
                particles = next
                step += 1

            ionisations.append(self._calorimeter.ionisations())

        allionisations = np.stack(ionisations, axis=0)
        return allionisations
