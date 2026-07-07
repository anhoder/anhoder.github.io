# SEO Full Audit Report — anhoder.com

**Audit Date**: 2026-07-07
**URL**: https://anhoder.com
**Platform**: Gridea (Static Site Generator) + Next Theme (by HsxyHao)
**Business Type**: Personal Technical Blog
**Total Pages**: ~130+ (94 articles + archives + tags + pagination)

---

## Executive Summary

### SEO Health Score: **42 / 100**

| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| Technical SEO | 30 | 22% | 6.6 |
| Content Quality | 40 | 23% | 9.2 |
| On-Page SEO | 45 | 20% | 9.0 |
| Schema / Structured Data | 0 | 10% | 0.0 |
| Performance (CWV) | 55 | 10% | 5.5 |
| AI Search Readiness | 25 | 10% | 2.5 |
| Images | 35 | 5% | 1.8 |
| **TOTAL** | | | **42.4** |

### Top 5 Critical Issues

1. 🔴 **No robots.txt** — Search engines have no crawl guidance
2. 🔴 **No XML sitemap** — No sitemap.xml submitted to search engines
3. 🔴 **No structured data (JSON-LD)** — Zero schema markup on all pages
4. 🔴 **Content is stale** — Last post 2021-12-25 (4+ years), may hurt rankings
5. 🔴 **Duplicate meta descriptions** — Every page has the same generic description

### Top 5 Quick Wins

1. 🟢 Add robots.txt (5 minutes)
2. 🟢 Generate XML sitemap (5 minutes)
3. 🟢 Add Article/BlogPosting JSON-LD schema to post template (30 minutes)
4. 🟢 Add Open Graph + Twitter Card tags to template (15 minutes)
5. 🟢 Fix duplicate meta descriptions on post pages (10 minutes)

---

## 1. Technical SEO — Score: 30/100

### What's Working ✅
- All pages are static HTML — excellent for crawling and TTFB
- Clean URL structure (no .html extensions, no query params)
- HTTPS enabled
- Proper charset (UTF-8)
- Viewport meta tag present
- Atom feed available at `/atom.xml`
- Semantic HTML elements used (`<header>`, `<nav>`, `<section>`, `<article>`, `<footer>`)
- Proper 404 page exists at `404.html`

### Issues Found

| # | Issue | Severity | Location | Recommendation |
|---|-------|----------|----------|----------------|
| 1 | No robots.txt | 🔴 Critical | Root (404 on live) | Create `robots.txt` at root with `Sitemap:` directive pointing to sitemap |
| 2 | No XML sitemap | 🔴 Critical | Root (404 on live) | Generate `sitemap.xml` with all post/archive/tag URLs |
| 3 | No canonical URL tags | 🟠 High | All pages | Add `<link rel="canonical">` to every page |
| 4 | No Open Graph tags | 🟠 High | All pages | Add og:title, og:description, og:image, og:url, og:type |
| 5 | No Twitter Card tags | 🟠 High | All pages | Add twitter:card, twitter:title, twitter:description |
| 6 | `<html>` lacks lang attribute | 🟡 Medium | All blog pages | Add `lang="zh-CN"` to `<html>` tag |
| 7 | No hreflang tags | 🟡 Medium | All pages | Add `<link rel="alternate" hreflang="zh-CN">` |
| 8 | `user-scalable=no` in viewport | 🟢 Low | All pages | Change to `user-scalable=yes` for accessibility |
| 9 | No prev/next pagination links | 🟢 Low | Pagination pages | Add `<link rel="prev">` / `<link rel="next">` |

---

## 2. On-Page SEO — Score: 45/100

### What's Working ✅
- Post title format: `Post Title | Site Name` — good pattern
- Article-specific descriptions exist in body area (line ~64)
- Publication dates displayed with Chinese locale
- Reading time and word count shown per post
- Clean internal linking to categories/tags
- Navigation structure covers all main sections

### Issues Found

