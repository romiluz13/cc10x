#!/usr/bin/env node
/**
 * Token Efficiency Measurement Tool
 * Measures Parameter 3: Token Efficiency
 */

const fs = require("fs");
const path = require("path");

// Rough token estimation: ~4 characters per token
const CHARS_PER_TOKEN = 4;

function estimateTokens(text) {
  return Math.ceil(text.length / CHARS_PER_TOKEN);
}

function measureTokenEfficiency(preMetricsFile, postMetricsFile) {
  const preMetrics = JSON.parse(fs.readFileSync(preMetricsFile, "utf-8"));
  const postMetrics = JSON.parse(fs.readFileSync(postMetricsFile, "utf-8"));

  // Estimate tokens from line counts (rough approximation)
  // Average line is ~80 characters, so lines * 80 / 4 = tokens
  const preSkillsTokens = Math.round(
    ((parseInt(preMetrics.skills_lines) || 0) * 80) / CHARS_PER_TOKEN,
  );
  const postSkillsTokens = Math.round(
    ((parseInt(postMetrics.skills_lines) || 0) * 80) / CHARS_PER_TOKEN,
  );

  const preHooksTokens = Math.round(
    ((parseInt(preMetrics.hooks_lines) || 0) * 80) / CHARS_PER_TOKEN,
  );
  const postHooksTokens = Math.round(
    ((parseInt(postMetrics.hooks_lines) || 0) * 80) / CHARS_PER_TOKEN,
  );

  const preSubagentsTokens = Math.round(
    ((parseInt(preMetrics.subagents_lines) || 0) * 80) / CHARS_PER_TOKEN,
  );
  const postSubagentsTokens = Math.round(
    ((parseInt(postMetrics.subagents_lines) || 0) * 80) / CHARS_PER_TOKEN,
  );

  const preTotalTokens = preSkillsTokens + preHooksTokens + preSubagentsTokens;
  const postTotalTokens =
    postSkillsTokens + postHooksTokens + postSubagentsTokens;

  // Calculate average tokens per skill
  const preAvgTokensPerSkill =
    preMetrics.skills_count > 0
      ? Math.round(preSkillsTokens / preMetrics.skills_count)
      : 0;
  const postAvgTokensPerSkill =
    postMetrics.skills_count > 0
      ? Math.round(postSkillsTokens / postMetrics.skills_count)
      : 0;

  // Calculate consolidation efficiency
  const tokensSaved = preTotalTokens - postTotalTokens;
  const consolidationEfficiency =
    preTotalTokens > 0
      ? Math.round((tokensSaved / preTotalTokens) * 100 * 100) / 100
      : 0;

  // Calculate reduction ratio
  const reductionRatio =
    preTotalTokens > 0
      ? Math.round((postTotalTokens / preTotalTokens) * 100 * 100) / 100
      : 0;

  return {
    parameter: "Token Efficiency",
    metrics: {
      pre_refactor: {
        skills_tokens: preSkillsTokens,
        hooks_tokens: preHooksTokens,
        subagents_tokens: preSubagentsTokens,
        total_tokens: preTotalTokens,
        avg_tokens_per_skill: preAvgTokensPerSkill,
        skills_count: preMetrics.skills_count,
      },
      post_refactor: {
        skills_tokens: postSkillsTokens,
        hooks_tokens: postHooksTokens,
        subagents_tokens: postSubagentsTokens,
        total_tokens: postTotalTokens,
        avg_tokens_per_skill: postAvgTokensPerSkill,
        skills_count: postMetrics.skills_count,
      },
      efficiency: {
        tokens_saved: tokensSaved,
        consolidation_efficiency_percent: consolidationEfficiency,
        reduction_ratio_percent: reductionRatio,
        improvement: tokensSaved > 0 ? "Better" : "Worse",
      },
    },
  };
}

if (require.main === module) {
  const preMetricsFile = process.argv[2];
  const postMetricsFile = process.argv[3];

  if (!preMetricsFile || !postMetricsFile) {
    console.error(
      "Usage: node measure-tokens.js <pre-metrics.json> <post-metrics.json>",
    );
    process.exit(1);
  }

  const result = measureTokenEfficiency(preMetricsFile, postMetricsFile);
  console.log(JSON.stringify(result, null, 2));
}

module.exports = { measureTokenEfficiency };
