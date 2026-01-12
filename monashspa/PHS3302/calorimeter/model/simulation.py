import copy
import numpy as np
from collections import deque
from multiprocessing import Pool
import multiprocessing as mp


def _run_single_simulation(args):
    '''Helper function for parallel simulation of individual particles.
    Takes a tuple of (calorimeter, particle, step_size) and returns ionisations.'''
    calorimeter, particle, step_size = args
    
    calorimeter.reset()
    particles = deque([copy.copy(particle)])
    
    while particles:
        p = particles.popleft()
        newparticles = calorimeter.step(p, step_size)
        # Only add particles that are still in the calorimeter
        for np_p in newparticles:
            if np_p.z < calorimeter._zend:
                particles.append(np_p)
            elif calorimeter._trace_enabled:
                # Record trace when particle exits calorimeter
                calorimeter.record_trace(np_p)

    return calorimeter.ionisations()


class Simulation:
    '''A simulation is defined by a calorimeter. Then individual simulation runs can be created by
    running the same particle through the calorimter multiple times.'''
    def __init__(self, calorimeter):
        self._calorimeter = calorimeter

    
    def simulate(self, particle, number, deadcellfraction=0.0):
        '''Run a individual simulation. The ingoing particle is simulated going
        through the calorimeter "number" times. A 2D array is returned with the
        first axis the ionisation in the individual layers and the second corresponding to each
        new particle.
        
        Uses multiprocessing to parallelize individual particle simulations across available CPU cores.'''
        # Prepare arguments for parallel execution
        args_list = [(copy.deepcopy(self._calorimeter), particle, 0.1) for _ in range(number)]
        
        # Use all available CPU cores for parallel simulation
        num_cores = mp.cpu_count()
        
        with Pool(num_cores) as pool:
            ionisations = pool.map(_run_single_simulation, args_list)

        allionisations = np.stack(ionisations, axis=0)
        mask = np.random.random(allionisations.shape) < deadcellfraction
        allionisations[mask] = 0
        return allionisations

    def simulate_with_tracing(self, particle, deadcellfraction=0.0):
        '''Run a single simulation with particle trajectory tracing enabled.
        This records the path of all particles created during the shower.
        Note: This is computationally expensive and should only be used for
        a single ingoing particle (number=1).
        
        Returns:
        --------
        tuple : (ionisations, calorimeter)
            ionisations: Array of ionisation deposited in each layer
            calorimeter: The calorimeter object containing the recorded particle traces
        '''
        # Create a fresh copy of the calorimeter
        cal = copy.deepcopy(self._calorimeter)
        cal.enable_tracing()
        cal.reset()
        
        particles = deque([copy.copy(particle)])
        all_particles = []
        
        while particles:
            p = particles.popleft()
            newparticles = cal.step(p, 0.1)
            
            # If no new particles created (energy below cutoff), record the current particle
            if not newparticles:
                all_particles.append(p)
            else:
                # Add all returned particles back to queue if still in calorimeter
                for np_p in newparticles:
                    if np_p.z < cal._zend:
                        particles.append(np_p)
                    else:
                        # Record particles that exit the calorimeter
                        all_particles.append(np_p)
        
        # Record all final particles
        for p in all_particles:
            cal.record_trace(p)
        
        ionisations = cal.ionisations()
        mask = np.random.random(ionisations.shape) < deadcellfraction
        ionisations[mask] = 0
        
        return ionisations, cal
