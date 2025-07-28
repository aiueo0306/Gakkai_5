from glob import glob
import feedparser
from feedgen.feed import FeedGenerator
import re

fg = FeedGenerator()
fg.title('学会RSS統合')
fg.link(href='https://example.com/rss_output/combined3.xml', rel='self')
fg.description('複数フィードを統合したマスターRSS')
fg.language('ja')

for xml_file in glob('rss_output/*.xml'):
    if 'combined3.xml' in xml_file:
        continue

    d = feedparser.parse(xml_file)
    fallback_source = d.feed.get("title") or "出典不明"

    for entry in d.entries:
        title = entry.title

        # タイトル先頭の【学会名】を抽出（例：【日本腎臓病薬物療法学会】）
        match = re.match(r'^【(.+?)】', title)
        if match:
            source = match.group(1)  # 学会名を抽出
        else:
            source = fallback_source.replace("統合RSSフィード", "").strip(" []")

        # タイトルは元のまま（学会名付き）
        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=entry.link)
        fe.description(entry.get("summary", ""))
        fe.pubDate(entry.get("published", ""))
        fe.guid(entry.link + "#" + entry.get("published", "2025"))
