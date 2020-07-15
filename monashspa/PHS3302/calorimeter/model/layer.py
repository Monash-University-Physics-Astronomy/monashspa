import random

class Layer:
    '''Defines an individual layer of a calorimeter. The properties of the layer are
    name, its material given as X0 per cm, the thickness, the response measuring the
    level of ionisation (in arbitrary units, zero for passive layer). The layer can
    keep track of the ionisation in it.'''

    def __init__(self, name, material, thickness, response=1.0):
        self._name = name
        self._material = material
        self._thickness = thickness
        self._yield = response
        self._ionisation = 0

    def ionise(self, particle, step):
        '''Records the ionisation in each layer from a particle going a certain length.'''
        if particle.ionise:
            self._ionisation += self._yield*step

    def interact(self, particle, step):
        '''Let a particle interact (bremsstrahlung or pair production). The interaction
        length is assumed to be the same for electrons and photons.'''
        material = self._material*step
        particles = [particle]
        if random.random() < material:
            particles = particle.interact()

        return particles

    def __str__(self):
        return f'{self._name:10} {self._material:.3f} {self._thickness:.2f} cm {self._ionisation:.3f}'