| # | Issue | Severity | Location | Recommendation |
|---|-------|----------|----------|----------------|
| 1 | Duplicate meta descriptions across ALL pages | 🔴 Critical | `index.html:9` and all posts | The generic `"一川烟草，满城风絮。"` appears before the article-specific one (line 64). Swap order or make unique per page. |
| 2 | Duplicate meta keywords | 🟠 High | All pages | All pages use `"anhoder的进阶日志"`. Posts have article-specific keywords at line 65 but the generic ones at line 8 come first. |
| 3 | Multiple `<h1>` tags on post pages | 🟡 Medium | Post detail pages | Post titles are `<h1>` AND article content headings from markdown are also `<h1>` — only one h1 per page |
| 4 | No breadcrumb navigation | 🟡 Medium | All pages | Add breadcrumbs for better UX and rich results |
| 5 | Homepage title lacks keyword targeting | 🟢 Low | `index.html:11` | `"anhoder的进阶日志"` doesn't describe content. Consider: `"anhoder的进阶日志 — PHP/Go/后端开发技术博客"` |
| 6 | No related posts section | 🟢 Low | Post detail pages | Add "related posts" to improve internal linking and dwell time |

---

## 3. Content Quality (E-E-A-T) — Score: 40/100

### What's Working ✅
- 94 original technical articles (PHP, Go, PostgreSQL, etc.)
- Clear categories and tags for content organization
- Author has GitHub profile with social proof
- Author bio available on About page
- Code syntax highlighting with highlight.js
- Proper heading hierarchy within articles

### Issues Found

| # | Issue | Severity | Location | Recommendation |
|---|-------|----------|----------|----------------|
| 1 | Content severely stale — last post Dec 2021 | 🔴 Critical | atom.xml `/updated` | Publish new content. Google prefers fresh/updated content. Consider adding update dates to old posts. |
| 2 | About page is extremely thin (56 words) | 🟠 High | `/post/about/` | Expand author bio with expertise, experience, credentials, and E-E-A-T signals |
| 3 | No article update/modified dates | 🟡 Medium | All post pages | Show both "published" and "updated" dates |
| 4 | Some posts may be under 300 words | 🟡 Medium | Various | Audit short posts and merge or expand them |
| 5 | No outbound links to authoritative sources | 🟢 Low | Most posts | Link to official docs, research papers, or reputable sources |
| 6 | Friends/link-exchange page nearly empty | 🟢 Low | `/friends/` | Either build a link exchange network or remove the page |
| 7 | No comments system | 🟢 Low | Post pages | Consider adding comments (Giscus/Disqus) for engagement signals |

---

## 4. Schema / Structured Data — Score: 0/100

### Issues Found

| # | Issue | Severity | Location | Recommendation |
|---|-------|----------|----------|----------------|
| 1 | **Zero structured data found** | 🔴 Critical | All pages | No JSON-LD, no microdata, no RDFa anywhere |

### Required Schema Implementations:

