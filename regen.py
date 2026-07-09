#!/usr/bin/env python3
"""
Blog page regeneration script for anhoder.com.

Usage:
    python3 regen.py

After adding a new post to post/<id>/index.html, run this to:
  1. Regenerate homepage + pagination pages
  2. Update sidebar article count
  3. Regenerate archives page
  4. Regenerate sitemap.xml
  5. Regenerate atom.xml

The script reads all post detail pages, extracts metadata (date, title, tags,
word count), sorts newest-first, and redistributes across pages.
"""
import os, re, hashlib
from pathlib import Path

_ENCODING = 'utf-8'

BLOG_DIR = Path(os.path.expanduser("~/Desktop/anhoder_blog"))
POSTS_PER_PAGE = 10


def extract_article_data(post_detail_html, post_id):
    """Extract metadata and generate listing article HTML from a post detail page."""
    title_m = re.search(
        r'<h1 class="post-title">\s*<a[^>]*>\s*([^<]+?)\s*</a>',
        post_detail_html, re.DOTALL,
    )
    title = title_m.group(1).strip() if title_m else "Untitled"

    date_m = re.search(
        r'<span class="publish-time" data-t="(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})">(\d{4}-\d{2}-\d{2})</span>',
        post_detail_html,
    )
    date_full = date_m.group(1) if date_m else "1970-01-01 00:00:00"
    date_short = date_m.group(2) if date_m else "1970-01-01"

    reading_m = re.search(
        r'<span>(\d+)<span class="language" data-lan="minute">分钟</span>',
        post_detail_html,
    )
    reading_time = reading_m.group(1) if reading_m else "1"

    wc_m = re.search(
        r'<span>(\d+)<span class="pc-show language" data-lan="words">字数</span>',
        post_detail_html,
    )
    word_count = wc_m.group(1) if wc_m else "0"

    # Tags from footer
    tags_start = post_detail_html.find('<div class="tags">')
    if tags_start == -1:
        tag_matches = []
    else:
        tags_end = post_detail_html.find('</div>', tags_start)
        tags_section = post_detail_html[tags_start:tags_end]
        tag_matches = re.findall(r'<a href="(/tag/[^/]+/)"># ([^<]+)</a>', tags_section)

    if tag_matches:
        parts = []
        for url, name in tag_matches:
            parts.append(f'      <a href="{url}">\n        <span>{name}</span>\n      </a>')
        tag_html = '、\n      \n'.join(parts)
    else:
        tag_html = '      <a href="/tag/Yxu2y8I-l/">\n        <span>其它</span>\n      </a>'

    # Rotate cover image through 400..409 using hash of post ID
    img_hash = int(hashlib.md5(post_id.encode()).hexdigest()[:8], 16)
    img_num = 400 + (img_hash % 10)

    # Extract meta description for Atom feed
    desc_m = re.search(
        r'<meta name="description" content="([^"]+)"',
        post_detail_html,
    )
    summary = desc_m.group(1) if desc_m else ''

    article = f'''  <article class="post-list-box  post box-shadow-wrapper">
    <div class="article-wrapper bg-color">
      <section class="post-header">
  <h1 class="post-title">
    <a class="post-title-link" href="/post/{post_id}/">
      {title}
    </a>
  </h1>
  <div class="post-meta">
    
    <span class="meta-item pc-show">
      <i class="fa fa-calendar-o"></i>
      <span class="language" data-lan="publish">发布于</span>
      <span class="publish-time" data-t="{date_full}">{date_short}</span>
      <span class="post-meta-divider pc-show">|</span>
    </span>
    
    <span class="meta-item">
      <i class="fa fa-folder-o"></i>
      <span class="pc-show language" data-lan="category-in">分类于</span>
      
      
{tag_html}
      
      
    </span>
    <span class="post-meta-divider">|</span>
    
    <span class="meta-item">
      <i class="fa fa-clock-o"></i>
      <span>{reading_time}<span class="language" data-lan="minute">分钟</span></span>
    </span>
    <span class="meta-item">
      <span class="post-meta-divider">|</span>
      <i class="fa fa-file-word-o"></i>
      <span>{word_count}<span class="pc-show language" data-lan="words">字数</span></span>
    </span>
    
  </div>
</section>
      <div class="post-body">
        
        
          
            <a href="/post/{post_id}/" rel="contents">
              <img src="https://picsum.photos/1024/{img_num}" class="no-fancybox" />
            </a>
          
          
        
        
        <div class="post-button text-center">
          <a class="btn language" data-lan="read-more" href="/post/{post_id}/" rel="contents">
            阅读全文 »
          </a>
        </div>
        
      </div>
      
        <footer class="post-footer">
          <div class="post-eof"></div>
        </footer>
      
    </div>
  </article>
'''
    return date_short, date_full, post_id, title, article, summary


