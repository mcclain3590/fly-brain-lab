# Fly Brain Lab — Project Charter

## 1. Project

**Name:** Fly Brain Lab

**Repository:** `mcclain3590/fly-brain-lab`

**Status:** Experimental / Research / Learning

**Primary Language:** Python

---

## 2. Mission

Fly Brain Lab is an experimental software-engineering and computational-neuroscience project for exploring biological neural circuits derived from the Drosophila connectome.

The project will begin with small, understandable subsets of real connectome data and progressively investigate:

1. biological connectivity,
2. neural circuit structure,
3. computational neuron dynamics,
4. signal propagation,
5. sensory-to-motor pathways,
6. artificial environments,
7. synaptic plasticity,
8. learning and memory,
9. emergent behaviour,
10. larger connectome-derived simulations.

The project prioritises understanding, reproducibility and scientific honesty over impressive demonstrations.

---

## 3. Core Research Question

Can computational neural systems constructed from measured Drosophila connectome topology exhibit meaningful signal propagation, adaptation, learning and behaviour when coupled to artificial sensory inputs and environments?

This question will be investigated experimentally.

No outcome is assumed in advance.

---

## 4. Starting Dataset

The initial biological source is the publicly available adult male Drosophila central nervous system connectome.

The project will initially access small subsets of the connectome rather than downloading or attempting to simulate the entire dataset.

Dataset provenance, versions, access methods and citations must be documented in:

`docs/DATA_SOURCES.md`

---

## 5. Engineering Philosophy

### Understand before scaling

We will not begin with a whole-brain simulation.

Progression should generally follow:

Small dataset
→ inspect
→ understand
→ visualise
→ model
→ test
→ validate
→ scale

### Biological data and computational models are different

The connectome is biological measurement/reconstruction data.

A computational neuron created from that data is a model.

These must never be described as the same thing.

### Experiments before claims

Interesting behaviour is not automatically evidence of biological equivalence.

Claims must follow experimental evidence.

### Reproducibility

An experiment should eventually be reproducible from:

- source code,
- configuration,
- dataset version,
- random seed where applicable,
- dependencies,
- experiment documentation,
- results.

---

## 6. Scientific Boundaries

Fly Brain Lab does NOT initially claim to:

- recreate a living fruit fly,
- resurrect an individual fly,
- recover memories from the original animal,
- reproduce consciousness,
- prove subjective experience,
- reproduce biological neural dynamics exactly,
- prove that simulated behaviour is equivalent to biological behaviour.

The connectome provides structural information.

Additional assumptions and computational models will be required to simulate neural activity.

Those assumptions must be documented.

---

## 7. Initial Success Criterion

The first milestone is intentionally small.

Fly Brain Lab must be able to:

1. access an authoritative connectome source,
2. retrieve a small set of real neurons,
3. retrieve connectivity between those neurons,
4. store the selected data locally,
5. inspect the data using Python,
6. visualise the resulting connectivity,
7. explain what every major field represents.

No neural simulation is required for this milestone.

---

## 8. Long-Term Experimental Direction

If earlier milestones succeed, later experiments may investigate:

Sensory input
→ connectome-derived neural circuit
→ neural dynamics
→ motor output
→ artificial environment
→ feedback

Later stages may introduce plasticity:

Experience
→ synaptic modification
→ persistent network change
→ behavioural testing

The purpose is to investigate computational behaviour produced by connectome-derived architectures.

---

## 9. Source of Truth

GitHub is the project's single source of truth.

Authoritative information includes:

- source code,
- architecture,
- engineering decisions,
- experiment definitions,
- dataset provenance,
- dependency configuration,
- test results,
- milestone status.

If important information exists only in an AI conversation or personal notebook, it is not considered an authoritative project decision.

---

## 10. Obsidian

Obsidian is the research and learning notebook.

It may contain:

- neuroscience notes,
- explanations,
- questions,
- hypotheses,
- paper notes,
- personal understanding,
- experiment ideas.

Obsidian is NOT the authoritative engineering source.

Any decision affecting implementation, architecture, datasets or experiments must be promoted into the GitHub repository.

---

## 11. AI Engineering Agents

Multiple AI systems may assist the project.

Their responsibilities will be defined in:

`docs/TOOL_ROLES.md`

No AI agent independently defines project scope or scientific conclusions.

Significant architectural changes must be documented.

---

## 12. Development Principle

Do not add complexity merely because it is technically possible.

At every stage ask:

**What is the smallest experiment that can answer the current question?**

Build that first.

---

## 13. Current Milestone

**M0 — Project Foundation**

Objectives:

- establish repository,
- establish documentation,
- define source-of-truth rules,
- define AI tool responsibilities,
- establish Python environment,
- document biological data sources,
- establish engineering standards.

After M0 is complete:

**M1 — Connectome Access**

The first biological data will enter the project