**Homepage** — `WebSite` + `SearchAction`:
```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "anhoder的进阶日志",
  "url": "https://anhoder.com",
  "description": "一川烟草，满城风絮。",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://anhoder.com/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

**Post Pages** — `Article` / `BlogPosting`:
```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Post Title",
  "datePublished": "2021-12-25",
  "author": {
    "@type": "Person",
    "name": "anhoder",
    "url": "https://github.com/anhoder"
  },
  "description": "Article description"
}
```

**About Page** — `Person`:
```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "anhoder",
  "url": "https://anhoder.com/post/about/",
  "sameAs": [
    "https://github.com/anhoder",
    "https://twitter.com/Alan_Albert_"
  ]
}
```

**BreadcrumbList** on all pages.

---

## 5. Images — Score: 35/100

### What's Working ✅
- Lazy loading (`loading="lazy"`) on images
- `<figure>` + `<figcaption>` for post images
- Favicon with cache-busting version
- Real post-images/ directory with actual screenshots (50 images)

### Issues Found

| # | Issue | Severity | Location | Recommendation |
|---|-------|----------|----------|----------------|
| 1 | Listing pages use random picsum.photos images | 🔴 Critical | `index.html` and pagination | Replace `picsum.photos` placeholders with real post thumbnails or remove them |
| 2 | PNG images not optimized (some 300KB+) | 🟠 High | `post-images/` | Convert to WebP/AVIF, compress (e.g., `post-images/1617677746929.png` = 321KB) |
| 3 | Images lack descriptive filenames | 🟡 Medium | `post-images/` | Timestamp-based names like `1617624599510.png` are not descriptive — rename with keywords |
| 4 | No responsive images | 🟡 Medium | All pages | Add `srcset` and `sizes` attributes for different viewport widths |
| 5 | Missing explicit width/height (CLS risk) | 🟡 Medium | Some images | Add width and height attributes to prevent layout shift |
| 6 | No Apple touch icon | 🟢 Low | All pages | Add `<link rel="apple-touch-icon">` for iOS bookmarks |
| 7 | Favicon only .ico (no modern formats) | 🟢 Low | Root | Add 32x32 PNG and 180x180 Apple icon variants |
| 8 | Avatar image is 221KB PNG | 🟢 Low | `/images/avatar.png` | Optimize to <50KB WebP |

---

## 6. Performance (Core Web Vitals) — Score: 55/100

### What's Working ✅
- Static HTML — minimal server processing
- GA and Baidu scripts use async loading
- KaTeX scripts use `defer`
- Pace.js loading indicator
- Font Awesome icons

### Issues Found

| # | Issue | Severity | Location | Recommendation |
|---|-------|----------|----------|----------------|
| 1 | Google Fonts without `font-display:swap` | 🟠 High | All pages (line 15-17) | Add `&display=swap` to Google Fonts URL to prevent CLS |
| 2 | 5 render-blocking CSS files in `<head>` | 🟠 High | All pages | Inline critical CSS, defer non-critical stylesheets |
| 3 | main.css is 39KB / 2192 lines unminified | 🟡 Medium | `/styles/main.css` | Minify CSS — target <15KB for critical path |
| 4 | 8+ third-party external resources | 🟡 Medium | All pages | Add `preconnect` for origins: `fonts.googleapis.com`, `cdn.jsdelivr.net` |
| 5 | No resource hints (preload/prefetch) | 🟡 Medium | All pages | Add `<link rel="preload">` for key fonts/CSS |
| 6 | KaTeX loaded globally (not just math pages) | 🟡 Medium | All pages | Conditionally load KaTeX only on pages with math content |
| 7 | Velocity.js loaded globally | 🟢 Low | All pages | Consider CSS-only animations or tree-shake unused features |
| 8 | GA uses deprecated UA format | 🟢 Low | All pages | Migrate to Google Analytics 4 (GA4) before UA sunset |
| 9 | Live2D kanbanmusume widget | 🟢 Low | `media/live2d/` | This is decorative-only; consider removing or lazy-loading |

### Third-Party Domains (8 total):

| Domain | Purpose | Impact |
|--------|---------|--------|
| `fonts.googleapis.com` | Font loading | Render-blocking |
| `googletagmanager.com` | Google Analytics | Async |
| `hm.baidu.com` | Baidu Analytics | Async |
| `cdn.jsdelivr.net` | Pace.js, Velocity.js, KaTeX | Render-blocking CSS |
| `picsum.photos` | Placeholder images | Unnecessary external dependency |

---

## 7. AI Search Readiness — Score: 25/100

### What's Working ✅
- Semantic HTML structure
- Clear publication dates on posts
- Atom feed for structured consumption
- Clean text content without excessive div nesting

### Issues Found

| # | Issue | Severity | Location | Recommendation |
|---|-------|----------|----------|----------------|
| 1 | No llms.txt / llms-full.txt | 🟠 High | Root | Create `/llms.txt` listing key pages for LLM crawlers |
| 2 | No AI crawler guidance (no robots.txt) | 🟠 High | Root | Add robots.txt with AI crawler rules (GPTBot, Claude, PerplexityBot, etc.) |
| 3 | No structured data for AI parsing | 🟡 Medium | All pages | Add JSON-LD schema (see Section 4) |
| 4 | Missing author attribution in metadata | 🟡 Medium | All pages | Add `<meta name="author">` and structured author data |
| 5 | No clear content modification timestamps | 🟡 Medium | Post pages | Add `<meta property="article:modified_time">` |

### Required llms.txt:
```
# anhoder.com
> anhoder的进阶日志 — 太阳不热，糖也正适合。
Technical blog about PHP, Go, PostgreSQL, and backend development.

