# SEO Action Plan — anhoder.com

**Date**: 2026-07-07 | **Current Health Score**: 42/100

---

## 🚀 Phase 1: Critical Fixes (Week 1)

These issues directly block or severely harm search engine indexing.

### 1. Create robots.txt
- **File**: `/robots.txt` (new)
- **Effort**: 5 min
```
User-agent: *
Allow: /
Sitemap: https://anhoder.com/sitemap.xml

User-agent: GPTBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: PerplexityBot
Allow: /
```

### 2. Generate XML Sitemap
- **File**: `/sitemap.xml` (new)
- **Effort**: 10 min
- Include: homepage, all 94 post URLs, archives, tags, pagination pages

### 3. Add JSON-LD Structured Data
- **Files**: Post template
- **Effort**: 30 min
- Add Article/BlogPosting schema to all post pages
- Add WebSite schema to homepage
- Add Person schema to About page
- Add BreadcrumbList schema

### 4. Fix Duplicate Meta Descriptions
- **Files**: All pages
- **Effort**: 15 min
- Move article-specific `<meta name="description">` from line ~64 to top of `<head>` for post pages
- Make homepage description unique and descriptive

### 5. Add Social Meta Tags (Open Graph + Twitter)
- **Files**: All pages
- **Effort**: 15 min
- Add og:title, og:description, og:image, og:url, og:type
- Add twitter:card, twitter:title, twitter:description

### 6. Replace Placeholder Images
- **Files**: `index.html`, pagination pages
- **Effort**: 30 min
- Replace `picsum.photos` images with real post thumbnail images
- Or remove images from listing if no thumbnails exist

---

## 📈 Phase 2: High-Impact Improvements (Weeks 2-3)

### 7. Publish New Content
- **Effort**: 4-8 hrs per post
- Target: 2-3 new posts in current year
- Update key old posts with new information

### 8. Fix Font Loading (CLS)
- **File**: All pages, line 15-17
- **Effort**: 2 min
- Add `&display=swap` to Google Fonts URL

### 9. Complete Schema Coverage
- **Files**: All pages
- **Effort**: 30 min
- Add WebSite/SearchAction schema on homepage
- Add Person schema on about page
- Add BreadcrumbList schema

### 10. Image Optimization
- **Files**: `/post-images/*.png`
- **Effort**: 30 min
- Convert all PNG images to WebP format
- Compress images to <100KB
- Add descriptive ALT text where missing

### 11. Performance Optimizations
- **Effort**: 15 min total
- Add `<link rel="preconnect">` for fonts.googleapis.com and cdn.jsdelivr.net
- Add `<link rel="preload">` for critical CSS
- Add prev/next pagination meta links

### 12. Expand About Page
- **File**: `/post/about/index.html`
- **Effort**: 30 min
- Add professional background, expertise areas, projects
- Include relevant experience and credentials

---

## 🎯 Phase 3: Content & Authority (Month 2)

### 13. Content Audit
- **Effort**: 2-4 hrs
- Identify posts under 300 words — expand or merge
- Add update timestamps to evergreen content
- Add internal "related posts" links

### 14. AI Search Readiness
- **Effort**: 10 min
- Create `/llms.txt` and `/llms-full.txt`
- Verify AI crawler access in robots.txt

### 15. GA4 Migration
- **Effort**: 30 min
- Create GA4 property
- Replace UA-161423102-1 with GA4 measurement ID

---

## 🔁 Phase 4: Monitoring & Iteration (Ongoing)

### 16. Search Console Setup
- Submit sitemap to Google Search Console
- Submit sitemap to Bing Webmaster Tools
- Monitor index coverage and fix errors

### 17. Regular Content
- Target: 1-2 quality posts per month
- Update old posts when technology changes

### 18. Backlink Building
- Guest posts on developer blogs
- Share on Reddit, V2EX, Hacker News
- Build out the Friends link-exchange page

---

## Estimated Effort Summary

| Phase | Items | Total Effort |
|-------|-------|-------------|
| Phase 1: Critical Fixes | 6 tasks | ~2 hours |
| Phase 2: Improvements | 6 tasks | ~6-10 hours |
| Phase 3: Content | 3 tasks | ~3-5 hours |
| Phase 4: Monitoring | 3 tasks | Ongoing |

**Total initial effort**: ~11-17 hours to reach SEO Health Score of 75+
