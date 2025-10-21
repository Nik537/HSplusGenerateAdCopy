# Visual Guide - Marketing Copy Generator

## 🖥️ User Interface Layout

```
┌────────────────────────────────────────────────────────────────┐
│ ⚡ Marketing Copy Generator              ✅ API Connected      │
└────────────────────────────────────────────────────────────────┘
┌──────────────────────┬─────────────────────────────────────────┐
│                      │                                         │
│   INPUT FORM         │   GENERATED COPY PREVIEW                │
│                      │                                         │
│ ┌──────────────────┐ │ ┌─────────────────────────────────────┐ │
│ │ Product URL      │ │ │ VARIANT 1 - PAIN POINT              │ │
│ │ [vigoshop.si/..] │ │ │ Engagement Score: 82/100            │ │
│ └──────────────────┘ │ │                                     │ │
│                      │ │ ┌─────────────────────────────────┐ │ │
│ ┌──────────────────┐ │ │ │ HS Plus  Sponsored              │ │ │
│ │ Product Name     │ │ │ │                                 │ │ │
│ │ [Auto-filled]    │ │ │ │ Tired of waiting?               │ │ │
│ └──────────────────┘ │ │ │                                 │ │ │
│                      │ │ │ Get your Product delivered...   │ │ │
│ ┌──────────────────┐ │ │ │                                 │ │ │
│ │ Price: 19,99€    │ │ │ │ Shop Now - Fast EU Delivery!   │ │ │
│ └──────────────────┘ │ │ └─────────────────────────────────┘ │ │
│                      │ │ 📋 Copy    Characters: 145          │ │
│ ┌──────────────────┐ │ └─────────────────────────────────────┘ │
│ │ Features         │ │                                         │
│ │ [Feature 1 |     │ │ ┌─────────────────────────────────────┐ │
│ │  Feature 2 |     │ │ │ VARIANT 2 - BENEFIT                 │ │
│ │  Feature 3]      │ │ │ Engagement Score: 85/100            │ │
│ └──────────────────┘ │ │ ... (Facebook preview)              │ │
│                      │ └─────────────────────────────────────┘ │
│ Market: [SI ▼]      │                                         │
│ Objective: [Conv▼]  │ ┌─────────────────────────────────────┐ │
│                      │ │ VARIANT 3 - SOCIAL PROOF            │ │
│ ┌──────────────────┐ │ │ Engagement Score: 88/100            │ │
│ │ ✨ Generate Copy │ │ │ ... (Facebook preview)              │ │
│ └──────────────────┘ │ └─────────────────────────────────────┘ │
│                      │                                         │
│ Or try an example:   │ ⬇️ Download TXT                        │
│ [Beauty] [Elec] [Auto]│                                        │
│                      │                                         │
└──────────────────────┴─────────────────────────────────────────┘
```

---

## 🎨 Color Scheme

```
Primary Blue:   #1877f2  (Facebook blue, CTAs)
Success Green:  #10b981  (Success messages, high scores)
Warning Orange: #f59e0b  (Medium scores)
Error Red:      #ef4444  (Errors, low scores)
Gray Background:#f5f5f5  (Page background)
Dark Text:      #1a1a1a  (Main text)
Light Gray:     #e5e7eb  (Borders, dividers)
```

---

## 📋 User Flow Diagram

### Flow 1: Quick Start (Example Product)

```
┌─────────────┐
│   Landing   │
│    Page     │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ Click       │
│"Beauty      │
│ Product"    │
└─────┬───────┘
      │
      ▼ (Auto-fills form)
┌─────────────┐
│ Product:    │
│ SMILY       │
│ Price: 19€  │
│ Market: SI  │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ Click       │
│"Generate    │
│  Copy"      │
└─────┬───────┘
      │
      ▼ (5-8 seconds)
┌─────────────┐
│ 3 Variants  │
│ Appear with │
│ Scores      │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ Click "Copy"│
│ on Variant 3│
│ (score: 88) │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ Paste into  │
│ Facebook    │
│ Ads Manager │
└─────────────┘

Total Time: 30 seconds
```

### Flow 2: Custom Product (URL Scraping)

```
┌─────────────┐
│   Landing   │
│    Page     │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ Paste       │
│ vigoshop.si │
│    URL      │
└─────┬───────┘
      │
      ▼ (Auto-scrape)
┌─────────────┐
│ Wait 2-3s   │
│ Scraping... │
└─────┬───────┘
      │
      ▼ (Auto-fills)
┌─────────────┐
│ Form filled │
│ with        │
│ product data│
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ Adjust      │
│ market/     │
│ objective   │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ Generate    │
│ Copy        │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ Review      │
│ 3 variants  │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ Download TXT│
│ or Copy     │
└─────────────┘

Total Time: 45 seconds
```

