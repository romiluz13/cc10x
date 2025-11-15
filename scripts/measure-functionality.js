#!/usr/bin/env node
/**
 * Functionality Preservation Measurement Tool
 * Measures Parameter 2: Functionality Preservation Score
 */

const fs = require("fs");
const path = require("path");

// Mapping of deleted skills to consolidated skills
const DELETED_TO_CONSOLIDATED = {
  "security-patterns": "code-review-patterns",
  "code-quality-patterns": "code-review-patterns",
  "performance-patterns": "code-review-patterns",
  "systematic-debugging": "debugging-patterns",
  "log-analysis-patterns": "debugging-patterns",
  "root-cause-analysis": "debugging-patterns",
  "feature-planning": "planning-patterns",
  "requirements-analysis": "planning-patterns",
  "ui-design": "frontend-patterns",
  "ux-patterns": "frontend-patterns",
  "accessibility-patterns": "frontend-patterns",
  "api-design-patterns": "architecture-patterns",
  "integration-patterns": "architecture-patterns",
};

// Mapping of deleted hooks to preserved functionality
const HOOK_PRESERVATION = {
  "notify-compact.sh": {
    preserved: false,
    reason: "Intentional simplification",
  },
  "notify-workflow-complete.sh": {
    preserved: false,
    reason: "Intentional simplification",
  },
  "pre-prompt.sh": {
    preserved: true,
    reason: "Moved to skill-discovery skill",
  },
  "session-start.sh": {
    preserved: true,
    reason: "Simplified in post-compact.sh",
  },
  "user-prompt-submit.sh": {
    preserved: false,
    reason: "Intentional simplification",
  },
};

// Mapping of deleted subagents to preserved functionality
const SUBAGENT_PRESERVATION = {
  "analysis-performance-quality": {
    preserved: true,
    consolidated_into: "code-reviewer",
  },
  "analysis-risk-security": {
    preserved: true,
    consolidated_into: "code-reviewer",
  },
  "analysis-ux-accessibility": {
    preserved: true,
    consolidated_into: "code-reviewer",
  },
  "planning-architecture-risk": {
    preserved: true,
    consolidated_into: "planner",
  },
  "planning-design-deployment": {
    preserved: true,
    consolidated_into: "planner",
  },
};

function measureFunctionalityPreservation(preMetricsFile, postMetricsFile) {
  const preMetrics = JSON.parse(fs.readFileSync(preMetricsFile, "utf-8"));
  const postMetrics = JSON.parse(fs.readFileSync(postMetricsFile, "utf-8"));

  // Identify deleted skills
  const preSkills = new Set(preMetrics.skill_names || []);
  const postSkills = new Set(postMetrics.skill_names || []);
  const deletedSkills = [...preSkills].filter((s) => !postSkills.has(s));

  // Identify deleted hooks
  const preHooks = new Set(preMetrics.hook_names || []);
  const postHooks = new Set(postMetrics.hook_names || []);
  const deletedHooks = [...preHooks].filter((h) => !postHooks.has(h));

  // Identify deleted subagents
  const preSubagents = new Set(preMetrics.subagent_names || []);
  const postSubagents = new Set(postMetrics.subagent_names || []);
  const deletedSubagents = [...preSubagents].filter(
    (s) => !postSubagents.has(s),
  );

  // Calculate preservation scores
  let skillsPreserved = 0;
  let skillsTotal = deletedSkills.length;
  const skillMappings = [];

  for (const deletedSkill of deletedSkills) {
    if (DELETED_TO_CONSOLIDATED[deletedSkill]) {
      skillsPreserved++;
      skillMappings.push({
        deleted: deletedSkill,
        consolidated_into: DELETED_TO_CONSOLIDATED[deletedSkill],
        preserved: true,
      });
    } else {
      skillMappings.push({
        deleted: deletedSkill,
        consolidated_into: null,
        preserved: false,
      });
    }
  }

  let hooksPreserved = 0;
  let hooksTotal = deletedHooks.length;
  const hookMappings = [];

  for (const deletedHook of deletedHooks) {
    const preservation = HOOK_PRESERVATION[deletedHook];
    if (preservation && preservation.preserved) {
      hooksPreserved++;
    }
    hookMappings.push({
      deleted: deletedHook,
      preserved: preservation ? preservation.preserved : false,
      reason: preservation ? preservation.reason : "Unknown",
    });
  }

  let subagentsPreserved = 0;
  let subagentsTotal = deletedSubagents.length;
  const subagentMappings = [];

  for (const deletedSubagent of deletedSubagents) {
    const preservation = SUBAGENT_PRESERVATION[deletedSubagent];
    if (preservation && preservation.preserved) {
      subagentsPreserved++;
    }
    subagentMappings.push({
      deleted: deletedSubagent,
      preserved: preservation ? preservation.preserved : false,
      consolidated_into: preservation ? preservation.consolidated_into : null,
    });
  }

  // Calculate overall preservation score
  const skillsScore =
    skillsTotal > 0 ? (skillsPreserved / skillsTotal) * 100 : 100;
  const hooksScore = hooksTotal > 0 ? (hooksPreserved / hooksTotal) * 100 : 100;
  const subagentsScore =
    subagentsTotal > 0 ? (subagentsPreserved / subagentsTotal) * 100 : 100;

  // Weighted average (skills are most important)
  const overallScore =
    skillsScore * 0.7 + hooksScore * 0.15 + subagentsScore * 0.15;

  return {
    parameter: "Functionality Preservation Score",
    metrics: {
      skills: {
        deleted_count: skillsTotal,
        preserved_count: skillsPreserved,
        score: Math.round(skillsScore * 100) / 100,
        mappings: skillMappings,
      },
      hooks: {
        deleted_count: hooksTotal,
        preserved_count: hooksPreserved,
        score: Math.round(hooksScore * 100) / 100,
        mappings: hookMappings,
      },
      subagents: {
        deleted_count: subagentsTotal,
        preserved_count: subagentsPreserved,
        score: Math.round(subagentsScore * 100) / 100,
        mappings: subagentMappings,
      },
      overall_score: Math.round(overallScore * 100) / 100,
    },
  };
}

if (require.main === module) {
  const preMetricsFile = process.argv[2];
  const postMetricsFile = process.argv[3];

  if (!preMetricsFile || !postMetricsFile) {
    console.error(
      "Usage: node measure-functionality.js <pre-metrics.json> <post-metrics.json>",
    );
    process.exit(1);
  }

  const result = measureFunctionalityPreservation(
    preMetricsFile,
    postMetricsFile,
  );
  console.log(JSON.stringify(result, null, 2));
}

module.exports = { measureFunctionalityPreservation };
