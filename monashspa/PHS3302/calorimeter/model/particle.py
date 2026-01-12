import random

class Particle:
    '''Base class for particles'''

    def __init__(self, type, z, energy, ionise, cutoff, x=0, y=0, angle_x=0, angle_y=0, trace=None):
        self.type = type
        self.z = z
        self.energy = energy
        self.ionise = ionise
        self.cutoff = cutoff
        self.x = x  # Transverse position (x-direction)
        self.y = y  # Transverse position (y-direction)
        self.angle_x = angle_x  # Angle with respect to z-axis in x-z plane
        self.angle_y = angle_y  # Angle with respect to z-axis in y-z plane
        self.trace = trace if trace is not None else []  # List of (z, x, y) positions

    def move(self, step):
        '''Move the particle forward by step, updating transverse position based on angle'''
        # Record current position before moving
        self.trace.append((self.z, self.x, self.y))
        
        # Update transverse positions based on angles
        self.x += step * self.angle_x
        self.y += step * self.angle_y
        
        # Move forward in z
        self.z += step

    def interact(self):
        '''This should implement the model for interaction.
        The base class particle doesn't interact at all'''
        return [self]

    def __str__(self):
        return f'{self.type:10} z:{self.z:.3f} E:{self.energy:.3f}'


class Electron(Particle):

    def __init__(self, z, energy, x=0, y=0, angle_x=0, angle_y=0, trace=None):
        super(Electron, self).__init__('elec', z, energy, True, 0.01, x, y, angle_x, angle_y, trace)

    def interact(self):
        '''An electron radiates a photon. Make the energy split evenly.
        New particles are created with a small random scattering angle.'''
        particles = []
        if self.energy > self.cutoff:
            split = random.random()
            # Small scattering angles (in radians) - approximately 1-10 degrees
            angle_sigma = 0.02  # Standard deviation of scattering angle
            new_angle_x = self.angle_x + random.gauss(0, angle_sigma)
            new_angle_y = self.angle_y + random.gauss(0, angle_sigma)
            
            particles = [
                Electron(self.z, split*self.energy, self.x, self.y, new_angle_x, new_angle_y, self.trace.copy()),
                Photon(self.z, (1.0-split)*self.energy, self.x, self.y, new_angle_x, new_angle_y, self.trace.copy())
            ]
        return particles


class Photon(Particle):

    def __init__(self, z, energy, x=0, y=0, angle_x=0, angle_y=0, trace=None):
        super(Photon, self).__init__('phot', z, energy, False, 0.01, x, y, angle_x, angle_y, trace)

    def interact(self):
        '''A photon splits into an electron and a positron. Make the energy split evenly.
        New particles are created with a small random scattering angle.'''
        particles = []
        if self.energy > self.cutoff:
            split = random.random()
            # Small scattering angles (in radians) - approximately 1-10 degrees
            angle_sigma = 0.05  # Standard deviation of scattering angle
            new_angle_x = self.angle_x + random.gauss(0, angle_sigma)
            new_angle_y = self.angle_y + random.gauss(0, angle_sigma)
            
            particles = [
                Electron(self.z, split*self.energy, self.x, self.y, new_angle_x, new_angle_y, self.trace.copy()),
                Electron(self.z, (1.0-split)*self.energy, self.x, self.y, new_angle_x, new_angle_y, self.trace.copy())
            ]
        return particles


class Muon(Particle):

    def __init__(self, z, energy, x=0, y=0, angle_x=0, angle_y=0, trace=None):
        super(Muon, self).__init__('muon', z, energy, True, 0.01, x, y, angle_x, angle_y, trace)
