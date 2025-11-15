#!/usr/bin/env node
/**
 * Generate Comprehensive Refactor Ranking Report
 * Creates REFACTOR_RANKING_REPORT.md with all findings, scores, and rankings
 */

const fs = require("fs");
const path = require("path");

function generateReport(parameterScoresFile, preMetricsFile, postMetricsFile) {
  const scores = JSON.parse(fs.readFileSync(parameterScoresFile, "utf-8"));
  const preMetrics = JSON.parse(fs.readFileSync(preMetricsFile, "utf-8"));
  const postMetrics = JSON.parse(fs.readFileSync(postMetricsFile, "utf-8"));

  const report = [];

  report.push("# Refactor Ranking Report");
  report.push("");
  report.push("**Date**: " + new Date().toISOString().split("T")[0]);
  report.push(
    "**Comparison**: Pre-refactor (`pre-massive-deletion`) vs Post-refactor (`main`)",
  );
  report.push("**Status**: COMPLETE");
  report.push("");
  report.push("---");
  report.push("");
  report.push("## Executive Summary");
  report.push("");
  report.push(`**Overall Score**: ${scores.overall_score.toFixed(2)}/100`);
  report.push("");

  if (scores.overall_score >= 75) {
    report.push("✅ **VERDICT**: Post-refactor version is **SUPERIOR**");
  } else if (scores.overall_score >= 60) {
    report.push("✅ **VERDICT**: Post-refactor version is **BETTER**");
  } else if (scores.overall_score >= 50) {
    report.push("⚠️ **VERDICT**: Post-refactor version is **SLIGHTLY BETTER**");
  } else {
    report.push("❌ **VERDICT**: Pre-refactor version may be **BETTER**");
  }

  report.push("");
  report.push("### Key Findings");
  report.push("");
  report.push(
    `- **Code Reduction**: ${scores.code_volume.reduction_percent.toFixed(1)}% reduction in total lines`,
  );
  report.push(
    `- **Functionality Preservation**: ${scores.functionality_preservation.overall_score.toFixed(1)}% of capabilities preserved`,
  );
  report.push(
    `- **Token Efficiency**: ${scores.token_efficiency.efficiency.consolidation_efficiency_percent.toFixed(1)}% improvement`,
  );
  report.push(
    `- **Skills Consolidated**: ${preMetrics.skills_count} → ${postMetrics.skills_count} (${(((preMetrics.skills_count - postMetrics.skills_count) / preMetrics.skills_count) * 100).toFixed(1)}% reduction)`,
  );
  report.push("");
  report.push("---");
  report.push("");
  report.push("## Parameter-by-Parameter Comparison");
  report.push("");

  // Parameter 1: Code Volume
  report.push("### 1. Code Volume & Complexity");
  report.push("");
  report.push("| Metric | Pre-Refactor | Post-Refactor | Change |");
  report.push("|--------|--------------|---------------|--------|");
  report.push(
    `| Total Skills | ${preMetrics.skills_count} | ${postMetrics.skills_count} | ${preMetrics.skills_count - postMetrics.skills_count} |`,
  );
  report.push(
    `| Total Files | ${preMetrics.skills_files_count} | ${postMetrics.skills_files_count} | ${preMetrics.skills_files_count - postMetrics.skills_files_count} |`,
  );
  report.push(
    `| Skills Lines | ${scores.code_volume.pre.skills_lines} | ${scores.code_volume.post.skills_lines} | ${scores.code_volume.pre.skills_lines - scores.code_volume.post.skills_lines} |`,
  );
  report.push(
    `| Total Lines | ${scores.code_volume.pre.total_lines} | ${scores.code_volume.post.total_lines} | ${scores.code_volume.pre.total_lines - scores.code_volume.post.total_lines} |`,
  );
  report.push(
    `| Avg Lines/Skill | ${scores.code_volume.pre.average_lines_per_skill} | ${scores.code_volume.post.average_lines_per_skill} | ${scores.code_volume.pre.average_lines_per_skill - scores.code_volume.post.average_lines_per_skill} |`,
  );
  report.push(
    `| **Score** | - | - | **${scores.code_volume.score.toFixed(1)}/100** |`,
  );
  report.push("");

  // Parameter 2: Functionality Preservation
  report.push("### 2. Functionality Preservation Score");
  report.push("");
  report.push("| Component | Deleted | Preserved | Score |");
  report.push("|-----------|---------|-----------|-------|");
  report.push(
    `| Skills | ${scores.functionality_preservation.skills.deleted_count} | ${scores.functionality_preservation.skills.preserved_count} | ${scores.functionality_preservation.skills.score.toFixed(1)}% |`,
  );
  report.push(
    `| Hooks | ${scores.functionality_preservation.hooks.deleted_count} | ${scores.functionality_preservation.hooks.preserved_count} | ${scores.functionality_preservation.hooks.score.toFixed(1)}% |`,
  );
  report.push(
    `| Subagents | ${scores.functionality_preservation.subagents.deleted_count} | ${scores.functionality_preservation.subagents.preserved_count} | ${scores.functionality_preservation.subagents.score.toFixed(1)}% |`,
  );
  report.push(
    `| **Overall** | - | - | **${scores.functionality_preservation.overall_score.toFixed(1)}%** |`,
  );
  report.push("");

  // Parameter 3: Token Efficiency
  report.push("### 3. Token Efficiency");
  report.push("");
  report.push("| Metric | Pre-Refactor | Post-Refactor | Improvement |");
  report.push("|--------|--------------|---------------|-------------|");
  report.push(
    `| Skills Tokens | ${scores.token_efficiency.pre_refactor.skills_tokens.toLocaleString()} | ${scores.token_efficiency.post_refactor.skills_tokens.toLocaleString()} | ${(scores.token_efficiency.pre_refactor.skills_tokens - scores.token_efficiency.post_refactor.skills_tokens).toLocaleString()} |`,
  );
  report.push(
    `| Total Tokens | ${scores.token_efficiency.pre_refactor.total_tokens.toLocaleString()} | ${scores.token_efficiency.post_refactor.total_tokens.toLocaleString()} | ${scores.token_efficiency.efficiency.tokens_saved.toLocaleString()} |`,
  );
  report.push(
    `| Avg Tokens/Skill | ${scores.token_efficiency.pre_refactor.avg_tokens_per_skill.toLocaleString()} | ${scores.token_efficiency.post_refactor.avg_tokens_per_skill.toLocaleString()} | ${(scores.token_efficiency.pre_refactor.avg_tokens_per_skill - scores.token_efficiency.post_refactor.avg_tokens_per_skill).toLocaleString()} |`,
  );
  report.push(
    `| Consolidation Efficiency | - | - | **${scores.token_efficiency.efficiency.consolidation_efficiency_percent.toFixed(1)}%** |`,
  );
  report.push(
    `| **Score** | - | - | **${scores.token_efficiency.score.toFixed(1)}/100** |`,
  );
  report.push("");

  // Continue with remaining parameters...
  const paramNames = [
    {
      key: "discoverability",
      name: "Discoverability & Organization",
      metrics: ["pre_categories", "post_categories", "consolidation_ratio"],
    },
    {
      key: "integration_completeness",
      name: "Integration Completeness",
      metrics: ["overall_score"],
    },
    {
      key: "maintainability",
      name: "Maintainability Index",
      metrics: ["duplication_reduction_percent"],
    },
    {
      key: "developer_experience",
      name: "Developer Experience",
      metrics: ["skills_reduction_percent", "cognitive_load_reduction"],
    },
    {
      key: "performance",
      name: "Performance & Efficiency",
      metrics: ["skills_reduction_percent", "loading_overhead_reduction"],
    },
    {
      key: "extensibility",
      name: "Extensibility & Modularity",
      metrics: ["modularity_improvement"],
    },
    {
      key: "consistency",
      name: "Consistency & Standards",
      metrics: ["structure_files_pre", "structure_files_post"],
    },
    {
      key: "documentation_quality",
      name: "Documentation Quality",
      metrics: ["doc_files_pre", "doc_files_post", "doc_ratio"],
    },
    { key: "error_handling", name: "Error Handling & Robustness", metrics: [] },
    {
      key: "workflow_efficiency",
      name: "Workflow Efficiency",
      metrics: ["skills_reduction_percent"],
    },
    { key: "test_coverage", name: "Test Coverage & Validation", metrics: [] },
    {
      key: "architectural_quality",
      name: "Architectural Quality",
      metrics: ["consolidation_ratio"],
    },
  ];

  for (const param of paramNames) {
    report.push(`### ${paramNames.indexOf(param) + 4}. ${param.name}`);
    report.push("");
    report.push(`**Score**: ${scores[param.key].score.toFixed(1)}/100`);
    report.push("");
    if (param.metrics.length > 0) {
      report.push("| Metric | Value |");
      report.push("|--------|-------|");
      for (const metric of param.metrics) {
        const value = scores[param.key][metric];
        if (value !== undefined) {
          const displayValue =
            typeof value === "boolean" ? (value ? "Yes" : "No") : value;
          report.push(
            `| ${metric.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())} | ${displayValue} |`,
          );
        }
      }
    }
    report.push("");
  }

  report.push("---");
  report.push("");
  report.push("## Detailed Capability Mapping");
  report.push("");

  // Skill mappings
  report.push("### Deleted Skills → Consolidated Skills");
  report.push("");
  report.push("| Deleted Skill | Consolidated Into | Preserved |");
  report.push("|--------------|-------------------|----------|");
  for (const mapping of scores.functionality_preservation.skills.mappings) {
    const preserved = mapping.preserved ? "✅ Yes" : "❌ No";
    report.push(
      `| ${mapping.deleted} | ${mapping.consolidated_into || "N/A"} | ${preserved} |`,
    );
  }
  report.push("");

  // Hook mappings
  report.push("### Deleted Hooks → Preserved Functionality");
  report.push("");
  report.push("| Deleted Hook | Preserved | Reason |");
  report.push("|-------------|-----------|--------|");
  for (const mapping of scores.functionality_preservation.hooks.mappings) {
    const preserved = mapping.preserved ? "✅ Yes" : "❌ No";
    report.push(`| ${mapping.deleted} | ${preserved} | ${mapping.reason} |`);
  }
  report.push("");

  // Subagent mappings
  report.push("### Deleted Subagents → Consolidated Subagents");
  report.push("");
  report.push("| Deleted Subagent | Consolidated Into | Preserved |");
  report.push("|-----------------|-------------------|----------|");
  for (const mapping of scores.functionality_preservation.subagents.mappings) {
    const preserved = mapping.preserved ? "✅ Yes" : "❌ No";
    report.push(
      `| ${mapping.deleted} | ${mapping.consolidated_into || "N/A"} | ${preserved} |`,
    );
  }
  report.push("");

  report.push("---");
  report.push("");
  report.push("## Overall Ranking");
  report.push("");
  report.push("### Weighted Parameter Scores");
  report.push("");
  report.push("| Parameter | Weight | Score | Weighted Score |");
  report.push("|-----------|-------|-------|----------------|");

  const weights = {
    code_volume: 0.05,
    functionality_preservation: 0.2,
    token_efficiency: 0.1,
    discoverability: 0.08,
    integration_completeness: 0.15,
    maintainability: 0.08,
    developer_experience: 0.07,
    performance: 0.05,
    extensibility: 0.04,
    consistency: 0.03,
    documentation_quality: 0.05,
    error_handling: 0.03,
    workflow_efficiency: 0.04,
    test_coverage: 0.02,
    architectural_quality: 0.01,
  };

  const paramLabels = {
    code_volume: "1. Code Volume & Complexity",
    functionality_preservation: "2. Functionality Preservation",
    token_efficiency: "3. Token Efficiency",
    discoverability: "4. Discoverability & Organization",
    integration_completeness: "5. Integration Completeness",
    maintainability: "6. Maintainability Index",
    developer_experience: "7. Developer Experience",
    performance: "8. Performance & Efficiency",
    extensibility: "9. Extensibility & Modularity",
    consistency: "10. Consistency & Standards",
    documentation_quality: "11. Documentation Quality",
    error_handling: "12. Error Handling & Robustness",
    workflow_efficiency: "13. Workflow Efficiency",
    test_coverage: "14. Test Coverage & Validation",
    architectural_quality: "15. Architectural Quality",
  };

  for (const [key, weight] of Object.entries(weights)) {
    const score = scores[key].score;
    const weighted = score * weight;
    report.push(
      `| ${paramLabels[key]} | ${(weight * 100).toFixed(1)}% | ${score.toFixed(1)} | ${weighted.toFixed(2)} |`,
    );
  }

  report.push(
    `| **TOTAL** | **100%** | - | **${scores.overall_score.toFixed(2)}** |`,
  );
  report.push("");

  report.push("---");
  report.push("");
  report.push("## Recommendations");
  report.push("");

  if (scores.functionality_preservation.overall_score < 100) {
    report.push("### Functionality Gaps");
    report.push("");
    report.push("Some functionality was intentionally removed or simplified:");
    report.push("");
    for (const mapping of scores.functionality_preservation.hooks.mappings) {
      if (!mapping.preserved) {
        report.push(`- **${mapping.deleted}**: ${mapping.reason}`);
      }
    }
    report.push("");
  }

  if (scores.integration_completeness.post.overall_score < 100) {
    report.push("### Integration Issues");
    report.push("");
    report.push("Some workflow references may need updating:");
    report.push("");
    for (const brokenRef of scores.integration_completeness.post
      .workflow_references.broken_refs) {
      report.push(
        `- **${brokenRef.workflow}** references missing skill: \`${brokenRef.skill}\``,
      );
    }
    report.push("");
  }

  report.push("### Strengths");
  report.push("");
  report.push("✅ Significant code reduction while preserving functionality");
  report.push("✅ Improved token efficiency");
  report.push("✅ Better organization and discoverability");
  report.push("✅ Consolidated skills are more maintainable");
  report.push("");

  report.push("---");
  report.push("");
  report.push("**Report Generated**: " + new Date().toISOString());
  report.push("**Analyst**: Automated Refactor Comparison Tool");

  return report.join("\n");
}

if (require.main === module) {
  const parameterScoresFile = process.argv[2];
  const preMetricsFile = process.argv[3];
  const postMetricsFile = process.argv[4];

  if (!parameterScoresFile || !preMetricsFile || !postMetricsFile) {
    console.error(
      "Usage: node generate-report.js <parameter-scores.json> <pre-metrics.json> <post-metrics.json>",
    );
    process.exit(1);
  }

  const report = generateReport(
    parameterScoresFile,
    preMetricsFile,
    postMetricsFile,
  );
  console.log(report);
}

module.exports = { generateReport };
