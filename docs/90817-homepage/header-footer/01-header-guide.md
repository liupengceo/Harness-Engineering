# Header Optimization Guide — 90817.com

## Current Problems

| Issue | Impact |
|-------|--------|
| Social links (Facebook/X/Instagram) have empty `href=""` | Broken links, bad UX, Google warnings |
| 11 menu items in one row — too many | Overflows on desktop, confusing navigation |
| No CTA button in header | Misses conversion opportunity |
| Top bar text "Steel Telecom Tower Manufacturer" links to homepage | Redundant, wastes space |
| No phone/email in header | B2B buyers want instant contact |

---

## Optimized Header Structure

### Top Bar (Utility Bar)

```
┌─────────────────────────────────────────────────────────────────────┐
│  📧 sales@90817.com  |  📞 +86-318-4431156  |  [FB] [LinkedIn] [YT]│
└─────────────────────────────────────────────────────────────────────┘
```

**Settings in Kadence Customizer:**
- Go to: Appearance → Customize → Header → Top Row
- **Left side:** Header HTML widget with:

```html
<span style="font-size:14px;">
  📧 <a href="mailto:sales@90817.com" style="color:#2D3748;">sales@90817.com</a>
  &nbsp;&nbsp;|&nbsp;&nbsp;
  📞 <a href="tel:+863184431156" style="color:#2D3748;">+86-318-4431156</a>
</span>
```

- **Right side:** Social Icons
  - Remove: Twitter/X, Instagram (unless you actually use them)
  - Keep/Add: Facebook, LinkedIn, YouTube, WhatsApp
  - **Fill in real URLs!** (currently all empty)

### Main Header Row

```
┌─────────────────────────────────────────────────────────────────────┐
│  [LOGO]     Home | Products ▼ | Solutions ▼ | About | Contact  [GET QUOTE] │
└─────────────────────────────────────────────────────────────────────┘
```

**Navigation restructure (reduce from 11 to 6 items + CTA):**

| Menu Item | Type | Dropdown Children |
|-----------|------|-------------------|
| Home | Page link | — |
| Products | Custom link (#) | Transmission Towers, Monopole Towers, Lattice Towers, Guyed Towers, 5G Cell Towers, Communication Towers |
| Solutions | Custom link (#) | Tower Design & Specs, Tower Cost & Pricing, Cell Tower Solutions |
| About Us | Page link | — |
| Contact Us | Page link | — |
| **Get a Quote** | Button (CTA) | — |

---

## Step-by-Step Implementation

### Step 1: Fix Social Links

1. Go to **Appearance → Customize → Header → Top Row → Social**
2. Remove any social platform you don't actually use
3. For each remaining platform, enter the REAL URL:
   - Facebook: `https://facebook.com/YOUR-PAGE`
   - LinkedIn: `https://linkedin.com/company/YOUR-COMPANY`
   - YouTube: `https://youtube.com/@YOUR-CHANNEL`
4. **Recommended:** Replace Instagram/Twitter with LinkedIn (more relevant for B2B)
5. Add WhatsApp: `https://wa.me/86XXXXXXXXXXX`

### Step 2: Reorganize Navigation

1. Go to **Appearance → Menus**
2. Create a new menu called "Primary Navigation 2025"
3. Structure as follows:

```
├── Home (page)
├── Products (custom link: #)
│   ├── Transmission Towers (category)
│   ├── Monopole Towers (category)
│   ├── Lattice Towers (category)
│   ├── Guyed Towers (category)
│   ├── 5G Cell Towers (category)
│   └── Communication Towers (category)
├── Solutions (custom link: #)
│   ├── Tower Design and Specs (page)
│   ├── Tower Cost and Pricing (page)
│   └── Cell Tower Solutions (page)
├── About Us (page)
└── Contact Us (page)
```

4. Assign to "Primary" menu location
5. Save

### Step 3: Add CTA Button to Header

1. Go to **Appearance → Customize → Header → Main Row**
2. In the **Right section**, add "Button" element (drag it after Navigation)
3. Configure:
   - **Text:** `Get a Quote`
   - **Link:** `/contact-us/`
   - **Style:** Filled
   - **Background:** `#3182CE` (matches brand blue)
   - **Text color:** `#FFFFFF`
   - **Border radius:** `4px`
   - **Padding:** `10px 24px`

### Step 4: Update Top Bar Content

1. Go to **Appearance → Customize → Header → Top Row → HTML**
2. Replace current content with the HTML snippet above (email + phone)
3. Set background: `#F7FAFC` (light gray) or keep white
4. Border bottom: `1px solid #eeeeee`

### Step 5: Mobile Header

1. Go to **Appearance → Customize → Header → Mobile Header**
2. Ensure logo + hamburger menu are showing
3. The mobile drawer menu will automatically use your new menu structure
4. Consider adding a phone icon button in mobile header for quick calling

---

## Before vs After

### Before:
```
[Steel Telecom Tower Manufacturer]                    [FB-empty] [X-empty] [IG-empty]
[LOGO]  Home|Trans|Mono|Lattice|Guyed|5G|Comm|Design|Cost|Cell|About|Contact
```

### After:
```
📧 sales@90817.com | 📞 +86-318-4431156              [FB] [LinkedIn] [YT] [WhatsApp]
[LOGO]       Home | Products ▼ | Solutions ▼ | About | Contact     [GET A QUOTE]
```

---

## Dropdown Styling (already configured in Kadence)

Your current dropdown settings are fine:
- Width: 180px
- Background: light
- Hover: blue background + white text
- Border bottom on items

No changes needed for dropdown appearance.
