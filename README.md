# Raft Technical Challenge — Agentic Order Intelligence (Python)

## Overview

Candidate Name: Nick Gupta

This project implements a **customer-facing, agentic AI system** that converts unstructured operational data into **trusted, structured insight**.

The system accepts a natural-language request, retrieves raw order data from a simulated customer API, normalizes inconsistent free-text into validated JSON, and returns **deterministic, auditable results** aligned with the user’s intent.

The focus of this solution is **operational usefulness**:
- Systems over models
- Deterministic behavior over novelty
- Clear failure modes
- Interfaces designed for real customers

This reflects how Raft approaches mission-critical AI under real-world constraints.

---

## Capabilities

- Natural-language query interface
- Agent-driven orchestration
- Constrained LLM-based normalization
- Deterministic filtering and validation
- Clean JSON output
- Optional Web API (Flask)
- Optional analytics extension (predictive averages by state)

---

## Architecture

See the architecture.png file.

```text
User (CLI / Web)
        ↓
Agent Controller
        ↓
Customer API (unstructured text)
        ↓
LLM Normalizer (schema-constrained)
        ↓
Schema Validation
        ↓
Deterministic Business Logic
        ↓
Structured JSON Output


```mermaid
flowchart LR
    A[User<br/>CLI or Web] --> B[Agent Controller]
    B --> C[Customer API<br/>Unstructured Text]
    C --> D[LLM Normalizer<br/>Schema-Constrained]
    D --> E[Schema Validation]
    E --> F[Deterministic Filtering]
    F --> G[Structured JSON Output]

