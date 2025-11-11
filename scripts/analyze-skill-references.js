#!/usr/bin/env node
/**
 * Skill Reference Analyzer
 * Analyzes all skills and their references in workflows
 * Builds dependency tree and identifies orphaned skills/subagents
 */

const fs = require("fs");
const path = require("path");

const SKILLS_DIR = "plugins/cc10x/skills";
const WORKFLOWS_DIR = "plugins/cc10x/skills/cc10x-orchestrator/workflows";

// Get all skills
function getAllSkills() {
  const skillsDir = path.join(process.cwd(), SKILLS_DIR);
  const skills = [];

  if (!fs.existsSync(skillsDir)) {
    console.error(`Skills directory not found: ${skillsDir}`);
    return skills;
  }

  const entries = fs.readdirSync(skillsDir, { withFileTypes: true });

  for (const entry of entries) {
    if (entry.isDirectory()) {
      const skillPath = path.join(entry.name, "SKILL.md");
      const fullPath = path.join(skillsDir, entry.name, "SKILL.md");

      if (fs.existsSync(fullPath)) {
        skills.push({
          name: entry.name,
          path: skillPath,
          fullPath: fullPath,
        });
      }
    }
  }

  return skills.sort((a, b) => a.name.localeCompare(b.name));
}

// Extract skill references from workflow files
function extractSkillReferences(workflowPath) {
  const content = fs.readFileSync(workflowPath, "utf-8");
  const skillRefs = new Set();

  // Pattern: `skill-name` or `skill-name` - **MANDATORY**
  const skillPattern = /`([a-z0-9-]+)`/g;
  let match;

  while ((match = skillPattern.exec(content)) !== null) {
    const skillName = match[1];
    // Skip common false positives
    if (
      ![
        "skill",
        "skills",
        "subagent",
        "subagents",
        "workflow",
        "workflows",
      ].includes(skillName)
    ) {
      skillRefs.add(skillName);
    }
  }

  // Also check for skill loading sections
  const loadingPattern = /Load.*?`([a-z0-9-]+)`/gi;
  while ((match = loadingPattern.exec(content)) !== null) {
    skillRefs.add(match[1]);
  }

  return Array.from(skillRefs);
}

// Extract subagent references
function extractSubagentReferences(workflowPath) {
  const content = fs.readFileSync(workflowPath, "utf-8");
  const subagents = new Set();

  // Pattern: subagent names like bug-investigator, code-reviewer, etc.
  const subagentPattern =
    /`([a-z-]+-(?:investigator|reviewer|verifier|builder|planner))`/g;
  let match;

  while ((match = subagentPattern.exec(content)) !== null) {
    subagents.add(match[1]);
  }

  // Also check for Task invocations
  const taskPattern = /Task\([^)]*subagent[^)]*["']([a-z-]+)["']/gi;
  while ((match = taskPattern.exec(content)) !== null) {
    subagents.add(match[1]);
  }

  return Array.from(subagents);
}

// Analyze all workflows
function analyzeWorkflows() {
  const workflowsDir = path.join(process.cwd(), WORKFLOWS_DIR);
  const workflows = {};

  if (!fs.existsSync(workflowsDir)) {
    console.error(`Workflows directory not found: ${workflowsDir}`);
    return workflows;
  }

  const files = fs.readdirSync(workflowsDir);

  for (const file of files) {
    if (file.endsWith(".md")) {
      const workflowPath = path.join(workflowsDir, file);
      const workflowName = path.basename(file, ".md");

      workflows[workflowName] = {
        path: workflowPath,
        skills: extractSkillReferences(workflowPath),
        subagents: extractSubagentReferences(workflowPath),
      };
    }
  }

  return workflows;
}

// Build dependency tree
function buildDependencyTree(skills, workflows) {
  const tree = {
    orchestrator: {
      workflows: {},
      skills: new Set(),
      subagents: new Set(),
    },
    skills: {},
    subagents: {},
    orphaned: {
      skills: [],
      subagents: [],
    },
  };

  // Map all skills
  for (const skill of skills) {
    tree.skills[skill.name] = {
      referencedIn: [],
      subagents: [],
    };
  }

  // Analyze workflows
  for (const [workflowName, workflow] of Object.entries(workflows)) {
    tree.orchestrator.workflows[workflowName] = {
      skills: workflow.skills,
      subagents: workflow.subagents,
    };

    // Track skill references
    for (const skillName of workflow.skills) {
      tree.orchestrator.skills.add(skillName);
      if (tree.skills[skillName]) {
        tree.skills[skillName].referencedIn.push(workflowName);
      }
    }

    // Track subagent references
    for (const subagentName of workflow.subagents) {
      tree.orchestrator.subagents.add(subagentName);
      if (!tree.subagents[subagentName]) {
        tree.subagents[subagentName] = [];
      }
      tree.subagents[subagentName].push(workflowName);
    }
  }

  // Find orphaned skills
  for (const skill of skills) {
    if (!tree.skills[skill.name].referencedIn.length) {
      tree.orphaned.skills.push(skill.name);
    }
  }

  return tree;
}

