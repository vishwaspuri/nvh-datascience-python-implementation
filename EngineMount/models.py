import numpy as np
import math

class Mount:
    # Defining coordinates of mounts and angles 
    def __init__(
            self, 
            x=0, 
            y=0, 
            z=0, 
            k_x=0, 
            k_y=0, 
            k_z=0, 
            n_x=0, 
            n_y=0, 
            n_z=0
        ):
        self.x = x
        self.y = y
        self.z = z
        self.k_x = k_x
        self.k_y = k_y
        self.k_z = k_z
        self.n_x = n_x
        self.n_y = n_y
        self.n_z = n_z

    def __str__(self):
        return self.x
    

    def local_stiffness_matrix(self):
        stiffness_matrix = np.array([
            [self.k_x*np.complex(1, self.n_x), 0, 0],
            [0, self.k_y*np.complex(1, self.n_y), 0],
            [0, 0, self.k_z*np.complex(1, self.n_z)]
        ])
        print('working')
        return stiffness_matrix 
    
    def g_matrix(self):
        return np.array([
            [1, 0, 0, 0, self.z, -self.y],
            [0, 1, 0, -self.z, 0, self.x],
            [0, 0, 1, self.y, -self.x, 0]
        ])
    
    def k_matrix(self):
        local_stiffness_matrix = self.local_stiffness_matrix()
        g_matrix = self.g_matrix()
        g_matrix_transpose = np.transpose(g_matrix)
        x = local_stiffness_matrix.dot(g_matrix)
        return g_matrix_transpose.dot(x)


class Engine:
    def __init__(self, mass, principal_moments=np.array([0, 0, 0]), theta=np.array([0,0,0])):
        self.mass = mass
        self.principal_moments = principal_moments
        self.theta = theta
    
    def mass_matrix(self):
        return np.array([
            [self.mass, 0, 0, 0, 0, 0],
            [0, self.mass, 0, 0, 0, 0],
            [0, 0, self.mass, 0, 0, 0],
            [0, 0, 0, self.principal_moments[0], 0, 0],
            [0, 0, 0, 0, self.principal_moments[1], 0],
            [0, 0, 0, 0, 0, self.principal_moments[1]],
        ])

class ForcePhasor:
    def __init__(self,  angular_frequency,  phasor_angle=np.zeros([6,1]),  f_x=0,  f_y=0,  f_z=0,  m_x=0,  m_y=0,  m_z=0):
        self.f_x = f_x
        self.f_y = f_y
        self.f_z = f_z
        self.m_x = m_x
        self.m_y = m_y
        self.m_z = m_z
        self.angular_frequency = angular_frequency
        self.phasor_angle = phasor_angle
    
    def force_phasor_matrix(self):
        return np.array([
            [self.f_x*math.exp(int(self.phasor_angle[0]))],
            [self.f_y*math.exp(int(self.phasor_angle[1]))],
            [self.f_z*math.exp(int(self.phasor_angle[2]))],
            [self.m_x*math.exp(int(self.phasor_angle[3]))],
            [self.m_y*math.exp(int(self.phasor_angle[4]))],
            [self.m_z*math.exp(int(self.phasor_angle[5]))]
        ])
    