import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const deck = await readFile(
	new URL("../keynote.html", import.meta.url),
	"utf8",
);

test("presents Harness & Loop Engineering as an Electric Print field guide", () => {
	assert.match(
		deck,
		/<title>Harness & Loop Engineering — A Field Guide<\/title>/,
	);
	assert.match(deck, /assets\/fonts\/archivo-900\.ttf/);
	assert.doesNotMatch(deck, /fonts\.googleapis\.com/);
	assert.match(deck, /--paper:/);
	assert.match(deck, /--warning:/);
	assert.match(deck, /--cobalt:/);
	assert.match(
		deck,
		/BUILD THE[\s\S]*OPERATING[\s\S]*SYSTEM[\s\S]*AROUND[\s\S]*THE[\s\S]*AGENT/i,
	);
	assert.match(deck, /data-section="Harness Engineering"/);
	assert.match(deck, /data-section="Loop Engineering"/);
	assert.match(deck, /data-section="Workflow System"/);
	assert.match(deck, /data-section="Production"/);
	assert.equal(
		(deck.match(/<(?:div|section) class="slide(?:\s|"|$)/g) ?? []).length,
		19,
	);
	assert.match(deck, /openai\.com\/index\/harness-engineering\//);
	assert.match(deck, /anthropic\.com\/engineering\/building-effective-agents/);
	assert.match(
		deck,
		/langchain\.com\/blog\/how-to-build-a-custom-agent-harness/,
	);
	assert.match(deck, /class="workflow four"/);
	assert.match(deck, /EVIDENCE → APPROVE · REPAIR · RE-PLAN · ESCALATE/);
	assert.match(deck, /PROVE → RE-PLAN/);
	assert.match(deck, /PROVE → REPAIR BUILD/);
	assert.match(deck, /PROVE → ESCALATE HUMAN/);
	assert.match(deck, /PROVE → PRESERVE HANDOFF/);
	assert.match(deck, /ENTRY POINTS: PLAN · DEBUG · REVIEW/);
	assert.match(deck, /FOR CONSEQUENTIAL[\s\S]*INDEPENDENT CHALLENGE/);
	assert.match(deck, /A HOST-SPECIFIC POC\. ITS CONCRETE MECHANISMS\s+BELONG/);
	assert.doesNotMatch(
		deck,
		/WORKFLOW ACTIVATION · SKILLS · PHASE ROLES · JOURNAL STATE/i,
	);
	assert.doesNotMatch(deck, /cc10x is the only Claude Code plugin/i);
	assert.doesNotMatch(deck, /Stop chasing better models/i);
	assert.doesNotMatch(deck, /font-size: (?:11|12|13)px/);
});

test("keeps the keynote navigation contract", () => {
	assert.match(
		deck,
		/const slides = Array\.from\(document\.querySelectorAll\("\.slide"\)\)/,
	);
	assert.match(deck, /document\.addEventListener\("keydown"/);
	assert.match(deck, /touchstart/);
	assert.match(deck, /slideCounter\.textContent/);
	assert.match(deck, /sectionLabel\.textContent/);
});
