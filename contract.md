APPROVED

---

# Sprint Contract — Round 1

### Scope

This sprint focuses on building the Counter App from scratch. The implementation will deliver all Core Features and the most commonly-used Enhanced Features (step size, keyboard support, visual feedback, min/max limits). The count history feature with undo capability will be deferred to a future round.

### Deliverables

- `index.html` — Single-file implementation with embedded CSS and JavaScript
- All functionality working offline (no external dependencies except system fonts)
- Responsive design working on mobile and desktop browsers

### Acceptance Criteria

1. **Initial Load** — Page loads showing counter at 0 with centered card layout (320px wide, white background, soft shadow).

2. **Increment** — Tapping the "+" button increases the count by the selected step value. Button shows 5% scale-down animation on press. Green color (#34C759).

3. **Decrement** — Tapping the "−" button decreases the count by the selected step value. Button shows 5% scale-down animation on press. Red color (#FF3B30).

4. **Counter Display** — Current count displays at 72px bold font in the center. Number uses tabular-nums so width stays stable during changes.

5. **Visual Feedback** — Counter value animates with a subtle bounce/scale effect on each change. Buttons show visual pulse animation on press.

6. **Step Size Selection** — Three-option segmented control above buttons allows selecting step of 1, 5, or 10. Default is 1.

7. **Reset Functionality** — Long-press (500ms) on the counter display resets count to 0. Reset animation plays.

8. **Keyboard Support** — Arrow Up increases count by step value, Arrow Down decreases by step value, R key resets to 0.

9. **Min/Max Limits** — Optional limits input fields below counter. When set, counter cannot exceed bounds. Default: no limits (empty fields).

10. **Persistence** — Counter value and step size persist across page refresh via localStorage.

11. **Mobile-Friendly** — All buttons have minimum 44px touch target size. Layout works on 320px-wide screens.

12. **Color Compliance** — Increment button uses green (#34C759), decrement button uses red (#FF3B30), background is soft gray (#F5F5F7), card is white (#FFFFFF).

### Out of Scope

- Count history and undo functionality (deferred to Round 2)
- Haptic/vibration feedback (mobile device limitation in pure web)
- Custom fonts (using system font stack only)
- Theming or color customization
- Auto-save indicators or status messages
