# Footer Optimization Guide — 90817.com

## Current Problems

| Issue | Impact |
|-------|--------|
| Company description appears TWICE (block-85 and block-81) | Looks like a bug, wastes space |
| "Categories" menu widget is EMPTY (only title, no links) | Useless section |
| "Company Info" menu widget is EMPTY (only title, no links) | Useless section |
| Social links in bottom footer all have empty `href=""` | Broken links |
| Email subscription form has no context/label | Users don't know why to subscribe |
| 5-column layout is unbalanced | Some columns have tons of content, others are empty |
| Footer bottom bar copyright only, no useful links | Missed opportunity for legal pages |

---

## Optimized Footer Structure

### Middle Footer (5 Columns → 4 Columns)

```
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  [LOGO]                    Products         Company          Contact Us    │
│  HB Power Tower Co., Ltd.  • Transmission   • About Us       📧 sales@... │
│  Professional manufacturer  • Monopole      • Certifications 📞 +86-318.. │
│  of transmission towers...  • Lattice       • Project Cases  📍 Guangchuan│
│                             • Guyed         • Tower Design      Hengshui  │
│  [Email Subscription]       • 5G Cell       • Cost & Pricing    Hebei,CN  │
│  Stay updated on our        • Communication • Blog/News                   │
│  latest projects                                             [WhatsApp]   │
│  [________@____] [→]                                                      │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│  © 2026 HB Power Tower Co., Ltd.    Privacy | Terms    [FB][LI][YT][WA]  │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Implementation

### Step 1: Change to 4-Column Layout

1. Go to **Appearance → Customize → Footer → Middle Row**
2. Change **Columns** from `5` to `4`
3. Set **Column Layout** to: `40% | 20% | 20% | 20%` (or "First Wide")
4. **Row Layout:** Full Width
5. **Background:** Keep `var(--global-palette4)` (dark: `#2D3748`)
6. **Padding:** Top `70px`, Bottom `70px`
7. **Column Gap:** `60px`

### Step 2: Column 1 — Brand + Newsletter

Go to **Appearance → Widgets → Footer Column 1**

**Remove:** The duplicate block (block-81). Keep only ONE company description.

**Keep/Edit block-85 to contain:**

```html
<!-- Company Logo -->
<figure class="wp-block-image size-full">
  <img src="https://90817.com/wp-content/uploads/2024/11/cropped-1730956562324-5-e1753844706175.png" alt="HB Power Tower" width="160" height="36" />
</figure>

<!-- Company Description (ONE copy only) -->
<p style="color:var(--wp--preset--color--theme-palette-8);font-size:15px;line-height:1.7;margin-bottom:24px;">
Professional manufacturer of transmission towers, monopole towers, and substation structures. Annual capacity: 80,000+ tons. Serving 15+ countries since 1994.
</p>

<!-- Newsletter Signup with Context -->
<h5 style="color:#fff;font-size:15px;margin-bottom:8px;">Stay Updated</h5>
<p style="color:var(--wp--preset--color--theme-palette-8);font-size:13px;margin-bottom:12px;">
Get project case studies and industry insights delivered to your inbox.
</p>
```

Then keep the existing Kadence email form below it.

### Step 3: Column 2 — Products (Fix Empty "Categories" Menu)

Go to **Appearance → Widgets → Footer Column 2**

**Remove:** The empty nav_menu-22 widget.

**Replace with a Navigation Menu widget:**

1. Add widget: **Navigation Menu**
2. Title: `Products`
3. Select menu: Create a new menu called "Footer Products" with these items:
   - Transmission Towers → `/category/transmission-tower-product/`
   - Monopole Towers → `/category/monopole-tower-product/`
   - Lattice Towers → `/category/lattice-tower/`
   - Guyed Towers → `/category/guyed-tower/`
   - 5G Cell Towers → `/category/5g-cell-tower/`
   - Communication Towers → `/category/communication-tower/`

### Step 4: Column 3 — Company (Fix Empty "Company Info" Menu)

Go to **Appearance → Widgets → Footer Column 3**

**Remove:** The empty nav_menu-23 widget.

**Replace with a Navigation Menu widget:**

1. Add widget: **Navigation Menu**
2. Title: `Company`
3. Select menu: Create a new menu called "Footer Company" with:
   - About Us → `/about-us/`
   - Tower Design & Specs → `/monopole-tower-design/`
   - Tower Cost & Pricing → `/monopole-tower-cost-price/`
   - Cell Tower Solutions → `/monopole-cell-tower/`
   - Contact Us → `/contact-us/`

### Step 5: Column 4 — Contact Info (Move from Column 5)

Go to **Appearance → Widgets → Footer Column 4**

**Remove** the old widget. Replace with a Custom HTML widget:

