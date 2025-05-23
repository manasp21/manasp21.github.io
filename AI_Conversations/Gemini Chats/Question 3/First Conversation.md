### User Prompt 1

Mirrorless lasing (MR) is a process of generation of a directed nearly monochromatic radiation,
without any mirrors, by a medium (in our case, an ensemble of atoms) exposed to a pump laser
beam. ML is usually associated with “pencil-like” pumping; it often occurs in both forward and
backward direction with respect to the pump beam. Degenerate mirrorless lasing (DML) refers to a
situation where the emitted radiation is at a frequency that is the same (or close to) the frequency
of the pump light.
Consider a J = 1 → J′ = 2 transition. There is no relaxation in the system except for the
spontaneous decay from the upper state to the lower state. The atoms are stationary. The pumped
volume is a cylindrical of length LL and radius RR; the atomic number density is n. The atoms
are illuminated with resonant cw light with linear z polarization.
What are the conditions for mirrorless lasing in the forward and backward directions for light
with x polarization? The axis of the cylinder is the y axis.

---
### Gemini Answer 1

Mirrorless lasing (ML) by an ensemble of atoms exposed to a pump laser beam results in directed, nearly monochromatic radiation without an external optical cavity. Degenerate mirrorless lasing (DML) occurs when the emitted radiation frequency is very close to the pump frequency. We consider a $J=1 \rightarrow J'=2$ atomic transition in stationary atoms, with spontaneous decay from the upper to the lower state as the only relaxation mechanism. The atoms are in a cylindrical volume of length $L_L$ and radius $R_R$ (with $L_L \gg R_R$, implying pencil-like pumping), with the cylinder axis along the y-axis. The atoms are pumped by resonant continuous-wave (cw) light that is linearly polarized along the z-axis and propagates along the y-axis. We need to determine the conditions for mirrorless lasing in the forward (+y) and backward (-y) directions for light polarized along the x-axis.

The conditions can be broken down into general requirements for mirrorless lasing, specific requirements for achieving x-polarized emission with a z-polarized pump, and conditions pertinent to obtaining emission in both forward and backward directions.

**A. General Requirements for Mirrorless Lasing:**

1.  **Sufficient Atomic Number Density ($n$):** A high enough density of active atoms is necessary to provide sufficient gain for the lasing process.
2.  **Elongated Gain Medium Geometry:** The "pencil-like" pumped volume ($L_L \gg R_R$) along the y-axis is crucial. This geometry ensures that amplified spontaneous emission (ASE) predominantly occurs along the long axis (y-axis), leading to directional forward and backward beams.
3.  **Resonant CW Pump Laser:** The pump laser must be tuned to be resonant with the $J=1 \rightarrow J'=2$ transition to efficiently excite the atoms.
4.  **Pump Intensity Above Threshold:** The intensity of the z-polarized pump light must exceed a certain threshold. This threshold is determined by the need to create and maintain a sufficient population inversion (or the conditions for lasing without inversion) for the x-polarized light, overcoming the spontaneous decay rate from the $J'=2$ state to the $J=1$ state.
5.  **High Gain-Length Product:** For lasing to occur, the product of the gain coefficient for x-polarized light ($g_x$) and the length of the gain medium ($L_L$) must be large enough ($g_x L_L > \text{threshold}$) to amplify spontaneous emission to a significant, coherent output. This means $g_x$ must be positive (net gain).

**B. Specific Requirements for X-Polarized Degenerate Mirrorless Lasing (with Z-Polarized Pump):**

The core challenge is to explain how a z-polarized pump leads to gain for an orthogonally (x) polarized emission. The quantization axis is naturally chosen along the polarization of the pump field, i.e., the z-axis.

