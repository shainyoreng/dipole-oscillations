# Magnetic dipole coupled oscillators - M.D.C.O

In this project we analyze coupled Oscillating magnets modeled as dipoles on rods, as in the following sketch:
![image](https://github.com/user-attachments/assets/6dcb8422-0392-4f3f-84da-6161271e18e2)

In this system there are 3 magnets of equal strengths $\left|\vec{m}_ {1}\right|=\left|\vec{m}_ {3}\right|=\left|\vec{m}_{3}\right|$, one stationary in the middle and two that can freely rotate around a rod of length $R$.
We will use a few assumptions.
1. The magnets can be modeled as a magnetic dipole moment.
2. Air resistance is completely neglected, and so are the rods' masses.

![image](https://github.com/user-attachments/assets/8ac60b9f-0b27-49f6-a548-e1a47117773f)


Before we jumped into this intimidating problem, we solved a similar one as can be be seen in this sketch:
![image](https://github.com/user-attachments/assets/50bfd9e4-e28c-4b21-97a2-61ebd4f0e969)
as you can see this system avoids the effect of gravity by making the magnets rotate around their center and thus we can trivially conclude that $0^\circ$ is the angle of stability. This system also makes the magnetic field calculations a lot simpler.
You can see this system simulated in time in this [link](https://alon-h.github.io/dipole-oscillations/) or you could <kbd>Ctrl+C</kbd> $\to$ <kbd>Ctrl+V</kbd> the sketch.js file into the [online p5js editor](https://editor.p5js.org) and then be able to edit the values.

## Theoretical Results

We will use Lagrangian mechanics to solve this problem theoretically. We will first write the Lagrangian for the simplest system. The total magnetic energy stored in the system is given by:

$$
U = U_{12} + U_{13} + U_{23}
$$

where 

$$
U_{ij} = -\vec{m_{i}} \cdot \vec{B_{j}}, \quad \vec{B} = \frac{\mu_{0}}{4\pi}\left(3\hat{r}\left(\vec{m}\cdot\hat{r}\right) - \vec{m}\right)
$$

are given by

$$
U_{12} = \frac{\mu_{0} m^{2} \cos \theta_{1}}{4\pi d^{3}}
$$

$$
U_{13} = \frac{\mu_{0} m^{2} \cos \theta_{2}}{4\pi d^{3}}
$$

$$
U_{23} = \frac{\mu_{0} m^{2}}{32\pi d^{3}}\left(2\sin \theta_{1} \sin \theta_{2} + \cos \theta_{1} \cos \theta_{2}\right)
$$

Thus the corresponding Lagrangian is

$$
L = \frac{1}{2} I \left(\dot{\theta}_{1}^{2} + \dot{\theta}_{2}^{2}\right) - \frac{\mu_{0} m^{2}}{32\pi d^{3}}\left[8\left(\cos \theta_{1} + \cos \theta_{2}\right) 2\sin
\theta_{1} \sin \theta_{2} + \cos \theta_{1} \cos \theta_{2}\right]
$$

Now to get the two normal modes for small oscillations around 0 (the stable point), we use the small angle approximation to get

$$
L = \frac{1}{2} I \left(\dot{\theta}_{1}^{2} + \dot{\theta}_{2}^{2}\right) - \frac{\mu_{0} m^{2}}{8 d^{3}}\left[\frac{9}{2}\left(\theta_{1}^{2} + \theta_{2}^{2}\right)-
2\theta_{1} \theta_{2}\right]
$$


From here we deduce the two normal modes are:

$$
\omega_{1}=\sqrt{\frac{7\mu_0 m^{2}}{32Id^{3}}},\vec{v_{1}}=\begin{pmatrix}1\\
-1
\end{pmatrix}
$$

$$
\omega_{2}=\sqrt{\frac{11\mu_0 m^{2}}{32Id^{3}}},\vec{v_{2}}=\begin{pmatrix}1\\
1
\end{pmatrix}
$$

We could have easily included the gravitational potential of the magnets, but then approximating around a non-zero stable point requires much more work. We also haven't gotten around to writing the Lagrangian for the case where the dipole is on a rod. If you think you found an appropriate Lagrangian, feel free to make contact.
### notes
We could have easily included the gravitational potential of the magnets, but then approximating around a non zero stable point requires much more work. 
We also haven't gotten around to writing the Lagrangian for the case where the dipole is on a rod. if you think you found an appropriate Lagrangian feel free to make contact.
![image](https://github.com/user-attachments/assets/b131ce4b-78da-4cc2-9139-91fde99f54fa)
