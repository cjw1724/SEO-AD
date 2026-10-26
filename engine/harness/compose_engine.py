# -*- coding: utf-8 -*-
"""
ComposeEngine: Harness² Scaffolding Synthesizer & Rollback Shield.
Safely integrates verified scaffolding mutations into the persistent vault and runtime,
enforcing constitutional boundaries and providing 0.1s instant rollback protection.
"""
import sys
import copy
import logging
from typing import Dict, Any, Optional

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from engine.harness.probe_engine import ProbeResult

logger = logging.getLogger("ComposeEngine")


class ComposeResult:
    """Encapsulates the composition / integration result."""

    def __init__(
        self,
        success: bool,
        candidate_id: str,
        generation: int,
        applied_changes: Dict[str, Any],
        message: str = "",
    ):
        self.success = success
        self.candidate_id = candidate_id
        self.generation = generation
        self.applied_changes = applied_changes
        self.message = message

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "candidate_id": self.candidate_id,
            "generation": self.generation,
            "applied_changes": self.applied_changes,
            "message": self.message,
        }


class ComposeEngine:
    """Safely composes passed mutations into active scaffolding with rollback protection."""

    def __init__(self, vault):
        self.vault = vault
        self._checkpoint: Optional[Dict[str, Any]] = None

    def create_checkpoint(self) -> Dict[str, Any]:
        """Saves an in-memory snapshot of the vault for instant rollback."""
        self._checkpoint = copy.deepcopy(self.vault._data)
        return self._checkpoint

    def rollback(self) -> bool:
        """Restores the vault to the saved checkpoint within 0.1s."""
        if not self._checkpoint:
            logger.warning("No checkpoint available to rollback.")
            return False

        try:
            self.vault._data = copy.deepcopy(self._checkpoint)
            self.vault.save()
            logger.info("RollbackShield: Successfully restored vault from checkpoint.")
            return True
        except Exception as e:
            logger.error(f"RollbackShield: Rollback failed: {e}")
            return False

    def compose(
        self,
        proposal: Dict[str, Any],
        probe_result: ProbeResult,
    ) -> ComposeResult:
        """
        Safely integrates the probed mutation into the vault if it passed.
        If any step fails, triggers RollbackShield automatically.
        """
        candidate_id = proposal.get("proposal_id", "UNKNOWN")

        # 1. Gate: Must have passed probe evaluation
        if not probe_result.passed:
            # Record failed attempt as REJECTED for permanent negative learning
            self.vault.record_learning(
                domain=proposal.get("module_name", "general"),
                symptom=f"Proposal {candidate_id} failed probe evaluation",
                root_cause=f"Probe score {probe_result.fitness_score} < threshold ({'; '.join(probe_result.reasons)})",
                scaffold_patch=proposal.get("suggested_patch", ""),
                fitness_score=probe_result.fitness_score,
                status="REJECTED",
            )
            return ComposeResult(
                success=False,
                candidate_id=candidate_id,
                generation=self.vault._data.get("active_generation", 1),
                applied_changes={},
                message=f"Probe failed with score {probe_result.fitness_score}: {'; '.join(probe_result.reasons)}",
            )

        # 2. Create checkpoint before making changes
        self.create_checkpoint()

        applied: Dict[str, Any] = {}
        try:
            payload = proposal.get("mutation_payload", {})

            # A. Apply Prompt Rules
            agent_role = payload.get("agent_role")
            rule = payload.get("rule")
            if agent_role and rule:
                self.vault.register_prompt_rule(agent_role, rule)
                applied["prompt_rule"] = {"role": agent_role, "rule": rule}

            # B. Apply Runtime Policies
            policy_updates = payload.get("policy_updates", {})
            if policy_updates:
                for k, v in policy_updates.items():
                    self.vault.set_policy(k, v)
                applied["policy_updates"] = policy_updates

            # C. Record active learning in vault
            entry = self.vault.record_learning(
                domain=proposal.get("module_name", "general"),
                symptom=proposal.get("rationale", ""),
                root_cause=f"Resolved via {proposal.get('category')}",
                scaffold_patch=proposal.get("suggested_patch", ""),
                fitness_score=probe_result.fitness_score,
                status="ACTIVE",
            )
            applied["learning_entry"] = entry

            new_gen = self.vault._data.get("active_generation", 1)
            return ComposeResult(
                success=True,
                candidate_id=candidate_id,
                generation=new_gen,
                applied_changes=applied,
                message="Successfully composed candidate mutation into active scaffold.",
            )

        except Exception as e:
            logger.error(f"Error during composition: {e}. Triggering RollbackShield.")
            self.rollback()
            return ComposeResult(
                success=False,
                candidate_id=candidate_id,
                generation=self.vault._data.get("active_generation", 1),
                applied_changes={},
                message=f"Composition aborted and rolled back due to error: {e}",
            )