---

## 🎯 Engagement Score Indicator

### Visual Representation

```
Score: 85/100
████████░░ 85%

Color Coding:
┌─────────────────────────────────────┐
│ 80-100: ████ GREEN   (Excellent)    │
│ 60-79:  ████ ORANGE  (Good)         │
│ 0-59:   ████ RED     (Needs work)   │
└─────────────────────────────────────┘
```

### Score Breakdown

```
Base Score: 50 points
═════════════════════════

+ Hook Length
  └─ 3 words or less:  +15 ✅
  └─ 4-5 words:        +10
  └─ 6+ words:         +5

+ Emoji Usage
  └─ 2-3 emojis:       +15 ✅
  └─ 1 or 4 emojis:    +10
  └─ Other:            +5

+ Character Count
  └─ Under 125:        +10 ✅
  └─ 125-150:          +5

+ Trust Signals
  └─ Present:          +10 ✅

+ EU Shipping
  └─ Mentioned:        +10 ✅
───────────────────────────
Total Score:         100/100
```

---

## 📱 Responsive Design

### Desktop (1920x1080)
```
┌────────────────────────────────────────┐
│           Full side-by-side            │
│     Form (40%)  |  Preview (60%)       │
│     Spacious layout, all visible       │
└────────────────────────────────────────┘
```

### Tablet (768x1024)
```
┌──────────────────┐
│   Form (full)    │
│                  │
├──────────────────┤
│ Preview (full)   │
│  (scrollable)    │
└──────────────────┘
```

### Mobile (375x667)
```
┌────────┐
│ Form   │
│ (stack)│
├────────┤
│Preview │
│(stack, │
│scroll) │
└────────┘
```

---

## 🎭 Variant Angle Visual Guide

### Variant 1: Pain Point ❌ → ✅
```
┌─────────────────────────────────────┐
│ PAIN POINT ANGLE                    │
├─────────────────────────────────────┤
│ Structure:                          │
│ 1. Identify pain   "Tired of X?"    │
│ 2. Present solution "Try Y!"        │
│ 3. Emphasize speed  "2-3 days"      │
│ 4. Remove risk     "Money-back"     │
│                                     │
│ Best for: Conversion, Problem-aware │
│ Tone: Direct, solution-focused      │
└─────────────────────────────────────┘
```

### Variant 2: Benefit 💭 → 🌟
```
┌─────────────────────────────────────┐
│ BENEFIT ANGLE                       │
├─────────────────────────────────────┤
│ Structure:                          │
│ 1. Paint vision    "Imagine..."     │
│ 2. Show transform  "Your life with" │
│ 3. Emphasize ease  "Just 2-3 days"  │
│ 4. Create urgency  "Limited stock"  │
│                                     │
│ Best for: Awareness, Dream-building │
│ Tone: Aspirational, exciting        │
└─────────────────────────────────────┘
```

### Variant 3: Social Proof 👥 → ⭐
```
┌─────────────────────────────────────┐
│ SOCIAL PROOF ANGLE                  │
├─────────────────────────────────────┤
│ Structure:                          │
│ 1. Show popularity "10,000+ users"  │
│ 2. Real testimonial "Life-changing" │
│ 3. Emphasize trust "Verified"       │
│ 4. FOMO element    "Join thousands" │
│                                     │
│ Best for: Engagement, Trust-building│
│ Tone: Community-focused, validated  │
└─────────────────────────────────────┘
```

---

## 🌍 Market Tone Comparison

### Slovenia (SI)
```
┌─────────────────────────────────────┐
│ Tone: Casual, friendly              │
│ Language: "Pridruži se!"            │
│ Focus: Local trust, community       │
│ Example: "Tisoči Slovencev že..."  │
└─────────────────────────────────────┘
```

### Germany (DE)
```
┌─────────────────────────────────────┐
│ Tone: Professional, quality-focused │
│ Language: "Präzision und Qualität"  │
│ Focus: Efficiency, reliability      │
│ Example: "Deutsche Qualität..."     │
└─────────────────────────────────────┘
```

### Italy (IT)
```
┌─────────────────────────────────────┐
│ Tone: Warm, family-oriented         │
│ Language: "Per la tua famiglia"     │
│ Focus: Style, value, emotion        │
│ Example: "La tua famiglia merita..."│
└─────────────────────────────────────┘
```

---

## 🎬 Animation & Interaction States

### Loading State
```
┌─────────────────────────────────────┐
│ ⚡ Generating Ad Copy...            │
│                                     │
│     ⏳ Please wait 5-8 seconds      │
│                                     │
│     [===========           ] 60%    │
└─────────────────────────────────────┘
```

