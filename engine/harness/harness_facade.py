# -*- coding: utf-8 -*-
"""
HarnessFacade: Unified Orchestration Interface for Harness².
Provides a single entry point for pipeline agents and runtime runners to:
1. Dynamically enrich agent prompts with self-evolved operational directives.
2. Intercept runtime exceptions and execute the Propose-Probe-Compose cycle.
3. Access dynamic policies with automatic fallbacks and rollback protection.
"""
import sys
import logging
import traceback
from typing import Dict, Any, Optional

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from engine.harness.harness_vault import HarnessVault, default_vault
from engine.harness.propose_engine import ProposeEngine
from engine.harness.probe_engine import ProbeEngine
from engine.harness.compose_engine import ComposeEngine, ComposeResult

logger = logging.getLogger("HarnessFacade")


class HarnessFacade:
    """Unified coordinator for the Harness² recursive self-improvement cycle."""

    def __init__(self, vault: Optional[HarnessVault] = None):
        self.vault = vault or default_vault
        self.propose_engine = ProposeEngine(self.vault)
        self.probe_engine = ProbeEngine(self.vault)
        self.compose_engine = ComposeEngine(self.vault)

    def enrich_prompt(self, agent_role: str, base_prompt: str) -> str:
        """Enriches an agent prompt with verified self-evolved rules from the vault."""
        return self.vault.inject_prompt_rules(agent_role, base_prompt)

    def get_policy(self, policy_name: str, default: Any = None) -> Any:
        """Retrieves a dynamic execution policy."""
        return self.vault.get_policy(policy_name, default)

    def handle_runtime_failure(
        self,
        module_name: str,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
    ) -> ComposeResult:
        """
        Executes the full Propose-Probe-Compose cycle on an unhandled exception.
        If self-improvement succeeds, updates the vault and active generation.
        """
        error_msg = str(error)
        stack = traceback.format_exc()
        logger.info(f"🧬 Harness² Intercept: Module '{module_name}' failed with: {error_msg}")

        # 1. Propose
        proposal = self.propose_engine.propose_mutation(
            module_name=module_name,
            error_message=error_msg,
            stack_trace=stack,
            context=context,
        )
        logger.info(f"🧬 Harness² Propose: Generated {proposal['proposal_id']} for {proposal['category']}")

        # 2. Probe
        probe_result = self.probe_engine.evaluate(proposal)
        logger.info(
            f"🧬 Harness² Probe: Candidate {proposal['proposal_id']} scored "
            f"{probe_result.fitness_score}/100 (Passed: {probe_result.passed})"
        )

        # 3. Compose
        compose_result = self.compose_engine.compose(proposal, probe_result)
        if compose_result.success:
            logger.info(
                f"🧬 Harness² Compose: Mutation successfully integrated! "
                f"Active Generation: {compose_result.generation}"
            )
        else:
            logger.warning(
                f"🧬 Harness² Compose: Mutation rejected ({compose_result.message}). System safe."
            )

        return compose_result


# Global singleton instance
harness_facade = HarnessFacade()
