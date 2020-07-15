import random

class Particle:
    '''Base class for particles'''

    def __init__(self, type, z, energy, ionise, cutoff):
        self.type = type
        self.z = z
        self.energy = energy
        self.ionise = ionise
        self.cutoff = cutoff

    def move(self, step):
        self.z += step

    def interact(self):
        '''This should implement the model for interaction.
        The base class particle doesn't interact at all'''
        return [particle]

    def __str__(self):
        return f'{self.type:10} z:{self.z:.3f} E:{self.energy:.3f}'


class Electron(Particle):

    def __init__(self, z, energy):
        super(Electron, self).__init__('elec', z, energy, True, 0.01)

    def interact(self):
        '''An electron radiates a photon. Make the energy split evenly.'''
        particles = []
        if self.energy > self.cutoff:
            split = random.random()
            particles = [Electron(self.z, split*self.energy), Photon(self.z, (1.0-split)*self.energy)]
        return particles


class Photon(Particle):

    def __init__(self, z, energy):
        super(Photon, self).__init__('phot', z, energy, False, 0.01)

    def interact(self):
        '''A photon splits into an electron and a positron. Make the energy split evenly.'''
        particles = []
        if self.energy > self.cutoff:
            split = random.random()
            particles = [Electron(self.z, split*self.energy), Electron(self.z, (1.0-split)*self.energy)]
        return particles


class Muon(Particle):

    def __init__(self, z, energy):
        super(Muon, self).__init__('muon', z, energy, True, 0.01)
