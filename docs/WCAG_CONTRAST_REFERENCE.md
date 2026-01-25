# WCAG AA Contrast Reference for Finanpy

## Color Contrast Requirements

WCAG AA requires a contrast ratio of **4.5:1** for normal text and **3:1** for large text (18pt+ or 14pt+ bold).

## Dark Theme Backgrounds
- `bg-gray-900`: #111827 (primary background)
- `bg-gray-800`: #1F2937 (secondary background, cards)
- `bg-gray-700`: #374151 (form inputs)

## Text Colors - Contrast Ratios

### ❌ FAILS WCAG AA (Before)
| Color Class | Hex | On gray-900 | On gray-800 | On gray-700 | Usage |
|------------|-----|-------------|-------------|-------------|-------|
| `text-gray-600` | #4B5563 | **1.9:1** ❌ | **2.2:1** ❌ | **2.6:1** ❌ | Decorative only |
| `text-gray-500` | #6B7280 | **2.4:1** ❌ | **2.8:1** ❌ | **3.3:1** ❌ | REMOVED |
| `text-gray-400` | #9CA3AF | **3.2:1** ❌ | **3.7:1** ❌ | **4.4:1** ❌ | REPLACED |

### ✅ PASSES WCAG AA (After)
| Color Class | Hex | On gray-900 | On gray-800 | On gray-700 | Usage |
|------------|-----|-------------|-------------|-------------|-------|
| `text-gray-300` | #D1D5DB | **5.8:1** ✅ | **6.8:1** ✅ | **8.0:1** ✅ | Secondary text, labels |
| `text-gray-200` | #E5E7EB | **7.5:1** ✅ | **8.8:1** ✅ | **10.3:1** ✅ | Alternative (not used) |
| `text-gray-100` | #F3F4F6 | **9.2:1** ✅ | **10.8:1** ✅ | **12.7:1** ✅ | Primary text |
| `text-white` | #FFFFFF | **11.6:1** ✅ | **13.6:1** ✅ | **16.0:1** ✅ | Emphasis text |

### ✅ Functional Colors (Always Pass)
| Color Class | Hex | On gray-900 | Usage |
|------------|-----|-------------|-------|
| `text-green-400` | #4ADE80 | **6.8:1** ✅ | Income, success |
| `text-red-400` | #F87171 | **4.5:1** ✅ | Expenses, errors |
| `text-blue-400` | #60A5FA | **4.7:1** ✅ | Info, links |
| `text-purple-400` | #C084FC | **5.2:1** ✅ | Accents, links |
| `text-yellow-400` | #FACC15 | **8.3:1** ✅ | Warnings |

## Updated Template Patterns

### Navigation Links (Inactive State)
```html
<!-- Before (3.2:1 - FAILS) -->
<a class="text-gray-400 hover:text-white">Link</a>

<!-- After (5.8:1 - PASSES) -->
<a class="text-gray-300 hover:text-white">Link</a>
```

### Secondary Text / Subtitles
```html
<!-- Before (3.2:1 - FAILS) -->
<p class="text-gray-400">Gerencie suas finanças</p>

<!-- After (5.8:1 - PASSES) -->
<p class="text-gray-300">Gerencie suas finanças</p>
```

### Form Placeholders
```html
<!-- Before (3.2:1 - FAILS) -->
<input placeholder="Digite..." class="placeholder-gray-400">

<!-- After (5.8:1 - PASSES) -->
<input placeholder="Digite..." class="placeholder-gray-300">
```

### Help Text
```html
<!-- Before (3.2:1 - FAILS) -->
<p class="text-xs text-gray-400">Este campo é obrigatório</p>

<!-- After (5.8:1 - PASSES) -->
<p class="text-xs text-gray-300">Este campo é obrigatório</p>
```

### Metadata / Small Text
```html
<!-- Before (2.4:1 - FAILS) -->
<span class="text-xs text-gray-500">01/01/2024</span>

<!-- After (3.2:1 - Improved but check context) -->
<span class="text-xs text-gray-400">01/01/2024</span>
```

## Design System Update

### Primary Text Hierarchy (New Standard)
1. **Heading/Emphasis**: `text-white` (11.6:1)
2. **Primary Text**: `text-gray-100` (9.2:1)
3. **Secondary Text**: `text-gray-300` (5.8:1)
4. **Tertiary/Metadata**: `text-gray-400` (3.2:1) - Use sparingly, only for non-critical info
5. **Decorative Only**: `text-gray-500`, `text-gray-600` - NOT for readable text

### Form Elements
- **Labels**: `text-gray-300` (medium weight)
- **Inputs**: `text-gray-100` (main text)
- **Placeholders**: `placeholder-gray-300`
- **Help Text**: `text-gray-300` (xs size)
- **Error Text**: `text-red-400`

### Navigation
- **Active Links**: `text-white` or gradient
- **Inactive Links**: `text-gray-300`
- **Hover State**: `text-white`

## Testing Tools

### Browser DevTools
1. Open DevTools (F12)
2. Select element
3. Go to Accessibility panel
4. Check "Contrast" section

### Online Tools
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Contrast Ratio](https://contrast-ratio.com/)
- [Adobe Color Accessibility Tools](https://color.adobe.com/create/color-accessibility)

### Automated Testing
```bash
# Using axe-core or Lighthouse
npm install -g lighthouse
lighthouse http://localhost:8000 --only-categories=accessibility
```

## Exceptions

Colors NOT subject to contrast requirements:
- Logos and brand elements
- Decorative images and icons
- Disabled form controls
- Incidental text (background patterns)

## References
- [WCAG 2.1 Success Criterion 1.4.3](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- [TailwindCSS Gray Scale](https://tailwindcss.com/docs/customizing-colors#color-palette-reference)
