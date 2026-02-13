# Style Standards

Adopt the **10mm GMS Design System** for all UI components. This system is technically defined by the `shadcn/ui` library architecture and our shared Design Tokens.

**Do not** attempt to mimic Material Design or other external systems if they conflict with the native aesthetic of our component library.

## Cross-Platform Styling
*   **Web**: Use **Tailwind CSS** configured with the `10mm-preset`.
*   **Mobile (Android/iOS)**: Use **NativeWind** to apply the same Tailwind tokens to React Native components.

## Interactivity
- **Pointer Cursor**: All clickable elements (buttons, links, interactable cards) **must** show a `pointer` cursor on hover.
- **Feedback**: Interactive elements must provide immediate visual feedback (hover state, active/pressed state, focus ring).
- **Animations**: Use the standard shadcn/Tailwind transitions (`transition-all duration-200`). Avoid custom keyframe animations unless critical for UX.

## Functional Priority
Semantic meaning takes precedence over branding. For example:
- **Green**: Success, completion, active status.
- **Red**: Errors, critical warnings.
- **Yellow/Orange**: Non-critical warnings, pending status.

If branding colors conflict with these universal semantic meanings (e.g., brand red for a success state), the semantic color must be used to ensure user clarity.

## Semantic Color System

We use a semantic color mapping that connects our Brand Identity to Functional Roles.

### 1. Brand Identity (The "Primitive" Colors)
*   **10mm GMS Red**: `#9e2326` (Secondary Brand Color / Destructive Actions)
*   **10mm GMS green**: `#166534` (Primary Brand Color / Success & Actions)
*   **10mm GMS Blue**: `#c6e6f6` (Accent / Background Accent)
*   **Rich Black**: `#151616` (Text/Neutral)
*   **White**: `#ffffff` (Surface)

### 2. Functional Roles (The "Tokens")
Do not use hex codes in code. Use these semantic names (Tailwind classes):

| Role | Tailwind Class | Value | Usage |
| :--- | :--- | :--- | :--- |
| **Primary** | `bg-primary` | **10mm GMS Green** | Main actions (Submit, Save), active states. |
| **Primary Fg** | `text-primary-foreground` | **White** | Text on top of primary buttons. |
| **Secondary** | `bg-secondary` | **10mm GMS Blue** | Low priority buttons, badges. |
| **Destructive** | `bg-destructive` | **10mm GMS Red** | Delete, Remove, Dangerous actions. |
| **Background** | `bg-background` | **White** | Page background. |
| **Surface** | `bg-card` | **White** + Shadow | Cards, Modals. |
| **Text** | `text-foreground` | **Rich Black** | Body text. |
| **Muted** | `text-muted-foreground` | **Gray-500** | Hints, labels, disabled text. |

### Typography
*   **Headings**: Poppins (Sans-serif, Geometric) -> `font-heading`
*   **Body**: Fira Sans (Sans-serif, Humanist) -> `font-body` or default sans.

### Typography

Document Font - Fira Sans
Logo Font - Poppins
Text in documents should be  Black #151616ff (0,0,0,1)

### Logos
For light themes use logo_colour.svg
For dark themes use logo_colour_reverse.svg

#### Asset Portability
*   **Font Independence**: All SVG assets (including logos) MUST have their text converted to paths/outlines. This ensures consistent rendering across different Operating Systems and environments where the target font might not be installed.
*   **Vector Fidelity**: Prefer SVG over Raster (PNG/JPG) for UI elements to maintain clarity at all zoom levels.

## External Branding

### Google Sign-In
To comply with Google Identity branding guidelines:
- **Button Text**: Use "Sign in with Google", "Sign up with Google", or "Continue with Google".
- **Typography**: Must use **Roboto Medium**.
- **Colors**: The Google "G" logo must be in its standard multi-color format.
- **Background**: The "G" logo must always appear on a white background (either as part of the logo asset or as a white container).
- **No Variations**: Do not use monochrome logos or custom brand colors for the Google icon.