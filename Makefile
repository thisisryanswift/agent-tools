.PHONY: check sync install test

# Structural checks only; these do not claim behavioral quality.
check:
	python3 scripts/check-skills.py

# Copy prompts/ source of truth into skills/*/references/
sync:
	cp prompts/review-prompt.md skills/code-review/references/review-prompt.md
	cp prompts/tests-prompt.md skills/test-coverage/references/tests-prompt.md
	cp prompts/brainstorming-prompt.md skills/brainstorming/references/brainstorming-prompt.md
	@echo "Synced."

# Choose a destination on the execution host and individual skills explicitly.
install:
	python3 scripts/install-skills.py $(ARGS)

test:
	python3 -m unittest discover -s tests -v