def gen_pagination(current_page, total_pages):
    """Generate pagination HTML."""
    lines = [
        '<div class="page bg-color">',
        '  <ul class="pagination-ul">',
        '    ', '    ',
        '      <!-- 1 2 3 4 ... N -->',
        '      ',
    ]
    if total_pages <= 7:
        show = list(range(1, total_pages + 1))
    elif current_page <= 4:
        show = [1, 2, 3, 4, '...', total_pages]
    elif current_page >= total_pages - 3:
        show = [1, '...', total_pages - 3, total_pages - 2, total_pages - 1, total_pages]
    else:
        show = [1, '...', current_page - 1, current_page, current_page + 1, '...', total_pages]

    for p in show:
        if p == '...':
            lines.extend([
                '        <li class="pagination-li">',
                '          …',
                '        </li>',
            ])
        else:
            active = ' pagination-active' if p == current_page else ' '
            href = '/' if p == 1 else f'/page/{p}'
            lines.extend([
                '        ', '          ',
                f'            <li class="pagination-li{active}">',
                f'              <a href="{href}">{p}</a>',
                '            </li>',
                '          ', '        ',
            ])

    lines.extend(['      ', '    ', '    '])
    if current_page > 1:
        prev = '/' if current_page == 2 else f'/page/{current_page - 1}'
        lines.extend([
            '      <li class="pagination-dir">',
            f'        <a href="{prev}"><i class="fa fa-angle-left"></i></a>',
            '      </li>',
        ])
    if current_page < total_pages:
        lines.extend([
            '      <li class="pagination-dir">',
            f'        <a href="/page/{current_page + 1}"><i class="fa fa-angle-right"></i></a>',
            '      </li>',
        ])
    lines.extend(['    ', '  </ul>', '</div>'])
    return '\n'.join(lines)


def update_sidebar_count(html, new_count):
    """Update article count in sidebar, preserving category/tag counts."""
    # Only replace the article count (first occurrence), not category/tag counts
    html = re.sub(
        r'(<span class="site-item-stat-count">)\d+(</span>\s*\n\s*<span class="site-item-stat-name language" data-lan="article">)',
        rf'\g<1>{new_count}\g<2>',
        html,
    )
    return html


def gen_sitemap(all_posts, num_pages):
    """Generate sitemap.xml."""
    BASE = 'https://anhoder.com'
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    # Static pages
    lines.append(f'  <url><loc>{BASE}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>')
    lines.append(f'  <url><loc>{BASE}/archives/</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>')
    lines.append(f'  <url><loc>{BASE}/tags/</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>')
    lines.append(f'  <url><loc>{BASE}/archives/page/2/</loc><changefreq>weekly</changefreq><priority>0.6</priority></url>')
    lines.append(f'  <url><loc>{BASE}/friends/</loc><changefreq>monthly</changefreq><priority>0.4</priority></url>')
    lines.append(f'  <url><loc>{BASE}/post/about/</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>')

    # Posts
    for _, _, pid, _, _, _ in all_posts:
        lines.append(f'  <url><loc>{BASE}/post/{pid}/</loc><priority>0.5</priority></url>')

    # Pagination pages
    for pn in range(2, num_pages + 1):
        lines.append(f'  <url><loc>{BASE}/page/{pn}/</loc><priority>0.4</priority></url>')

    # Tag pages
    tags_dir = BLOG_DIR / "tag"
    if tags_dir.exists():
        for td in sorted(os.listdir(str(tags_dir))):
            tag_home = tags_dir / td / "index.html"
            if not tag_home.exists():
                continue
            tag_pages = [tag_home]
            tag_page_dir = tags_dir / td / "page"
            if tag_page_dir.exists():
                for pp in sorted(os.listdir(str(tag_page_dir)), key=int):
                    ppf = tag_page_dir / pp / "index.html"
                    if ppf.exists():
                        tag_pages.append(ppf)
            for i in range(len(tag_pages)):
                path = f'/tag/{td}/' if i == 0 else f'/tag/{td}/page/{i + 1}/'
                lines.append(f'  <url><loc>{BASE}{path}</loc><priority>0.3</priority></url>')

    lines.append('</urlset>')
    return '\n'.join(lines) + '\n'


