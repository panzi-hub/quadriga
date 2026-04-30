# Counter App - Product Specification

## 1. Overview

**Product Name:** Counter App  
**Type:** Simple interactive web application  
**Core Functionality:** A clean, intuitive counter that allows users to increment and decrement a numerical value with immediate visual feedback.  
**Target Users:** Anyone needing a quick, elegant way to count items, track numbers, or manage simple tallies.

---

## 2. Features

### Core Features
1. **Display Counter** — Shows the current count value prominently in the center of the screen.
2. **Increment Button** — Increases the counter by 1 when clicked.
3. **Decrement Button** — Decreases the counter by 1 when clicked.
4. **Reset Functionality** — Double-tap or long-press to reset counter to zero.

### Enhanced Features
5. **Step Size Option** — User can select increment/decrement amount (1, 5, 10).
6. **Count History** — Shows last 5 operations with undo capability.
7. **Keyboard Support** — Arrow keys (Up/Down) for increment/decrement, R to reset.
8. **Haptic Feedback** — Visual pulse animation on button press.
9. **Min/Max Limits** — Configurable boundaries (default: no limits).

---

## 3. User Stories

| # | Story |
|---|-------|
| 1 | As a user, I want to tap a large "+" button to increase the count so I can quickly tally items. |
| 2 | As a user, I want to tap a "−" button to decrease the count in case I tap too many. |
| 3 | As a user, I want to see the current count displayed clearly so I know the total at a glance. |
| 4 | As a user, I want haptic/visual feedback on each tap so the app feels responsive. |
| 5 | As a user, I want to change the step size so I can count in batches (e.g., +5 at a time). |
| 6 | As a user, I want to undo my last action so I can correct mistakes. |

---

## 4. Technical Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Vanilla HTML/CSS/JavaScript (single file, no dependencies) |
| **Fonts** | System font stack for performance |
| **Animations** | CSS transitions + keyframes |
| **State Management** | Simple JavaScript object with localStorage persistence |
| **Responsive** | CSS Flexbox, works on mobile and desktop |

---

## 5. Design Direction

### Visual Style
- **Aesthetic:** Minimalist, modern, with subtle depth through soft shadows.
- **Feel:** Clean, calm, professional — like a premium calculator app.

### Color Palette
| Element | Color |
|---------|-------|
| Background | `#F5F5F7` (soft gray) |
| Card/Surface | `#FFFFFF` (white) |
| Primary (Increment) | `#34C759` (vibrant green) |
| Secondary (Decrement) | `#FF3B30` (clear red) |
| Text (Count) | `#1D1D1F` (near-black) |
| Text (Secondary) | `#86868B` (muted gray) |

### Typography
- **Counter Display:** 72px, bold, tabular-nums for stable width during updates
- **Buttons:** 48px bold symbols (+/−)
- **Labels:** 14px medium weight

### Layout
- **Structure:** Centered card on page
- **Card Size:** 320px wide, auto height
- **Spacing:** Generous padding (32px)
- **Button Size:** 64px circular touch targets

### Interaction Design
- Buttons scale down 5% on press (active state)
- Counter value animates with a subtle bounce on change
- Undo button appears as a pill below the counter
- Step selector is a subtle segmented control above the buttons

---

## 6. File Structure

```
/
├── spec.md          (this file)
└── index.html       (single-file implementation with embedded CSS/JS)
```

---

## 7. Acceptance Criteria

- [ ] Counter displays 0 on initial load
- [ ] Tapping "+" increases count by step value
- [ ] Tapping "−" decreases count by step value
- [ ] Counter persists across page refresh (localStorage)
- [ ] Undo restores previous count
- [ ] Keyboard navigation works (arrows, R)
- [ ] Mobile-friendly touch targets (min 44px)
- [ ] No external dependencies