```html
<h5 style="color:#fff;font-size:16px;margin-bottom:16px;">Contact Us</h5>

<div style="color:#CBD5E0;font-size:15px;line-height:2.2;">
  <p>📧 <a href="mailto:sales@90817.com" style="color:#fff;">sales@90817.com</a></p>
  <p>📞 <a href="tel:+863184431156" style="color:#fff;">+86-318-4431156</a></p>
  <p>📞 <a href="tel:+863184431166" style="color:#fff;">+86-318-4431166</a></p>
  <p>📍 No.86 Guangchuan Dev Zone<br>&nbsp;&nbsp;&nbsp;&nbsp;Hengshui, Hebei, China</p>
</div>

<div style="margin-top:20px;">
  <a href="https://wa.me/86XXXXXXXXXXX" 
     style="display:inline-block;padding:10px 20px;background:#25D366;color:#fff;border-radius:4px;font-size:14px;font-weight:600;text-decoration:none;">
    💬 WhatsApp Us
  </a>
</div>
```

### Step 6: Remove Column 5 (Certifications)

Since we're going from 5 → 4 columns, the **Certifications** column (text-3 widget) should be **removed from the footer** — certification info is already well-displayed on the About Us page and homepage.

If you want to keep a brief mention, add this one line to the bottom of Column 1:

```html
<p style="color:#718096;font-size:12px;margin-top:16px;">ISO 9001 | ISO 14001 | ISO 45001 Certified</p>
```

### Step 7: Fix Bottom Footer Bar

Go to **Appearance → Customize → Footer → Bottom Row**

**Left side (HTML):**

```html
<p style="font-size:14px;">© 2026 HB Power Tower Co., Ltd. All rights reserved.</p>
```

**Right side (Social Icons):**

1. Go to Footer → Bottom Row → Social
2. **Remove all platforms with empty URLs**
3. Add only platforms with REAL URLs:
   - Facebook: `https://facebook.com/YOUR-PAGE`
   - LinkedIn: `https://linkedin.com/company/YOUR-COMPANY`
   - YouTube: `https://youtube.com/@YOUR-CHANNEL`
   - Email: `mailto:sales@90817.com`
   - Phone: `tel:+863184431156`
4. Style: Filled, Color: White on transparent

**Optional — Add legal links to left side:**

```html
<p style="font-size:14px;">
  © 2026 HB Power Tower Co., Ltd. &nbsp;|&nbsp; 
  <a href="/privacy-policy/" style="color:#A0AEC0;">Privacy Policy</a> &nbsp;|&nbsp; 
  <a href="/terms/" style="color:#A0AEC0;">Terms</a>
</p>
```

---

## Before vs After Comparison

### BEFORE (Current):
```
Col 1 (broken):           Col 2:        Col 3:          Col 4:           Col 5:
[Logo]                    Categories    Certifications  Company Info     Contact Us
Company desc #1           (EMPTY!)      ISO 9001...     (EMPTY!)         Email
Company desc #2 (dupe!)                 ISO 14001...                     Tel
[Email form - no label]                 ISO 45001...                     Address
                                        Production Lic
                                        Safety Lic
─────────────────────────────────────────────────────────────────────────────────
© 2026 HB Power Tower                                  [FB-∅][X-∅][IG-∅][📧][📞][YT-∅]
```

### AFTER (Optimized):
```
Col 1 (40%):              Col 2 (20%):      Col 3 (20%):       Col 4 (20%):
[Logo]                    Products           Company            Contact Us
Company description       • Transmission     • About Us         📧 sales@90817.com
(single, clean)           • Monopole         • Tower Design     📞 +86-318-4431156
                          • Lattice          • Cost & Pricing   📞 +86-318-4431166
Stay Updated              • Guyed            • Cell Solutions   📍 Guangchuan, Hengshui
Get project case...       • 5G Cell          • Contact Us          Hebei, China
[_____@_____] [→]         • Communication                      [💬 WhatsApp Us]

ISO 9001 | 14001 | 45001
─────────────────────────────────────────────────────────────────────────────────
© 2026 HB Power Tower Co., Ltd. | Privacy | Terms            [FB] [LinkedIn] [YT]
```

---

## Summary of Changes

| What | Action |
|------|--------|
| Duplicate company description | DELETE block-81, keep block-85 |
| Empty Categories menu | REPLACE with real product links |
| Empty Company Info menu | REPLACE with real page links |
| Certifications column | REMOVE (move 1-liner to col 1) |
| Column count | REDUCE from 5 to 4 |
| Email subscription | ADD context label above form |
| Social links | FIX: add real URLs, remove unused |
| Bottom bar | ADD legal links, fix social |
| Contact column | ADD WhatsApp button |
| Column proportions | SET to 40/20/20/20 |
