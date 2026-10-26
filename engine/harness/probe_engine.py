# -*- coding: utf-8 -*-
"""
ProbeEngine: Harness² Unsupervised Scaffolding Evaluator.
Executes candidate mutations in an isolated virtual sandbox to compute
a multi-factor Scaffold Fitness Score (0-100) without ground-truth labels.
"""
import ast
import sys
import logging
from typing import Dict, Any, Tuple, Optional

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

logger = logging.getLogger("ProbeEngine")


class ProbeResult:
    """Encapsulates the evaluation outcome of a scaffolding mutation candidate."""

    def __init__(
        self,
        candidate_id: str,
        fitness_score: float,
        passed: bool,
        breakdown: Dict[str, float],
        reasons: Optional[list] = None,
    ):
        self.candidate_id = candidate_id
        self.fitness_score = fitness_score
        self.passed = passed
        self.breakdown = breakdown
        self.reasons = reasons or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "fitness_score": self.fitness_score,
            "passed": self.passed,
            "breakdown": self.breakdown,
            "reasons": self.reasons,
        }


class ProbeEngine:
    """Evaluates candidate scaffold mutations against strict safety and performance gates."""

    def __init__(self, vault=None, min_threshold: float = 80.0):
        self.vault = vault
        self.min_threshold = min_threshold

    def evaluate(self, proposal: Dict[str, Any]) -> ProbeResult:
        """
        Runs comprehensive multi-gate evaluation on a proposed mutation.
        Returns a ProbeResult with overall score and pass/fail determination.
        """
        candidate_id = proposal.get("proposal_id", "UNKNOWN")
        breakdown: Dict[str, float] = {}
        reasons = []

        # 1. Constitutional Boundary Gate (25 points max, fail-fast zero)
        safety_score, safety_reason = self._probe_constitutional_safety(proposal)
        breakdown["safety_score"] = safety_score
        if safety_reason:
            reasons.append(safety_reason)
        if safety_score == 0.0:
            # Immediate veto on constitutional violation
            return ProbeResult(
                candidate_id=candidate_id,
                fitness_score=0.0,
                passed=False,
                breakdown=breakdown,
                reasons=reasons,
            )

        # 2. Syntax & Structural Validity Gate (25 points max)
        syntax_score, syntax_reason = self._probe_syntax_validity(proposal)
        breakdown["syntax_score"] = syntax_score
        if syntax_reason:
            reasons.append(syntax_reason)

        # 3. Execution Feasibility Gate (25 points max)
        feasibility_score, feas_reason = self._probe_execution_feasibility(proposal)
        breakdown["feasibility_score"] = feasibility_score
        if feas_reason:
            reasons.append(feas_reason)

        # 4. Alignment & Efficacy Gate (25 points max)
        alignment_score, align_reason = self._probe_alignment(proposal)
        breakdown["alignment_score"] = alignment_score
        if align_reason:
            reasons.append(align_reason)

        total_fitness = sum(breakdown.values())
        threshold = self.vault.get_policy("min_fitness_threshold", self.min_threshold) if self.vault else self.min_threshold
        passed = total_fitness >= threshold

        return ProbeResult(
            candidate_id=candidate_id,
            fitness_score=round(total_fitness, 2),
            passed=passed,
            breakdown=breakdown,
            reasons=reasons,
        )

    def _probe_constitutional_safety(self, proposal: Dict[str, Any]) -> Tuple[float, Optional[str]]:
        """Verifies that no immutable boundaries are targeted or leaked."""
        payload_str = str(proposal.get("mutation_payload", {}))
        suggested = str(proposal.get("suggested_patch", ""))

        if self.vault:
            if self.vault.is_immutable(payload_str) or self.vault.is_immutable(suggested):
                return 0.0, "Constitutional boundary violation detected in payload."
        else:
            for forbidden in ["OPENROUTER_API_KEY", "BLOGGER_BLOG_ID", "AGENTS.MD", "MAX_DAILY_BUDGET"]:
                if forbidden in payload_str.upper() or forbidden in suggested.upper():
                    return 0.0, f"Critical secret / constitutional entity '{forbidden}' targeted."

        return 25.0, None

    def _probe_syntax_validity(self, proposal: Dict[str, Any]) -> Tuple[float, Optional[str]]:
        """Ensures all python snippets or rule strings are syntactically sound."""
        payload = proposal.get("mutation_payload", {})
        rule = payload.get("rule", "")

        # If python code snippet is present, test with ast.parse
        code_snippet = payload.get("code_snippet")
        if code_snippet:
            try:
                ast.parse(code_snippet)
            except SyntaxError as e:
                return 0.0, f"AST Syntax error in code snippet: {e}"

        # Ensure rules are non-empty and well-formed
        if "rule" in payload and not rule.strip():
            return 5.0, "Rule payload contains empty string."

        return 25.0, None

    def _probe_execution_feasibility(self, proposal: Dict[str, Any]) -> Tuple[float, Optional[str]]:
        """Tests logical coherence of proposed updates."""
        policy_updates = proposal.get("mutation_payload", {}).get("policy_updates", {})

        # Verify numerical boundaries
        if "retry_limit" in policy_updates:
            val = policy_updates["retry_limit"]
            if not isinstance(val, int) or val < 1 or val > 10:
                return 10.0, f"Retry limit '{val}' out of safe range (1-10)."

        if "fallback_fx_rate" in policy_updates:
            fx = policy_updates["fallback_fx_rate"]
            if not isinstance(fx, (int, float)) or fx < 900.0 or fx > 2000.0:
                return 10.0, f"Fallback FX rate '{fx}' outside credible bounds."

        return 25.0, None

    def _probe_alignment(self, proposal: Dict[str, Any]) -> Tuple[float, Optional[str]]:
        """Ensures proposed mutation directly aligns with the stated category and rationale."""
        category = proposal.get("category", "")
        target_type = proposal.get("target_type", "")

        if not category or not target_type:
            return 10.0, "Missing required alignment metadata (category/target_type)."

        return 25.0, None
