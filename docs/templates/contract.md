# Sprint Contract — Round 2

### Scope
Fix the critical default step value bug ( Round 1 acceptance criterion #6 violation ) and elevate the Counter App with a distinctive visual identity. Transform the app from a generic template into a premium, personality-rich product.

### Deliverables
- **index.html** — Updated single-file implementation with:
  - **BUG FIX FIRST** — Default step value corrected to 1 (no localStorage state on fresh load)
  - Custom SVG iconography (favicon, decorative accents)
  - Redesigned counter display: premium typography (custom font, gradient fill or soft glow, subtle ambient pulse)
  - Tactile button design: depth through gradients/shadows, visible 3D press effect on tap, hover lift effect
  - Polished step selector: smooth sliding pill indicator (200-300ms transition), clear active state
  - Meaningful microcopy: limit feedback ("You're at the limit"), first-load hint, branded tagline

### Acceptance Criteria

1. **Bug Fix Verification** — Fresh load (clear localStorage first): tap the + button once. Counter changes from 0 to exactly 1 (not 5). The "1" step button shows active state.

2. **Custom Visual Identity** — At least 2 custom SVG elements present (e.g., custom favicon, button icon, decorative accent). App looks distinctive, not like a generic template.

3. **Elevated Counter Display** — Number uses at least 2 of: custom font from Google Fonts, gradient text fill, soft glow/shadow, ambient pulse animation. Not plain bold system text.

4. **Tactile Button Design** — +/- buttons have depth (gradient fills, shadows). On tap: button visibly depresses with transform (not just color change). On hover: subtle lift/scale effect.

5. **Polished Step Selector** — Background pill slides smoothly (200-300ms) between options when tapping. Active option is visually distinct with clear hierarchy.

6. **Meaningful Microcopy** — At least one contextual message beyond "Long-press to reset". Examples: limit feedback when hitting min/max, helper text on first load, branded tagline. No placeholder text.

7. **All Round 1 Functionality Preserved** — Verified by:
   - Increment/decrement works
   - Long-press (500ms) on counter resets to 0
   - Keyboard: Arrow Up/Down changes count, R resets
   - Min/max limits clamp correctly
   - localStorage persists state across refresh
   - Bounce animation on counter, pulse on button press

8. **Responsive & Accessible** — Touch targets ≥44px, visible focus states, aria-labels on interactive elements.

### Out of Scope
- Count history/undo feature (from user story #6)
- Backend or API changes
- Multi-file refactoring (single HTML file)
- Browser compatibility beyond modern browsers