def _local_to_atom_time(local_dt_str):
    """Convert '2026-07-09 20:00:00' (UTC+8) to Atom UTC format '2026-07-09T12:00:00.000Z'."""
    from datetime import datetime, timezone, timedelta
    dt = datetime.strptime(local_dt_str, '%Y-%m-%d %H:%M:%S')
    dt_utc = dt - timedelta(hours=8)  # local is UTC+8
    return dt_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z')


def gen_atom(all_posts):
    """Generate atom.xml."""
    BASE = 'https://anhoder.com'
    TITLE = 'anhoder的进阶日志'
    SUBTITLE = '一川烟草，满城风絮。'

    # Latest update time from newest post
    if all_posts:
        latest_dt = all_posts[0][1]  # date_full of newest post
    else:
        latest_dt = '1970-01-01 00:00:00'
    updated = _local_to_atom_time(latest_dt)

    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        '    <id>/</id>',
        f'    <title>{TITLE}</title>',
        f'    <updated>{updated}</updated>',
        '    <generator>https://github.com/jpmonette/feed</generator>',
        '    <link rel="alternate" href="/"/>',
        '    <link rel="self" href="/atom.xml"/>',
        f'    <subtitle>{SUBTITLE}</subtitle>',
        '    <logo>/images/avatar.png</logo>',
        '    <icon>/favicon.ico</icon>',
        '    <rights>All rights reserved 2021, anhoder的进阶日志</rights>',
    ]

    for _, date_full, pid, title, _, summary in all_posts:
        atom_updated = _local_to_atom_time(date_full)
        lines.extend([
            '    <entry>',
            f'        <title type="html"><![CDATA[{title}]]></title>',
            f'        <id>/post/{pid}/</id>',
            f'        <link href="/post/{pid}/">',
            '        </link>',
            f'        <updated>{atom_updated}</updated>',
            f'        <summary type="html"><![CDATA[{summary}]]></summary>',
            '    </entry>',
            '',
        ])

    lines.append('</feed>')
    return '\n'.join(lines)


