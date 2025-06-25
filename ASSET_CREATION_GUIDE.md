# Missing Assets Creation Guide

## 🎯 Required Assets to Create

### 1. favicon.ico
**Location:** `/favicon.ico` (root directory)
**Purpose:** Browser tab icon
**Specifications:**
- **Dimensions:** 32x32 pixels (minimum), 16x16, 32x32, 48x48 (multi-size ICO)
- **Format:** ICO file format
- **Source:** Use your profile-image.png
- **Tools:** 
  - Online: favicon.io, realfavicongenerator.net
  - Software: GIMP, Photoshop
- **Process:**
  1. Resize profile image to 32x32 pixels
  2. Convert to ICO format
  3. Save as `favicon.ico` in root directory

### 2. og-image.jpg  
**Location:** `/assets/og-image.jpg`
**Purpose:** Social media preview image (Facebook, Twitter, LinkedIn)
**Specifications:**
- **Dimensions:** 1200x630 pixels (Facebook recommended)
- **Format:** JPEG, high quality (90-95%)
- **Size:** Under 1MB
- **Content Suggestions:**
  - Your name and title
  - Brief description: "Experimental Physicist & AI Researcher"
  - Professional background or your profile image
  - Clean, readable typography
- **Tools:**
  - Online: Canva, Pablo by Buffer, Adobe Express
  - Software: Photoshop, GIMP, Figma
- **Text to Include:**
  - "Manas Pandey"
  - "Experimental Physicist & AI Researcher"
  - "IIT Kanpur"
  - Optional: Portfolio website URL

### 3. assets/ Directory Structure
**Current:** `/assets/` exists but needs og-image.jpg
**Required:** 
```
/assets/
  ├── og-image.jpg (1200x630px, <1MB)
  └── images/ (already exists)
```

## 📝 Implementation Steps

1. **Create favicon.ico:**
   ```bash
   # After creating the file
   # Place in: /favicon.ico
   ```

2. **Create og-image.jpg:**
   ```bash
   # After creating the file  
   # Place in: /assets/og-image.jpg
   ```

3. **Verify References:**
   - All HTML files reference `/favicon.ico`
   - All HTML files reference `/assets/og-image.jpg` in Open Graph meta tags
   - No code changes needed after creating files

## ✅ Validation

After creating the assets:
- **Favicon:** Should appear in browser tabs
- **OG Image:** Test with Facebook Debugger or Twitter Card Validator
- **File sizes:** favicon.ico <50KB, og-image.jpg <1MB

## 🔗 Useful Tools

- **Favicon:** https://favicon.io/favicon-converter/
- **OG Image:** https://www.canva.com/create/og-images/
- **Testing:** https://developers.facebook.com/tools/debug/