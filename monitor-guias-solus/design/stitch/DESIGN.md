---
name: Clinical Precision
colors:
  surface: '#f7fafa'
  surface-dim: '#d7dbdb'
  surface-bright: '#f7fafa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f4f4'
  surface-container: '#ebeeee'
  surface-container-high: '#e5e9e9'
  surface-container-highest: '#e0e3e3'
  on-surface: '#181c1d'
  on-surface-variant: '#3e4949'
  inverse-surface: '#2d3131'
  inverse-on-surface: '#eef1f1'
  outline: '#6e797a'
  outline-variant: '#bdc9c9'
  surface-tint: '#00696e'
  primary: '#006065'
  on-primary: '#ffffff'
  primary-container: '#0d7a80'
  on-primary-container: '#c7fbff'
  inverse-primary: '#7dd4db'
  secondary: '#3755c3'
  on-secondary: '#ffffff'
  secondary-container: '#708cfd'
  on-secondary-container: '#00217a'
  tertiary: '#82461d'
  on-tertiary: '#ffffff'
  tertiary-container: '#9f5d32'
  on-tertiary-container: '#ffeee7'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#99f1f7'
  primary-fixed-dim: '#7dd4db'
  on-primary-fixed: '#002022'
  on-primary-fixed-variant: '#004f53'
  secondary-fixed: '#dde1ff'
  secondary-fixed-dim: '#b8c4ff'
  on-secondary-fixed: '#001453'
  on-secondary-fixed-variant: '#173bab'
  tertiary-fixed: '#ffdbc8'
  tertiary-fixed-dim: '#ffb68b'
  on-tertiary-fixed: '#321200'
  on-tertiary-fixed-variant: '#70370f'
  background: '#f7fafa'
  on-background: '#181c1d'
  surface-variant: '#e0e3e3'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  title-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  data-mono:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  container-padding: 24px
  gutter: 16px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style
The design system is engineered for high-stakes oncology data management, where clarity saves time and reduces cognitive load. The brand personality is authoritative yet supportive, characterized by a **Corporate / Modern** aesthetic that prioritizes information density and accessibility. 

The visual language utilizes a "Clean Precision" approach: high whitespace efficiency, rigorous alignment, and a systematic use of semantic color to provide immediate status recognition. The goal is to evoke a sense of reliability and calm in a complex medical administrative environment.

## Colors
This design system employs a specialized healthcare palette designed for rapid triaging:
- **Primary (Teal):** Used for core branding, primary actions, and navigational anchors.
- **Status Blue (Active):** Denotes items currently in process or under review.
- **Status Green (Authorized):** Indicates successful completion or approval.
- **Status Yellow (Pending):** Signals items requiring attention or external feedback.
- **Status Red (Overdue/Denied):** Highlights critical blockers or final rejections.
- **Status Orange (Expiring):** A warning state for time-sensitive authorizations.

The background uses a subtle cool-gray tint to reduce screen glare during extended use, while cards and containers utilize pure white to create clear elevation.

## Typography
The typography system relies exclusively on **Inter** to ensure maximum legibility across dense data tables and complex forms. 

For the oncology monitoring context, "tabular numbers" (`tnum`) must be enabled for all data-heavy displays to ensure numerical values align vertically, facilitating easier comparison of dates and authorization codes. Hierarchy is established through weight shifts (600 for headers, 400 for content) rather than dramatic size changes to maintain high information density.

## Layout & Spacing
The layout follows a **Fixed Grid** philosophy on desktop to ensure data columns remain predictable and readable. 

- **Desktop (1440px+):** 12-column grid with 24px margins and 16px gutters.
- **Tablet (1024px):** 8-column grid with 20px margins.
- **Mobile (600px):** 4-column grid with 16px margins.

The spacing rhythm is built on a 4px baseline. Components like data tables should utilize "Compact" (8px vertical padding) and "Standard" (12px vertical padding) modes to allow users to customize their information density.

## Elevation & Depth
This design system uses a **Tonal Layering** approach combined with **Ambient Shadows** to define hierarchy without cluttering the UI.

- **Level 0 (Background):** #F8FAFC. The lowest layer.
- **Level 1 (Cards/Surface):** Pure white with a 1px border (#E2E8F0).
- **Level 2 (Hover/Active):** A soft, diffused shadow (0px 4px 12px rgba(0, 0, 0, 0.05)) to indicate interactivity.
- **Level 3 (Modals/Popovers):** A more pronounced shadow (0px 12px 32px rgba(0, 0, 0, 0.1)) to focus user attention.

Avoid using shadows for static elements; rely on subtle borders to keep the interface feeling "flat" and professional.

## Shapes
The design system adopts a **Soft** shape language. This provides a modern, approachable feel while maintaining the structural rigor required for a corporate medical tool. 

- **Standard Buttons/Inputs:** 0.25rem (4px).
- **Data Cards/Containers:** 0.5rem (8px).
- **Status Tags/Chips:** 0.25rem (4px) or fully pill-shaped for high-contrast status visibility.
- **Selection Indicators:** 2px stroke width for focus states to meet AA accessibility standards.

## Components

### Buttons & Inputs
Buttons feature a subtle 1px top-inner highlight to provide a professional, tactile feel. Primary buttons use the Teal palette with white text. Input fields must always include a clear 1px border (#E2E8F0) that darkens on hover and turns Primary Teal on focus.

### Status Chips
Status chips are critical for this system. They should use a "Subtle Fill" style: a light tinted background (10% opacity of the semantic color) with high-contrast text (80% opacity of the semantic color). This ensures color-coding is visible without overwhelming the text legibility.

### Data Tables
Tables are the heart of the system. Use sticky headers and a "Zebra Stripe" alternate row coloring (#F1F5F9) for rows exceeding 10 items. Action buttons within rows should be icon-only or ghost-style until hover to reduce visual noise.

### Progress Indicators
For oncology authorizations, use a "Stepper" component for tracking the journey from "Submitted" to "Authorized." Each step uses the semantic colors defined in the palette to indicate at which stage a delay or denial occurred.

### Cards
Summary cards at the top of the dashboard should feature a thick 4px left-border accent using the semantic status colors to provide a quick visual count of "Overdue" vs "Authorized" guides.