def main():
    posts_dir = BLOG_DIR / "post"
    article_pat = r'(<article class="post-list-box  post box-shadow-wrapper">.*?</article>\n)'

    # ── Collect all posts ──
    all_posts = []
    for d in sorted(os.listdir(str(posts_dir))):
        p = posts_dir / d / "index.html"
        if not p.exists():
            continue
        if d == 'about':
            continue
        with open(p, encoding=_ENCODING) as f:
            content = f.read()
        date_short, date_full, pid, title, article, summary = extract_article_data(content, d)
        all_posts.append((date_short, date_full, pid, title, article, summary))

    all_posts.sort(key=lambda x: x[0], reverse=True)
    num_pages = (len(all_posts) + POSTS_PER_PAGE - 1) // POSTS_PER_PAGE
    post_count = len(all_posts)
    print(f"Posts: {post_count}, Pages: {num_pages}")

    # ── Read page templates ──
    with open(BLOG_DIR / "index.html", encoding=_ENCODING) as f:
        hp = f.read()
    p2 = None
    if num_pages >= 2:
        with open(BLOG_DIR / "page/2/index.html", encoding=_ENCODING) as f:
            p2 = f.read()

    # Homepage template parts
    closing_pat = '</section>\n        </div>\n      </div>\n    </div>'
    sec_start = hp.find('<section class="section bg-color posts-expand slide-down-in">')
    sec_end = hp.find(closing_pat, sec_start)
    hp_header = hp[:sec_start]
    hp_footer = hp[sec_end + len(closing_pat):]
    hp_arts = list(re.finditer(article_pat, hp, re.DOTALL))
    if not hp_arts:
        raise RuntimeError(f'No article blocks found in {BLOG_DIR / "index.html"} — cannot extract preamble')
    sec_body_start = hp.find('>', sec_start) + 1
    preamble = hp[sec_body_start : hp_arts[0].start()]

    # Non-home page template parts
    p2_header = None
    p2_footer = None
    if p2 is not None:
        p2_sec_start = p2.find('<section class="section bg-color posts-expand slide-down-in">')
        p2_sec_end = p2.find(closing_pat, p2_sec_start)
        p2_header = p2[:p2_sec_start]
        p2_footer = p2[p2_sec_end + len(closing_pat):]

    # ── Regenerate pages ──
    for pn in range(1, num_pages + 1):
        start = (pn - 1) * POSTS_PER_PAGE
        end = min(start + POSTS_PER_PAGE, len(all_posts))
        page_articles = '\n'.join([a for _, _, _, _, a, _ in all_posts[start:end]])
        is_home = pn == 1
        pagination = gen_pagination(pn, num_pages)
        header = hp_header if is_home else p2_header
        footer = hp_footer if is_home else p2_footer
        # p2_header/p2_footer should always be set here since num_pages >= 2
        # when we reach non-home pages, but guard just in case:
        if header is None or footer is None:
            header, footer = hp_header, hp_footer

        section = (
            f'{header}<section class="section bg-color posts-expand slide-down-in">'
            f'{preamble}{page_articles}\n  \n            \n            \n'
            f'{pagination}\n          </section>\n        </div>\n      </div>\n    </div>{footer}'
        )

        if is_home:
            out = BLOG_DIR / "index.html"
        else:
            (BLOG_DIR / f"page/{pn}").mkdir(parents=True, exist_ok=True)
            out = BLOG_DIR / f"page/{pn}/index.html"

        with open(out, 'w', encoding=_ENCODING) as f:
            f.write(section)
        print(f"  Page {pn}: {end - start} articles → {out.relative_to(BLOG_DIR)}")

    # ── Update sidebar article count ──
    sidebar_files = (
        [BLOG_DIR / "index.html"]
        + [BLOG_DIR / f"page/{p}/index.html" for p in range(2, num_pages + 1)]
        + [BLOG_DIR / "archives/index.html", BLOG_DIR / "tags/index.html"]
    )
    # Also tag detail pages (including pagination)
    tags_dir = BLOG_DIR / "tag"
    if tags_dir.exists():
        for td in os.listdir(str(tags_dir)):
            tp = tags_dir / td / "index.html"
            if tp.exists():
                sidebar_files.append(tp)
            # Tag pagination pages: tag/<name>/page/<N>/index.html
            tag_page_dir = tags_dir / td / "page"
            if tag_page_dir.exists():
                for pp in sorted(os.listdir(str(tag_page_dir)), key=int):
                    ppf = tag_page_dir / pp / "index.html"
                    if ppf.exists():
                        sidebar_files.append(ppf)

    for fp in sidebar_files:
        if fp.exists():
            c = fp.read_text(encoding=_ENCODING)
            c = update_sidebar_count(c, post_count)
            fp.write_text(c, encoding=_ENCODING)

    # ── Update archives header count ──
    af = BLOG_DIR / "archives/index.html"
    if af.exists():
        c = af.read_text(encoding=_ENCODING)
        c = re.sub(r'(data-lan="archives" data-count=")\d+(")', rf'\g<1>{post_count}\g<2>', c)
        c = re.sub(r'共计\d+篇', f'共计{post_count}篇', c)
        af.write_text(c, encoding=_ENCODING)

    # ── Regenerate sitemap.xml ──
    sitemap_content = gen_sitemap(all_posts, num_pages)
    (BLOG_DIR / "sitemap.xml").write_text(sitemap_content, encoding=_ENCODING)
    print(f"  sitemap.xml → {len(sitemap_content)} bytes")

    # ── Regenerate atom.xml ──
    atom_content = gen_atom(all_posts)
    (BLOG_DIR / "atom.xml").write_text(atom_content, encoding=_ENCODING)
    print(f"  atom.xml → {len(atom_content)} bytes")

    print(f"\nDone. {post_count} posts, {num_pages} pages, sidebar updated.")


if __name__ == '__main__':
    main()
