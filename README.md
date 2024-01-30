# Hunt Crossley / Hertz Parameter Identification

In some Open Sim muscoloskeletal models used for predictive gait simulations, the contact between foot and ground is modeled via [Hunt Crossley spheres](https://simtk.org/api_docs/molmodel/api_docs22/Simbody/html/classSimTK_1_1HuntCrossleyForce.html). 

According to Simbody, the normal force exchanged by the floor and a Hunt Crossley Sphere object is composed of an elastic and a dissipative component.

$f_k =  4/3 * \sigma   \sqrt{R}  * E * x^{3/2}$

computes the elastic ccontribution. In particular $\sigma=1$, $R$ is the radius of the sphere, $E$  is the composite young modulus ($N/m^2$) of the two colliding objects, $x$ is the deformation of the sphere which causes the reaction force.

$f_{diss} = (3/2) * f_k *c * \dot{x}$

represents the dissipative contribution. Note that it depends both on the dissipation coefficient $c$ and on the elastic contribution $f_k$ itself.

The parameters which can be changed in OpenSim are $E$, referred to as stiffness, and $c$.

# Objective of this repo

The goal is to estimate $E$ and $c$ by means of experimental data

# Experiments

We distinguish between *in vivo* and *in vitro*. 

The first refers to a collision experiment between a mass and a live heelpad [3,4]. Here the effect of the lower leg is also captured. We are more interested in these type of experiments. The deceleration of the mass during impact with the heelpad is measured with an accelerometer and force/deformation plots are produced.

In vitro refers to experiments usually done with an indenter on severed samples of heel pad, sometimes with residual calcaneus bone present [2].

# References

[1] M. A. Sherman, A. Seth, and S. L. Delp, “Simbody: multibody dynamics for biomedical research,” Procedia IUTAM,  2011.

[2] P. Aerts, R. F. Ker, D. De Clercq, D. W. Ilsley, and R. McN. Alexander, “The mechanical properties of the human heel pad: A paradox resolved,” Journal of Biomechanics,1995.

[3] P. Aerts and D. D. Clercq, “Deformation characteristics of the heel region of the shod foot during a simulated heel strike: The effect of varying midsole hardness,” Journal of Sports Sciences, 1993.

[4] H. Kinoshita, T. Ogawa, K. Kuzuhara, and K. Ikuta, “In Vivo Examination of the Dynamic Properties of the Human Heel Pad,” Int J Sports Med, 1993.



# Data

artz asc_vitro : Aertz 1995, Fig 1B

barefoot: Aertz 1993, Fig.4

deceleration/displacement: Kinoshita 1993, Fig.3
