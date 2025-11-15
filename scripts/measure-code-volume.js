#!/usr/bin/env node
/**
 * Code Volume Measurement Tool
 * Measures Parameter 1: Code Volume & Complexity
 */

const fs = require("fs");
const path = require("path");

function measureCodeVolume(metricsFile) {
  const metrics = JSON.parse(fs.readFileSync(metricsFile, "utf-8"));

  const result = {
    parameter: "Code Volume & Complexity",
    metrics: {
      total_skills: metrics.skills_count,
      total_files: metrics.skills_files_count,
      skill_md_files: metrics.skill_md_count,
      patterns_md_files: metrics.patterns_md_count,
      reference_md_files: metrics.reference_md_count,
      skills_lines: parseInt(metrics.skills_lines) || 0,
      all_skill_files_lines: parseInt(metrics.all_skill_files_lines) || 0,
      hooks_lines: parseInt(metrics.hooks_lines) || 0,
      subagents_lines: parseInt(metrics.subagents_lines) || 0,
      total_lines:
        (parseInt(metrics.all_skill_files_lines) || 0) +
        (parseInt(metrics.hooks_lines) || 0) +
        (parseInt(metrics.subagents_lines) || 0),
      average_lines_per_skill:
        metrics.skills_count > 0
          ? Math.round(
              (parseInt(metrics.all_skill_files_lines) || 0) /
                metrics.skills_count,
            )
          : 0,
    },
  };

  return result;
}

if (require.main === module) {
  const metricsFile = process.argv[2];
  if (!metricsFile) {
    console.error("Usage: node measure-code-volume.js <metrics-file.json>");
    process.exit(1);
  }

  const result = measureCodeVolume(metricsFile);
  console.log(JSON.stringify(result, null, 2));
}

module.exports = { measureCodeVolume };
