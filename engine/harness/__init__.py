"""
Harness² (Harness Squared) Self-Scaffolding Evolution Package.
Google Cloud AI Research recursive agent optimization engine.
"""
from engine.harness.harness_vault import HarnessVault, default_vault
from engine.harness.propose_engine import ProposeEngine, FailureCategory
from engine.harness.probe_engine import ProbeEngine, ProbeResult
from engine.harness.compose_engine import ComposeEngine, ComposeResult
from engine.harness.harness_facade import HarnessFacade, harness_facade

__all__ = [
    "HarnessVault",
    "default_vault",
    "ProposeEngine",
    "FailureCategory",
    "ProbeEngine",
    "ProbeResult",
    "ComposeEngine",
    "ComposeResult",
    "HarnessFacade",
    "harness_facade",
]