6.  **Creation of Anisotropic Gain for X-Polarization via Magnetic Sublevel Manipulation:**
    * **Pump Interaction ($\Delta M_z = 0$):** The z-polarized pump laser (Electric field $\vec{E}_{pump} \parallel \hat{z}$) drives transitions where the magnetic quantum number $M_z$ does not change:
        * $|J=1, M_z=0\rangle \leftrightarrow |J'=2, M'_z=0\rangle$
        * $|J=1, M_z=1\rangle \leftrightarrow |J'=2, M'_z=1\rangle$
        * $|J=1, M_z=-1\rangle \leftrightarrow |J'=2, M'_z=-1\rangle$
    * **X-Polarized Emission ($\Delta M_z = \pm 1$):** X-polarized light propagating along the y-axis (Electric field $\vec{E}_{emitted} \parallel \hat{x}$) is generated by transitions where $\Delta M_z = \pm 1$:
        The relevant emissive transitions from the directly pumped excited sublevels are:
        * $|J'=2, M'_z=0\rangle \rightarrow |J=1, M_z=+1\rangle$
        * $|J'=2, M'_z=0\rangle \rightarrow |J=1, M_z=-1\rangle$
        * $|J'=2, M'_z=+1\rangle \rightarrow |J=1, M_z=0\rangle$
        * $|J'=2, M'_z=-1\rangle \rightarrow |J=1, M_z=0\rangle$
        (Transitions from $M'_z=\pm 2$ could also contribute if these states are populated, e.g., through collisional relaxation or if the pump isn't purely z-polarized, but are not directly pumped by a $\Delta M_z=0$ process from $J=1$).
    * **Mechanism for Orthogonal Gain:**
        * **Population Inversion between Specific Magnetic Sublevels:** The z-polarized pumping, in conjunction with spontaneous decay processes (which can occur with $\Delta M_z = 0, \pm 1$), must lead to a population inversion on one or more of the $\Delta M_z = \pm 1$ transitions listed above. For example, the population of $|J'=2, M'_z=1\rangle$ must be greater than that of $|J=1, M_z=0\rangle$ ($N(J'=2, M'_z=1) > N(J=1, M_z=0)$) for gain on that specific x-polarized transition. This occurs due to optical pumping creating an anisotropic distribution of populations among the sublevels. The rates of pumping and the branching ratios of spontaneous decay (governed by Clebsch-Gordan coefficients) determine the steady-state populations.
        * **Lasing Without Inversion (LWI):** Alternatively, or in conjunction, strong resonant pumping can induce atomic coherences between the magnetic sublevels (Zeeman coherences). These coherences can lead to gain for the x-polarized light through quantum interference effects or mechanisms like hidden inversion in the dressed-state basis, even if a simple population inversion between the bare atomic sublevels is not achieved.

7.  **Degenerate Emission:** The gain mechanism (either population inversion or LWI) must provide amplification at a frequency very close to the pump laser frequency, as specified for DML.

8.  **Absence of Strong External Magnetic Fields (or Controlled Field):** While not explicitly stated to be absent, the phenomenon of DML with orthogonal polarization is often sensitive to magnetic fields. The problem assumes a simple system; uncontrolled external fields could disrupt the necessary sublevel population distributions or coherences. The linearly polarized pump itself breaks the symmetry and defines an effective quantization axis.

**C. Conditions for Emission in both Forward (+y) and Backward (-y) Directions:**

9.  **Bidirectional Gain Medium:** The conditions outlined in (A) and (B) that establish gain for x-polarized light must be present throughout the elongated pumped volume. Since the atoms are stationary and the pumping is CW, the local properties of the gain medium should, in principle, be the same for waves propagating in both +y and -y directions. Amplified Spontaneous Emission (ASE) will naturally build up along both directions of the pencil-shaped gain region.
10. **Sufficient Interaction Length ($L_L$):** The length of the gain medium must be sufficient for the ASE to be amplified to lasing intensities in both directions.
11. **Absence of Unidirectional Loss or Feedback Mechanisms:** The system should not contain any elements or intrinsic processes that preferentially favor one direction of propagation over the other for the x-polarized light.

In summary, mirrorless lasing in the forward and backward directions for x-polarized light, when pumped by z-polarized light resonant with a $J=1 \rightarrow J'=2$ transition, requires a sufficient density of atoms in an elongated geometry, pumped above a threshold intensity. Crucially, the z-polarized pump must induce an anisotropy in the atomic state populations or coherences, leading to net gain for the orthogonally polarized x-emission via population inversion between specific magnetic sublevels or LWI mechanisms. This gain must be present for frequencies degenerate with the pump and support amplification in both propagation directions along the pump axis.
