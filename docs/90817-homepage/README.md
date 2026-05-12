# 90817.com Homepage - Optimized Block Code

## How to Use

### Method 1: Full Page Code (Recommended)
1. Go to WordPress Admin → Pages → Edit "Home" page
2. Click the **three dots menu (⋮)** in the top right corner
3. Select **"Code editor"**
4. **Select all** existing content and **delete** it
5. Copy the entire content from `homepage-blocks.html`
6. **Paste** it into the code editor
7. Click **"Exit code editor"** to return to visual mode
8. Click **"Update"** to save

### Method 2: Section by Section
If you prefer to add sections one at a time, use the individual files in the `sections/` folder.

## Files

| File | Description |
|------|-------------|
| `homepage-blocks.html` | Complete homepage (all sections combined) |
| `sections/01-hero-banner.html` | Hero section with CTA buttons |
| `sections/02-stats-bar.html` | Key statistics counter bar |
| `sections/03-product-categories.html` | 6 product category grid |
| `sections/04-why-choose-us.html` | 4 advantages section |
| `sections/05-project-cases.html` | Project case studies |
| `sections/06-certifications.html` | Certification logos display |
| `sections/07-cta-section.html` | Final call-to-action |

## Image Placeholders

The code uses placeholder image URLs. You need to replace them with your actual images:

| Placeholder | Recommended Size | Description |
|---|---|---|
| `YOUR-HERO-IMAGE-URL` | 1920×800px | Main hero banner background |
| `YOUR-TRANSMISSION-TOWER-IMAGE` | 600×400px | Transmission tower product photo |
| `YOUR-MONOPOLE-TOWER-IMAGE` | 600×400px | Monopole tower product photo |
| `YOUR-LATTICE-TOWER-IMAGE` | 600×400px | Lattice tower product photo |
| `YOUR-GUYED-TOWER-IMAGE` | 600×400px | Guyed tower product photo |
| `YOUR-5G-TOWER-IMAGE` | 600×400px | 5G cell tower product photo |
| `YOUR-COMMUNICATION-TOWER-IMAGE` | 600×400px | Communication tower product photo |
| `YOUR-PROJECT-X-IMAGE` | 800×500px | Project case study photos |

## SEO Notes

- Page Title should be set to: `Transmission Tower Manufacturer | Monopole & Lattice Towers | HB Power Tower`
- Meta Description: `HB Power Tower — China's leading manufacturer of 10-500kV transmission towers, monopole towers & lattice towers. 80,000+ tons/year capacity. Free quote within 24h.`
- Make sure to install Rank Math SEO plugin and configure these in the SEO settings panel below the editor.

## Kadence Theme Settings to Change

1. **Remove Hero Title**: Go to Appearance → Customize → Pages → Page Layout → Title → Set to "Disabled"
2. **Set Page to Full Width**: In the page editor, look for the Kadence Page Settings panel and set Layout to "Full Width" with no sidebar