### Success State
```
┌─────────────────────────────────────┐
│ ✅ Ad Copy Generated Successfully!  │
│                                     │
│ 3 variants ready to use             │
│ Average engagement score: 85/100    │
└─────────────────────────────────────┘
```

### Error State
```
┌─────────────────────────────────────┐
│ ❌ Oops! Something went wrong       │
│                                     │
│ Failed to scrape product. Please    │
│ enter details manually.             │
│                                     │
│ [Try Again]  [Dismiss]              │
└─────────────────────────────────────┘
```

### Copy Confirmation
```
┌─────────────────────────────────────┐
│ ✓ Copied to clipboard!              │
└─────────────────────────────────────┘
```

---

## 📊 Data Visualization

### Character Count Meter
```
Target: Under 150 words (mobile-friendly)

Current: 142 characters
[████████████████████████░] 95%
                              ↑
                         Sweet spot
```

### Emoji Balance Indicator
```
Ideal: 2-3 emojis

Current: 3 emojis
[☺️] [🚚] [✅]

Status: ✅ Perfect balance
```

---

## 🎨 Facebook Ad Preview Mockup

```
┌─────────────────────────────────────┐
│ ┌─────┐ HS Plus                     │
│ │ HS  │ Sponsored                   │
│ └─────┘                             │
├─────────────────────────────────────┤
│                                     │
│ Tired of waiting?                   │
│                                     │
│ Get your Product delivered in just  │
│ 2-3 days from our EU warehouse! 🚚  │
│                                     │
│ No more month-long shipping from    │
│ China. Features include X, Y, Z.    │
│                                     │
│ 100% money-back guarantee! ✅       │
│                                     │
│ Shop Now - Fast EU Delivery! →     │
│                                     │
├─────────────────────────────────────┤
│ 👍 Like  💬 Comment  ↗️ Share       │
└─────────────────────────────────────┘
```

---

## 🔄 System Status Indicators

### API Health Check
```
Backend Status:
┌─────────────────────────────────────┐
│ Flask API:      ✅ Connected        │
│ Claude API:     ✅ Configured       │
│ Scraper:        ✅ Ready            │
│ Response Time:  <100ms              │
└─────────────────────────────────────┘
```

### Generation Progress
```
Step 1: ✅ Scraping product...      (2s)
Step 2: ✅ Building prompt...       (1s)
Step 3: 🔄 Calling Claude API...    (5s)
Step 4: ⏸  Parsing response...
Step 5: ⏸  Calculating scores...

Estimated time remaining: 3 seconds
```

---

## 🎯 Quick Actions Menu

```
┌─────────────────────────────────────┐
│ Quick Actions                       │
├─────────────────────────────────────┤
│ 📋 Copy Variant 1                   │
│ 📋 Copy Variant 2                   │
│ 📋 Copy Variant 3                   │
│ ⬇️  Download All as TXT             │
│ 🔄 Regenerate Copy                  │
│ 🗑️  Clear Form                      │
└─────────────────────────────────────┘
```

---

## 📱 Mobile-First Design

### Input Form (Mobile)
```
┌──────────────┐
│ Product URL  │
│ [________]   │
│              │
│ Name         │
│ [________]   │
│              │
│ Price        │
│ [________]   │
│              │
│ Features     │
│ [________]   │
│ [________]   │
│              │
│ Market       │
│ [SI ▼]      │
│              │
│ Objective    │
│ [Conv ▼]    │
│              │
│ [Generate]   │
│              │
│ Examples:    │
│ [Beauty]     │
│ [Electronics]│
│ [Automotive] │
└──────────────┘
```

---

## 🎨 Typography Scale

```
H1 (Page Title):     24px, Bold
H2 (Section):        20px, Bold
H3 (Card Title):     16px, SemiBold
Body:                14px, Regular
Small (Hint):        12px, Regular
Button:              16px, SemiBold
```

---

## 🎯 Call-to-Action Hierarchy

### Primary CTA
```
┌──────────────────────────────┐
│    ✨ Generate Ad Copy        │
└──────────────────────────────┘
Color: Blue (#1877f2)
Size: Large, full-width
```

### Secondary CTA
```
┌──────────────────────────────┐
│    ⬇️ Download TXT            │
└──────────────────────────────┘
Color: Green (#10b981)
Size: Medium
```

### Tertiary CTA
```
[📋 Copy]  [Beauty]  [Electronics]
Color: Blue outline
Size: Small
```

---

This visual guide helps understand the UI/UX design without needing screenshots. The actual implementation matches these ASCII mockups closely!
