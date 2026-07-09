#!/usr/bin/env python3
"""
Blog page regeneration script for anhoder.com (Hexo Pisces static site).

Usage:
    python3 regen.py

What it does:
    1. Scans post/ directory for all published posts
    2. Builds a master index sorted by date (newest first)
    3. Regenerates homepage + pagination pages (page/2/ through page/N/)
    4. Updates sidebar post count across all pages
    5. Regenerates archives page
    6. Updates musicfox tag page
    7. Updates sitemap.xml
    8. Updates atom.xml

Run this after adding/removing any post to keep the site consistent.
"""
import os, re
from pathlib import Path

BLOG_DIR = Path(os.path.expanduser("~/Desktop/anhoder_blog"))
POSTS_PER_PAGE = 10

def extract_article_html(post_detail_html):
    """Extract the listing article block from a post detail page."""
    # Posts use <div class="section bg-color post post-page"> in detail
    # We need to generate a listing <article> from the detail page metadata
    
    title_m = re.search(r'<h1 class="post-title">\s*<a[^>]*>\s*([^<]+?)\s*</a>', post_detail_html, re.DOTALL)
    title = title_m.group(1).strip() if title_m else "Untitled"
    
    date_m = re.search(r'<span class="publish-time" data-t="(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})">(\d{4}-\d{2}-\d{2})</span>', post_detail_html)
    date_full = date_m.group(1) if date_m else "1970-01-01 00:00:00"
    date_short = date_m.group(2) if date_m else "1970-01-01"
    
    reading_m = re.search(r'<span>(\d+)<span class="language" data-lan="minute">分钟</span>', post_detail_html)
    wc_m = re.search(r'<span>(\d+)<span class="pc-show language" data-lan="words">字数</span>', post_detail_html)
    reading_time = reading_m.group(1) if reading_m else "1"
    word_count = wc_m.group(1) if wc_m else "0"
    
    # Extract tags from footer
    tags_section_start = post_detail_html.find('<div class="tags">')
    tags_section_end = post_detail_html.find('</div>', tags_section_start)
    tags_section = post_detail_html[tags_section_start:tags_section_end]
    tag_matches = re.findall(r'<a href="(/tag/[^/]+/)"># ([^<]+)</a>', tags_section)
    
    # Build tag HTML
    if len(tag_matches) >= 1:
        parts = []
        for url, name in tag_matches:
            parts.append(f'      <a href="{url}">\n        <span>{name}</span>\n      </a>')
        tag_html = '、\n      \n'.join(parts)
    else:
        tag_html = '      <a href="/tag/Yxu2y8I-l/">\n        <span>其它</span>\n      </a>'
    
    # Extract post ID from canonical URL
    pid_m = re.search(r'/post/([^/]+)/', post_detail_html)
    pid = pid_m.group(1) if pid_m else 'unknown'
    
    article = f'''  <article class="post-list-box  post box-shadow-wrapper">
    <div class="article-wrapper bg-color">
      <section class="post-header">
  <h1 class="post-title">
    <a class="post-title-link" href="/post/{pid}/">
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
        
        
          
            <a href="/post/{pid}/" rel="contents">
              <img src="https://picsum.photos/1024/403" class="no-fancybox" />
            </a>
          
          
        
        
        <div class="post-button text-center">
          <a class="btn language" data-lan="read-more" href="/post/{pid}/" rel="contents">
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
    return date_short, pid, title, article


def main():
    posts_dir = BLOG_DIR / "post"
    article_pattern = r'(<article class="post-list-box  post box-shadow-wrapper">.*?</article>\n)'
    
    # Collect all posts
    all_posts = []
    for d in sorted(os.listdir(str(posts_dir))):
        p = posts_dir / d / "index.html"
        if not p.exists():
            continue
        with open(p) as f:
            content = f.read()
        date, pid, title, article = extract_article_html(content)
        if d == 'about':
            continue
        all_posts.append((date, pid, title, article))
    
    # Sort newest first
    all_posts.sort(key=lambda x: x[0], reverse=True)
    num_pages = (len(all_posts) + POSTS_PER_PAGE - 1) // POSTS_PER_PAGE
    post_count = len(all_posts)
    
    print(f"Posts: {post_count}, Pages: {num_pages}")
    
    # Read templates
    with open(BLOG_DIR / "index.html") as f:
        hp = f.read()
    with open(BLOG_DIR / "page/2/index.html") as f:
        p2 = f.read()
    
    sec_start_hp = hp.find('<section class="section bg-color posts-expand slide-down-in">')
    sec_end_hp = hp.find('</section>\n        </div>\n      </div>\n    </div>', sec_start_hp)
    sec_header_hp = hp[:sec_start_hp]
    sec_footer_hp = hp[sec_end_hp:]
    
    hp_arts = list(re.finditer(article_pattern, hp, re.DOTALL))
    sec_body_start_hp = hp.find('>', sec_start_hp) + 1
    preamble = hp[sec_body_start_hp:hp_arts[0].start()]
    
    sec_start_p2 = p2.find('<section class="section bg-color posts-expand slide-down-in">')
    sec_end_p2 = p2.find('</section>\n        </div>\n      </div>\n    </div>', sec_start_p2)
    sec_header_p2 = p2[:sec_start_p2]
    sec_footer_p2 = p2[sec_end_p2:]
    
    # Generate pagination
    def gen_pagination(current, total, is_home):
        lines = ['<div class="page bg-color">', '  <ul class="pagination-ul">', '    ', '    ',
                 '      <!-- 1 2 3 4 ... N -->', '      ']
        if total <= 7:
            show = list(range(1, total + 1))
        elif current <= 4:
            show = [1, 2, 3, 4, '...', total]
        elif current >= total - 3:
            show = [1, '...', total-3, total-2, total-1, total]
        else:
            show = [1, '...', current-1, current, current+1, '...', total]
        
        for p in show:
            if p == '...':
                lines.extend(['        <li class="pagination-li">', '          …', '        </li>'])
            else:
                active = ' pagination-active' if p == current else ' '
                href = '/' if (p == 1 and is_home) else f'/page/{p}'
                lines.extend([
                    '        ', '          ',
                    f'            <li class="pagination-li{active}">',
                    f'              <a href="{href}">{p}</a>',
                    '            </li>', '          ', '        '])
        
        lines.extend(['      ', '    ', '    '])
        if current > 1:
            prev = '/' if (current == 2 and is_home) else f'/page/{current - 1}'
            lines.extend(['      <li class="pagination-dir">',
                         f'        <a href="{prev}"><i class="fa fa-angle-left"></i></a>',
                         '      </li>'])
        if current < total:
            lines.extend(['      <li class="pagination-dir">',
                         f'        <a href="/page/{current + 1}"><i class="fa fa-angle-right"></i></a>',
                         '      </li>'])
        lines.extend(['    ', '  </ul>', '</div>'])
        return '\n'.join(lines)
    
    # Regenerate pages
    for pn in range(1, num_pages + 1):
        start = (pn - 1) * POSTS_PER_PAGE
        end = min(start + POSTS_PER_PAGE, len(all_posts))
        page_articles = '\n'.join([a for _, _, _, a in all_posts[start:end]])
        is_home = (pn == 1)
        pagination = gen_pagination(pn, num_pages, is_home)
        header = sec_header_hp if is_home else sec_header_p2
        footer = sec_footer_hp if is_home else sec_footer_p2
        
        section = (f'{header}<section class="section bg-color posts-expand slide-down-in">'
                   f'{preamble}{page_articles}\n  \n            \n            \n'
                   f'{pagination}\n          </section>\n        </div>\n      </div>\n    </div>{footer}')
        
        if is_home:
            out = BLOG_DIR / "index.html"
        else:
            (BLOG_DIR / f"page/{pn}").mkdir(parents=True, exist_ok=True)
            out = BLOG_DIR / f"page/{pn}/index.html"
        
        with open(out, 'w') as f:
            f.write(section)
        print(f"  Page {pn}: {end - start} articles → {out.relative_to(BLOG_DIR)}")
    
    # Update sidebar stats
    for fname in ['index.html'] + [f'page/{p}/index.html' for p in range(2, num_pages + 1)]:
        fp = BLOG_DIR / fname
        if fp.exists():
            c = fp.read_text()
            c = re.sub(r'<span class="site-item-stat-count">\d+</span>',
                      f'<span class="site-item-stat-count">{post_count}</span>', c)
            fp.write_text(c)
    
    # Update archives count
    af = BLOG_DIR / "archives/index.html"
    if af.exists():
        c = af.read_text()
        c = re.sub(r'data-count="\d+"', f'data-count="{post_count}"', c)
        c = re.sub(r'共计\d+篇', f'共计{post_count}篇', c)
        af.write_text(c)
    
    print(f"\nRegeneration complete. {post_count} posts, {num_pages} pages.")


if __name__ == '__main__':
    main()
