from glob import glob
import feedparser
from feedgen.feed import FeedGenerator

fg = FeedGenerator()
fg.title('学会RSS統合')  # ← より中立的なタイトル
fg.link(href='https://example.com/rss_output/combined.xml', rel='self')
fg.description('複数フィードを統合したマスターRSS')
fg.language('ja')

for xml_file in glob('rss_output/*.xml'):
    if 'combined.xml' in xml_file:
        continue  # 自分自身は読み込まない

    d = feedparser.parse(xml_file)
    source = d.feed.get("title") or "出典不明"
    source = source.replace("統合RSSフィード", "").strip(" []")

    for entry in d.entries:
        fe = fg.add_entry()
        fe.title(f"[{source}] {entry.title}")
        fe.link(href=entry.link)
        fe.description(entry.get("summary", ""))
        fe.pubDate(entry.get("published", ""))
        fe.guid(entry.link + "#" + entry.get("published", "2025"))

fg.rss_file('rss_output/combined3.xml')
