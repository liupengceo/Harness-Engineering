# Header & Footer 快速修复操作手册

> 这份文档是给你**直接在 WordPress 后台操作用的**，每一步都是"去哪里 → 改什么 → 粘贴什么"。
> 预计总操作时间：30–45 分钟。

---

## 一、HEADER 修复（3 步）

---

### 第 1 步：修复顶部栏 — 把无用文字换成联系方式

**去哪里：** `外观 → 自定义 → Header → Top Row → 左侧区域 → HTML`

**删除当前内容：**
```
<a href="https://90817.com/"><strong>Steel Telecom Tower Manufacturer</strong></a>
```

**替换为（直接复制粘贴）：**
```html
<span style="font-size:13px; color:#4A5568;">
  ✉️ <a href="mailto:sales@90817.com" style="color:#2B6CB0; text-decoration:none; font-weight:600;">sales@90817.com</a>
  &nbsp;&nbsp;|&nbsp;&nbsp;
  📞 <a href="tel:+863184431156" style="color:#2B6CB0; text-decoration:none; font-weight:600;">+86-318-4431156</a>
  &nbsp;&nbsp;|&nbsp;&nbsp;
  💬 <a href="https://wa.me/8613800000000" style="color:#25D366; text-decoration:none; font-weight:600;">WhatsApp</a>
</span>
```

> ⚠️ 把 `8613800000000` 换成你真实的 WhatsApp 号码

**右侧社交图标修复：** `Header → Top Row → 右侧区域 → Social`

- Facebook → 填入你的 Facebook 主页 URL（如果没有就**删除这个图标**）
- X (Twitter) → **删除**（B2B 用不上）
- Instagram → **删除**（B2B 用不上）
- **新增 LinkedIn** → 填入公司 LinkedIn URL
- **新增 YouTube** → 填入频道 URL（如果有工厂视频）

> 🔴 关键：没有真实 URL 的社交图标必须删除，空链接对 SEO 有害！

---

### 第 2 步：精简导航菜单 — 11 个变 5+下拉

**去哪里：** `外观 → 菜单`

**操作：**
1. 点击"创建新菜单"，命名为 `主导航-新`
2. 按以下结构添加菜单项：

```
Home                        （页面）
Products                    （自定义链接，URL 填 #）
  ├── Transmission Towers   （分类 — 拖进去变子菜单）
  ├── Monopole Towers       （分类）
  ├── Lattice Towers        （分类）
  ├── Guyed Towers          （分类）
  ├── 5G Cell Towers        （分类）
  └── Communication Towers  （分类）
Solutions                   （自定义链接，URL 填 #）
  ├── Tower Design and Specs    （页面）
  ├── Tower Cost and Pricing    （页面）
  └── Cell Tower Solutions      （页面）
About Us                    （页面）
Contact Us                  （页面）
```

3. 在底部"菜单设置"中，勾选 **Primary** 位置
4. 保存菜单

> 效果：导航从 3 行折行变成 1 行整齐排列，Products 和 Solutions 鼠标悬停显示下拉

---

### 第 3 步：导航栏右侧加"Get a Quote"按钮

**去哪里：** `外观 → 自定义 → Header → Main Row`

**操作：**
1. 在 Main Row 的**右侧区域**，点击 `+` 添加新元素
2. 选择 **"Button"**（按钮）
3. 设置：
   - 文字：`Get a Quote`
   - 链接：`/contact-us/`
   - 背景色：`#3182CE`
   - 文字颜色：`#FFFFFF`
   - 圆角：`4px`
   - 上下内边距：`10px`，左右内边距：`24px`
4. 发布

---

## 二、FOOTER 修复（4 步）

---

### 第 4 步：删除重复的公司描述

**去哪里：** `外观 → 小工具 → Footer 1`（或 `外观 → 自定义 → Footer → Middle Row → Column 1`）

**你会看到两段几乎一样的公司介绍：**
- block-85（带 Logo 的那段）← ✅ **保留这个**
- block-81（没有 Logo，只有文字）← ❌ **删除这个**

**同时在保留的 block-85 下面，邮件订阅表单上方，加一行说明文字：**

在 Kadence Form 上面添加一个段落 Block：

```
Stay updated — get project case studies and industry news.
```

字体大小设为 `13px`，颜色设为浅灰色。

---