// Generate ASCII tree visualization
function generateASCIITree(tree) {
  let output = "\n";
  output += "=".repeat(80) + "\n";
  output += "SKILL & SUBAGENT DEPENDENCY TREE\n";
  output += "=".repeat(80) + "\n\n";

  output += "ORCHESTRATOR\n";
  output += "│\n";
  output += "├─ Workflows:\n";

  for (const [workflowName, workflow] of Object.entries(
    tree.orchestrator.workflows,
  )) {
    output += `│  ├─ ${workflowName}\n`;
    output += `│  │  ├─ Skills (${workflow.skills.length}):\n`;
    for (const skill of workflow.skills.slice(0, 5)) {
      output += `│  │  │  ├─ ${skill}\n`;
    }
    if (workflow.skills.length > 5) {
      output += `│  │  │  └─ ... (+${workflow.skills.length - 5} more)\n`;
    }
    output += `│  │  └─ Subagents (${workflow.subagents.length}):\n`;
    for (const subagent of workflow.subagents) {
      output += `│  │     ├─ ${subagent}\n`;
    }
  }

  output += "\n";
  output += "SKILLS BY WORKFLOW:\n";
  output += "-".repeat(80) + "\n";

  const skillToWorkflows = {};
  for (const [workflowName, workflow] of Object.entries(
    tree.orchestrator.workflows,
  )) {
    for (const skill of workflow.skills) {
      if (!skillToWorkflows[skill]) {
        skillToWorkflows[skill] = [];
      }
      skillToWorkflows[skill].push(workflowName);
    }
  }

  const sortedSkills = Object.keys(skillToWorkflows).sort();
  for (const skill of sortedSkills) {
    const workflows = skillToWorkflows[skill];
    output += `${skill}\n`;
    for (const wf of workflows) {
      output += `  └─ ${wf}\n`;
    }
  }

  output += "\n";
  output += "SUBAGENTS BY WORKFLOW:\n";
  output += "-".repeat(80) + "\n";

  for (const [subagent, workflows] of Object.entries(tree.subagents)) {
    output += `${subagent}\n`;
    for (const wf of workflows) {
      output += `  └─ ${wf}\n`;
    }
  }

  if (tree.orphaned.skills.length > 0) {
    output += "\n";
    output += "⚠️  ORPHANED SKILLS (not referenced in any workflow):\n";
    output += "-".repeat(80) + "\n";
    for (const skill of tree.orphaned.skills) {
      output += `  - ${skill}\n`;
    }
  }

  if (tree.orphaned.subagents.length > 0) {
    output += "\n";
    output += "⚠️  ORPHANED SUBAGENTS (not referenced in any workflow):\n";
    output += "-".repeat(80) + "\n";
    for (const subagent of tree.orphaned.subagents) {
      output += `  - ${subagent}\n`;
    }
  }

  output += "\n";
  output += "=".repeat(80) + "\n";
  output += `Total Skills: ${Object.keys(tree.skills).length}\n`;
  output += `Referenced Skills: ${Object.keys(tree.skills).length - tree.orphaned.skills.length}\n`;
  output += `Orphaned Skills: ${tree.orphaned.skills.length}\n`;
  output += `Total Subagents: ${Object.keys(tree.subagents).length}\n`;
  output += `Orphaned Subagents: ${tree.orphaned.subagents.length}\n`;
  output += "=".repeat(80) + "\n";

  return output;
}

// Main execution
function main() {
  console.log("Analyzing skills and workflows...\n");

  const skills = getAllSkills();
  console.log(`Found ${skills.length} skills`);

  const workflows = analyzeWorkflows();
  console.log(`Found ${Object.keys(workflows).length} workflows`);

  const tree = buildDependencyTree(skills, workflows);

  const visualization = generateASCIITree(tree);
  console.log(visualization);

  // Write to file
  const outputPath = path.join(process.cwd(), "SKILL-DEPENDENCY-TREE.txt");
  fs.writeFileSync(outputPath, visualization);
  console.log(`\nDependency tree written to: ${outputPath}`);

  // Return results for validation
  return {
    totalSkills: skills.length,
    referencedSkills: skills.length - tree.orphaned.skills.length,
    orphanedSkills: tree.orphaned.skills,
    totalSubagents: Object.keys(tree.subagents).length,
    orphanedSubagents: tree.orphaned.subagents,
    tree,
  };
}

if (require.main === module) {
  main();
}

module.exports = { main, getAllSkills, analyzeWorkflows, buildDependencyTree };