## Core Pages
- [Blog Home](https://anhoder.com): Latest articles
- [Archives](https://anhoder.com/archives/): All 94 articles
- [About](https://anhoder.com/post/about/): Author bio and contact

## Optional
- [Tags](https://anhoder.com/tags/): Browse by topic
- [Atom Feed](https://anhoder.com/atom.xml): Subscribe
```

---

## 8. Action Plan

### Phase 1: Critical Fixes (Week 1)

| Priority | Task | Effort |
|----------|------|--------|
| 🔴 | Create robots.txt with Sitemap directive | 5 min |
| 🔴 | Generate sitemap.xml with all URLs | 10 min |
| 🔴 | Add JSON-LD Article schema to post template | 30 min |
| 🔴 | Fix duplicate meta descriptions (move article-specific desc to top) | 15 min |
| 🔴 | Add Open Graph + Twitter Card meta tags | 15 min |
| 🔴 | Replace picsum.photos images with real thumbnails or remove | 30 min |
| 🟠 | Add canonical URL tags to all pages | 10 min |
| 🟠 | Fix `<html lang>` attribute and `user-scalable` | 2 min |

### Phase 2: High-Impact Improvements (Weeks 2-3)

| Priority | Task | Effort |
|----------|------|--------|
| 🟠 | Publish 2-3 new blog posts | 4-8 hrs |
| 🟠 | Add `font-display:swap` to Google Fonts | 2 min |
| 🟠 | Add JSON-LD WebSite, Person, BreadcrumbList schemas | 30 min |
| 🟠 | Optimize images: convert PNG to WebP, compress | 30 min |
| 🟡 | Add preconnect hints for third-party origins | 5 min |
| 🟡 | Add prev/next pagination meta links | 10 min |
| 🟡 | Improve About page content (E-E-A-T signals) | 30 min |
| 🟡 | Add breadcrumb navigation | 1 hr |

### Phase 3: Content & Authority (Month 2)

| Priority | Task | Effort |
|----------|------|--------|
| 🟡 | Audit thin content — expand or merge short posts | 2-4 hrs |
| 🟡 | Add "updated" dates to key articles | 30 min |
| 🟡 | Add related posts section on each article | 1 hr |
| 🟡 | Create llms.txt for AI crawlers | 10 min |
| 🟢 | Add outbound links to authoritative sources | ongoing |
| 🟢 | Set up GA4 migration | 30 min |

### Phase 4: Monitoring & Iteration (Ongoing)

| Priority | Task | Effort |
|----------|------|--------|
| 🟢 | Submit sitemap to Google Search Console | 5 min |
| 🟢 | Submit sitemap to Bing Webmaster Tools | 5 min |
| 🟢 | Monitor Core Web Vitals in Search Console | ongoing |
| 🟢 | Regular content updates (aim for 1-2 posts/month) | ongoing |
| 🟢 | Build backlinks via guest posts, communities | ongoing |

---

## Appendix: File Reference

### Key Files to Modify
| File | Changes Needed |
|------|---------------|
| `robots.txt` | **CREATE** — crawl rules + sitemap location |
| `sitemap.xml` | **CREATE** — all URL listing |
| `llms.txt` | **CREATE** — LLM crawler guidance |
| `index.html` | Fix description, add OG/Twitter/schema tags, fix picsum images |
| `post/*/index.html` | Fix descriptions, add schema, canonical, OG tags |
| `post/about/index.html` | Expand content, add Person schema |
| `404.html` | Add lang="zh-CN" |
| `styles/main.css` | Minify, audit unused rules |
| `post-images/*.png` | Convert to WebP, compress |

### Generated Artifacts
*This report was generated by manual codebase audit on 2026-07-07.*