### 第 5 步：填充空的 Categories 菜单

**去哪里：** `外观 → 菜单`

**操作：**
1. 创建新菜单，命名为 `Footer-Products`
2. 添加以下分类：
   - Transmission Towers
   - Monopole Towers
   - Lattice Towers
   - Guyed Towers
   - 5G Cell Towers
   - Communication Towers
3. 保存

**然后去：** `外观 → 小工具 → Footer 2`
- 删除原来空的导航菜单小工具
- 添加新的"导航菜单"小工具
- 标题填：`Products`
- 选择菜单：`Footer-Products`
- 保存

---

### 第 6 步：填充空的 Company Info 菜单

**去哪里：** `外观 → 菜单`

**操作：**
1. 创建新菜单，命名为 `Footer-Company`
2. 添加以下页面：
   - About Us
   - Tower Design and Specs
   - Tower Cost and Pricing
   - Cell Tower Solutions
   - Contact Us
3. 保存

**然后去：** `外观 → 小工具 → Footer 4`（Company Info 那一列）
- 删除原来空的导航菜单小工具
- 添加新的"导航菜单"小工具
- 标题填：`Company`
- 选择菜单：`Footer-Company`
- 保存

---

### 第 7 步：Contact Us 列加 WhatsApp 按钮

**去哪里：** `外观 → 小工具 → Footer 6`（或通过 Customizer → Footer → Column 5）

**在现有的联系信息下面，添加一个"自定义 HTML"小工具，粘贴：**

```html
<div style="margin-top:20px;">
  <a href="https://wa.me/8613800000000" target="_blank" rel="noopener"
     style="display:inline-block; padding:12px 24px; background:#25D366; color:#fff; border-radius:4px; font-size:14px; font-weight:600; text-decoration:none; text-align:center;">
    💬 WhatsApp Us
  </a>
</div>
```

> ⚠️ 把 `8613800000000` 换成你真实的 WhatsApp 号码

---

## 三、底部版权栏修复

**去哪里：** `外观 → 自定义 → Footer → Bottom Row`

**左侧 HTML 替换为：**
```html
<p style="font-size:13px; margin:0;">© 2026 HB Power Tower Co., Ltd. All rights reserved.</p>
```

**右侧社交图标：** 和顶部一样，删除所有空 URL 的图标，只保留有真实链接的。

---

## 操作后效果对比

### HEADER 修复前：
```
[Steel Telecom Tower Manufacturer]               [FB空] [X空] [IG空]
[LOGO]  Home Transmission Monopole Lattice Guyed 5G Comm Design Cost Cell About Contact
         （11个一字排开，折行3行，拥挤混乱）
```

### HEADER 修复后：
```
✉️ sales@90817.com | 📞 +86-318-4431156 | 💬 WhatsApp     [LinkedIn] [YouTube]
[LOGO]      Home | Products▼ | Solutions▼ | About | Contact     [Get a Quote]
             （5个主菜单 + 下拉，整洁专业）
```

### FOOTER 修复前（你截图的样子）：
```
[Logo]              CATEGORIES    CERTIFICATIONS     COMPANY INFO     Contact Us
HB Power Tower...   （空的！）     ISO 9001...        （空的！）        Email
HB Power Tower...                  ISO 14001...                        Tel
（重复！）                          ISO 45001...                        Address
[邮件表单-无说明]                   Production Lic
                                   Safety Lic
```

### FOOTER 修复后：
```
[Logo]              Products        Company           Contact Us
HB Power Tower...   • Transmission  • About Us        📧 sales@90817.com
（只出现一次）       • Monopole      • Tower Design    📞 +86-318-4431156
                    • Lattice       • Cost & Pricing  📞 +86-318-4431166
Stay updated...     • Guyed         • Cell Solutions  📍 Guangchuan, Hengshui
[___@___] [提交]    • 5G Cell       • Contact Us      [💬 WhatsApp Us]
                    • Communication
```

---

## 注意事项

1. **所有操作完成后点"发布"**（Customizer 右上角蓝色按钮）
2. **清除缓存**：如果你用了 Cloudflare 或缓存插件，操作后记得清缓存
3. **手机检查**：修改后用手机打开网站确认移动端显示正常
4. **Certifications 那一列**：可以保留也可以删除。如果保留，建议改标题为 `Quality` 或 `Standards`，内容更简洁
