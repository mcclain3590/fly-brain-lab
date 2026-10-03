# Fly Brain Lab — Research & Engineering Roadmap

## Guiding Principle

Progress from the smallest understandable biological circuit toward increasingly complex computational experiments.

Do not scale until the current level is understood, tested and reproducible.

---

# M0 — Project Foundation

Status: COMPLETE

Goal:

Create a reproducible engineering and research foundation.

Deliverables:

- GitHub repository
- project charter
- tool roles
- roadmap
- architecture
- engineering standards
- dataset/source documentation
- decision log
- experiment log
- Python environment
- dependency management
- `.gitignore`
- initial README

Exit criteria:

The project can be cloned onto another machine and its purpose,
architecture, rules and next milestone can be understood from the repository.

---

# M1 — Connectome Access

Status: IN PROGRESS

Goal:

Retrieve a small amount of authoritative biological connectome data.

Target:

Approximately 10–20 neurons initially.

Tasks:

- identify authoritative MaleCNS access method
- document dataset version
- establish API/client access
- retrieve real neuron records
- retrieve connectivity
- inspect returned fields
- save a small local subset
- document provenance

Questions to answer:

- What uniquely identifies a neuron?
- What represents a synapse?
- What represents neuron-to-neuron connectivity?
- What biological information is measured?
- What information is inferred?
- What information is missing?

Exit criteria:

We can retrieve real connectome data and explain the important fields.

---

# M2 — Connectivity Visualisation

Goal:

Turn connectivity data into an understandable graph.

Concept:

Neuron = node

Connection = directed edge

Measured connectivity information = edge metadata

Tasks:

- construct graph representation
- visualise selected neurons
- inspect incoming connections
- inspect outgoing connections
- investigate connection strength/count information

Exit criteria:

We can visually trace connectivity through a small real circuit.

---

# M3 — Biological Circuit Selection

Goal:

Stop working with arbitrary neurons and select a biologically meaningful circuit.

Potential directions:

- olfactory pathway
- visual pathway
- sensory-to-motor pathway
- learning-related circuit

Selection must be based on biological evidence.

Tasks:

- research candidate circuit
- identify relevant neuron classes
- trace connectivity
- document scientific sources
- extract manageable subgraph

Exit criteria:

We have one documented biological circuit suitable for computational modelling.

---

# M4 — Computational Neuron Model

Goal:

Introduce neural dynamics.

Important distinction:

Connectome structure does not define complete neuron dynamics.

Any computational dynamics introduced here are modelling assumptions.

Tasks:

- study candidate neuron models
- choose simplest appropriate model
- document assumptions
- implement model
- test individual neuron behaviour

Possible starting models may include:

- threshold units
- leaky integrator
- leaky integrate-and-fire

Model selection will be decided later based on the experiment.

Exit criteria:

We understand and can demonstrate the behaviour of our computational neuron model.

---

# M5 — Signal Propagation

Goal:

Run activity through a connectome-derived circuit.

Pipeline:

Input
→ computational neurons
→ connectome-derived connectivity
→ activity propagation
→ output

Tasks:

- map biological connectivity into simulation
- define timing/update rules
- inject controlled input
- record activity
- visualise propagation

Exit criteria:

A controlled stimulus produces measurable activity through the selected circuit.

---

# M6 — Sensory / Motor Interface

Goal:

Connect the neural circuit to external inputs and outputs.

Potential architecture:

Artificial sensor
→ sensory interface
→ connectome-derived circuit
→ motor interface
→ action

Tasks:

- define sensory encoding
- define motor decoding
- document artificial mappings
- test deterministic stimuli

Exit criteria:

External input can produce an observable action through the neural system.

---

# M7 — Virtual Environment

Goal:

Close the perception-action loop.

Architecture:

Environment
→ sensory input
→ neural circuit
→ motor output
→ environment changes
→ new sensory input

Start extremely simple.

Possible first environment:

A 2D agent choosing between left and right.

Exit criteria:

The neural system interacts continuously with an environment.

---

# M8 — Plasticity

Goal:

Allow selected computational synapses to change with experience.

Important:

Plasticity rules introduced by us are computational assumptions unless directly supported by biological evidence.

Tasks:

- study biological learning mechanisms
- choose plasticity rule
- implement controlled weight modification
- record before/after state
- test persistence

Exit criteria:

Experience produces measurable persistent network change.

---

# M9 — Associative Learning & Memory

Goal:

Test whether previous experience changes future behaviour.

Example experiment:

Stimulus A + reward
Stimulus B + negative outcome

Then:

Stimulus A alone
Stimulus B alone

Measure whether behaviour differs because of previous training.

Tasks:

- define training protocol
- establish control condition
- record network state
- train
- test
- compare behaviour
- repeat experiment

Exit criteria:

A reproducible experiment demonstrates experience-dependent behavioural change.

This may be described as computational associative memory only when supported by the experiment.

---

# M10 — Scaling Experiments

Goal:

Investigate larger connectome-derived systems.

Only begin after earlier milestones are stable.

Potential experiments:

- larger sensory circuits
- multiple sensory modalities
- larger recurrent networks
- richer environments
- navigation
- control tasks
- comparison against artificial neural architectures

Scaling is an experiment, not automatically an improvement.

---

# Long-Term Research Question

Eventually investigate:

How much useful adaptive behaviour can emerge when biological connectome topology is combined with explicit computational neuron dynamics, artificial sensory interfaces and learning mechanisms?

---

# Not a Current Goal

The project is NOT currently attempting:

- whole-brain biological fidelity
- consciousness simulation
- resurrection
- recovery of the original fly's memories
- proof of subjective experience
- immediate replication of self-driving connectome projects

These subjects may be discussed scientifically but are not engineering milestones.

---

# Current Position

M1 — Connectome Access (IN PROGRESS)

First selected circuit: `ORN_DA1 -> DA1_lPN` (see `docs/DATA_SOURCES.md`).
Dataset/endpoint access verified live; authoritative checksummed retrieval
via `scripts/retrieve_da1.py` not yet executed.

Next:

Complete M1 retrieval, inspection and provenance documentation before
moving to M2 — Connectivity Visualisation.
