.PHONY: check sync install

# Verify that skills/*/references/ copies match prompts/ source of truth
check:
	@echo "Checking skills references are in sync with prompts..."
	@fail=0; \
	for skill_ref in skills/*/references/*.md; do \
		prompt_name=$$(basename "$$skill_ref"); \
		if [ -f "prompts/$$prompt_name" ]; then \
			if ! diff -q "prompts/$$prompt_name" "$$skill_ref" > /dev/null 2>&1; then \
				echo "DRIFT: prompts/$$prompt_name != $$skill_ref"; \
				fail=1; \
			fi; \
		fi; \
	done; \
	if [ $$fail -eq 1 ]; then \
		echo ""; \
		echo "Run 'make sync' to copy prompts/ into skills/*/references/"; \
		exit 1; \
	fi
	@echo "All references in sync."

# Copy prompts/ source of truth into skills/*/references/
sync:
	cp prompts/review-prompt.md skills/code-review/references/review-prompt.md
	cp prompts/tests-prompt.md skills/test-coverage/references/tests-prompt.md
	cp prompts/brainstorming-prompt.md skills/brainstorming/references/brainstorming-prompt.md
	cp prompts/jules-prompt.md skills/jules/references/jules-prompt.md
	@echo "Synced."

# Install to ~/.config/opencode/ (manual alternative to chezmoi externals)
install:
	mkdir -p ~/.config/opencode/agents ~/.config/opencode/command ~/.config/opencode/prompts ~/.config/opencode/plugin
	cp prompts/*.md ~/.config/opencode/prompts/
	cp agent/*.md ~/.config/opencode/agents/
	cp command/*.md ~/.config/opencode/command/
	cp plugin/*.ts ~/.config/opencode/plugin/
	@echo "Installed to ~/.config/opencode/"
	@echo "Restart OpenCode for changes to take effect."
