# SpallationSim: Geant4 Nuclear Spallation Simulation

This project simulates nuclear spallation of a target using a 1 GeV proton beam. The simulation is implemented in Geant4 and was developed as part of the BL4S CERN project for pre-experimental validation.

---

## Simulation Overview

- **Target:** Tungsten (W), cylindrical shape, 15 cm diameter, 60 cm height
- **Beam:**
  - 1000 protons
  - 50 pi+ mesons (5% contamination)
  - Energy: 1 GeV
- **Output:** Neutron data including energy, theta, and phi saved in CSV format (`neutron_output.csv`)

---

## File Directory

```bash
SpallationSim/
├── CMakeLists.txt
├── main.cc
├── include/
│   ├── DetectorConstruction.hh
│   ├── PrimaryGeneratorAction.hh
│   ├── RunAction.hh
│   └── SteppingAction.hh
├── src/
│   ├── DetectorConstruction.cc
│   ├── PrimaryGeneratorAction.cc
│   ├── RunAction.cc
│   └── SteppingAction.cc
└── neutron_output.csv  # output file
```

---

## Build Instructions

```bash
mkdir build && cd build
cmake ..
make -j
./SpallationSim
```

---

## Data Analysis (Python)

The following three analysis functions are provided in `neutron_analysis.py`:

1. `plot_energy_distribution(path)` – Histogram of neutron energy
2. `plot_energy_vs_angle_3d(path)` – 3D scatter plot based on energy and angular distribution
3. `plot_angle_distribution(path)` – Histogram of neutron count versus theta angle

### Example Usage
```python
from neutron_analysis import *
plot_energy_distribution("neutron_output.csv")
plot_energy_vs_angle_3d("neutron_output.csv")
plot_angle_distribution("neutron_output.csv")
```

---

## Objective

This experiment is planned to be performed during the CERN Beamline for Schools (BL4S) 2024 program by PhysiCAL team, aiming to observe neutron production and its energy-angular distribution via spallation.

---

## Authors

> This project was developed for the CERN Beamline for Schools (BL4S) competition. All rights reserved.

Contact: [musluoglu.mert10@gmail.com]
