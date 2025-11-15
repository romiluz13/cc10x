#!/usr/bin/env node
/**
 * Integration Completeness Measurement Tool
 * Measures Parameter 5: Integration Completeness
 */

const fs = require("fs");
const path = require("path");
const {
  getAllSkills,
  analyzeWorkflows,
} = require("./analyze-skill-references");

function measureIntegrationCompleteness(metricsFile) {
  const metrics = JSON.parse(fs.readFileSync(metricsFile, "utf-8"));

  // Subagent whitelist (these are not skills, they're subagents)
  const subagentWhitelist = new Set([
    "code-reviewer",
    "integration-verifier",
    "component-builder",
    "bug-investigator",
    "planner",
  ]);

  // Tool whitelist (common CLI tools referenced in workflows)
  const toolWhitelist = new Set([
    "jq",
    "grep",
    "curl",
    "wget",
    "sed",
    "awk",
    "find",
    "xargs",
  ]);

  // Get current skills and workflows
  const skills = getAllSkills();
  const workflows = analyzeWorkflows();

  const skillNames = new Set(skills.map((s) => s.name));
  const workflowSkillRefs = new Set();
  const brokenRefs = [];

  // Check all workflow references
  for (const [workflowName, workflow] of Object.entries(workflows)) {
    for (const skillRef of workflow.skills) {
      // Skip subagents and tools (they're not skills)
      if (subagentWhitelist.has(skillRef) || toolWhitelist.has(skillRef)) {
        continue;
      }

      workflowSkillRefs.add(skillRef);
      if (!skillNames.has(skillRef)) {
        brokenRefs.push({
          workflow: workflowName,
          skill: skillRef,
          type: "missing_skill",
        });
      }
    }
  }

  // Calculate coverage
  const totalRefs = workflowSkillRefs.size;
  const validRefs = totalRefs - brokenRefs.length;
  const coveragePercent =
    totalRefs > 0 ? Math.round((validRefs / totalRefs) * 100 * 100) / 100 : 100;

  // Check orchestrator references (if orchestrator skill exists)
  let orchestratorRefs = 0;
  let orchestratorBrokenRefs = 0;

  const orchestratorPath = path.join(
    process.cwd(),
    "plugins/cc10x/skills/cc10x-orchestrator/SKILL.md",
  );
  if (fs.existsSync(orchestratorPath)) {
    const orchestratorContent = fs.readFileSync(orchestratorPath, "utf-8");
    const skillPattern = /`([a-z0-9-]+)`/g;
    let match;
    const orchestratorSkillRefs = new Set();

    while ((match = skillPattern.exec(orchestratorContent)) !== null) {
      const skillName = match[1];
      // Skip common false positives, subagents, and tools
      if (
        !["skill", "skills", "workflow", "workflows"].includes(skillName) &&
        !subagentWhitelist.has(skillName) &&
        !toolWhitelist.has(skillName)
      ) {
        orchestratorSkillRefs.add(skillName);
        orchestratorRefs++;
        if (!skillNames.has(skillName)) {
          orchestratorBrokenRefs++;
        }
      }
    }
  }

  const orchestratorCoverage =
    orchestratorRefs > 0
      ? Math.round(
          ((orchestratorRefs - orchestratorBrokenRefs) / orchestratorRefs) *
            100 *
            100,
        ) / 100
      : 100;

  // Overall integration score
  const overallScore = coveragePercent * 0.7 + orchestratorCoverage * 0.3;

  return {
    parameter: "Integration Completeness",
    metrics: {
      workflow_references: {
        total: totalRefs,
        valid: validRefs,
        broken: brokenRefs.length,
        coverage_percent: coveragePercent,
        broken_refs: brokenRefs,
      },
      orchestrator_references: {
        total: orchestratorRefs,
        valid: orchestratorRefs - orchestratorBrokenRefs,
        broken: orchestratorBrokenRefs,
        coverage_percent: orchestratorCoverage,
      },
      overall_score: Math.round(overallScore * 100) / 100,
    },
  };
}

if (require.main === module) {
  const metricsFile = process.argv[2];

  if (!metricsFile) {
    console.error("Usage: node measure-integration.js <metrics-file.json>");
    process.exit(1);
  }

  const result = measureIntegrationCompleteness(metricsFile);
  console.log(JSON.stringify(result, null, 2));
}

module.exports = { measureIntegrationCompleteness };
