import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D

class Calorimeter:
    '''This defines the calorimeter. The model is a strict one dimensinal model,
    where layers are positioned along the positive z direction and are imagined to
    stretch infinitely into the x and y directions.'''

    class Volume:
        '''A simple volume of the detector that has a layer starting at a given z position'''

        def __init__(self, z, layer):
            self.z = z
            self.layer = layer

    def __init__(self, layers=[]):
        self._layers = layers.copy()
        self._zend = 0
        self._trace_enabled = False
        self._particle_traces = []

    def add_layer(self, layer):
        '''Add a single layer to the back of the calorimeter.'''
        self._layers.append(self.Volume(self._zend, copy.copy(layer)))
        self._zend += layer._thickness

    def add_layers(self, layers):
        '''Add a list of layers, one after the other to the back of the calorimeter.'''
        for l in layers:
            self.add_layer(l)

    def step(self, particle, step):
        '''Move a particle by the amount step forward in the calorimeter,
        Return a list of particles created during
        the step. If particle doesn't do anything it is just stepped forward.
        If trace is enabled, records the particle trajectory.'''

        involume = False
        for volume in self._layers:
            if (particle.z >= volume.z) and (particle.z < volume.z + volume.layer._thickness):
                involume = True
                break

        particle.move(step)

        particles = [particle]
        if involume:
            layer = volume.layer
            layer.ionise(particle, step)
            particles = layer.interact(particle, step)

        return particles

    def positions(self, active=True):
        '''Provide an array of the z coordinates for the start of each layer. If active=True, only return the active layers'''
        return np.array([v.z for v in self._layers if not active or v.layer._yield>0])

    def ionisations(self, active=True):
        '''Provide a list of the ionisation deposited in each of the layers. If active=True, only return the active layers'''
        return np.array([v.layer._ionisation for v in self._layers if not active or v.layer._yield>0])

    def reset(self):
        '''Clears the recorded ionisation in each layer and particle traces'''
        for v in self._layers:
            v.layer._ionisation=0
        self._particle_traces = []

    def __str__(self):
        txt = 'The layers of the calorimeter:\n'
        for volume in self._layers:
            txt += f'{volume.z:.2f} ' + str(volume.layer) + '\n'
        return txt

    def enable_tracing(self):
        '''Enable particle trajectory tracing. Note: This is computationally expensive and should
        only be used for a single ingoing particle.'''
        self._trace_enabled = True

    def disable_tracing(self):
        '''Disable particle trajectory tracing.'''
        self._trace_enabled = False

    def get_particle_traces(self):
        '''Return the recorded particle traces as a list of (particle, trace_list) tuples.
        Each trace_list contains (z, x, y) positions along the particle trajectory.'''
        return self._particle_traces

    def record_trace(self, particle):
        '''Record the final trajectory of a particle.'''
        if self._trace_enabled and particle.trace and (particle.type in ('elec', 'muon')):
            # Add final position to the trace
            final_trace = particle.trace + [(particle.z, particle.x, particle.y)]
            self._particle_traces.append((particle, final_trace))

    def draw(self, ax=None, extend=15, show_traces=False):
        '''Draw the calorimeter design with z-axis horizontal.
        
        Parameters:
        -----------
        ax : matplotlib.axes.Axes, optional
            The axes to draw on. If None, creates a new figure.
        extend : float, optional
            The perpendicular extent of the calorimeter (default: 10).
        show_traces : bool, optional
            If True, overlay recorded particle trajectories (default: False).
            
        Returns:
        --------
        matplotlib.axes.Axes
            The axes containing the drawing.
        '''
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 6))
        
        # Colors: blue for active layers, gray for passive layers
        active_color = '#1f77b4'    # Blue
        passive_color = '#999999'   # Gray
        
        # Draw each layer
        for volume in self._layers:
            z_start = volume.z
            thickness = volume.layer._thickness
            
            # Determine color based on whether layer is active
            color = active_color if volume.layer._yield > 0 else passive_color
            
            # Create rectangle: (z_start, -extend/2), width=thickness, height=extend
            rect = patches.Rectangle(
                (z_start, -extend/2),
                thickness,
                extend,
                linewidth=1,
                edgecolor='black',
                facecolor=color,
                alpha=0.7
            )
            ax.add_patch(rect)
        
        # Draw particle traces if enabled
        electron_color = '#d62728'  # Red
        muon_color = '#2ca02c'      # Green
        has_electron_trace = False
        has_muon_trace = False
        if show_traces and self._particle_traces:
            for particle, trace in self._particle_traces:
                if particle.type not in ('elec', 'muon'):
                    continue
                if len(trace) > 1:
                    z_coords = [pos[0] for pos in trace]
                    x_coords = [pos[1] for pos in trace]
                    color = electron_color if particle.type == 'elec' else muon_color
                    ax.plot(z_coords, x_coords, '-', color=color, linewidth=1.0, alpha=0.03)
                    if particle.type == 'elec':
                        has_electron_trace = True
                    else:
                        has_muon_trace = True
                    
        # Set axis properties
        ax.set_xlim(-0.5, self._zend + 0.5)
        ax.set_ylim(-extend/2 - 1, extend/2 + 3)
        ax.set_xlabel('z position (cm)', fontsize=12)
        ax.set_ylabel('Perpendicular extent (cm)', fontsize=12)
        ax.set_title('Calorimeter Design', fontsize=14, fontweight='bold')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        # Add legend
        active_patch = patches.Patch(color=active_color, alpha=0.7, label='Active layer')
        passive_patch = patches.Patch(color=passive_color, alpha=0.7, label='Passive layer')
        legend_handles = [active_patch, passive_patch]
        if show_traces:
            if has_electron_trace:
                legend_handles.append(Line2D([0],[0], color=electron_color, lw=2, label='Electron traces'))
            if has_muon_trace:
                legend_handles.append(Line2D([0],[0], color=muon_color, lw=2, label='Muon traces'))
        ax.legend(handles=legend_handles, loc='upper right')
        
        return ax


