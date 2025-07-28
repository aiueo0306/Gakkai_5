from glob import glob
import feedparser
from feedgen.feed import FeedGenerator

# RSSフィードの基本情報を設定
fg = FeedGenerator()
fg.title('学会RSS統合')  # マスターRSSのタイトル（内部用）
fg.link(href='https://example.com/rss_output/combined3.xml', rel='self')
fg.description('複数フィードを統合したマスターRSS')
fg.language('ja')

# 各RSSファイルを読み込んで統合（自身は除外）
for xml_file in glob('rss_output/*.xml'):
    if 'combined3.xml' in xml_file:
        continue  # 自分自身を読み込まないようにする

    d = feedparser.parse(xml_file)
    source = d.feed.get("title") or "出典不明"
    source = source.replace("統合RSSフィード", "").strip(" []")  # 不要な修飾を除去

    for entry in d.entries:
        fe = fg.add_entry()
        fe.title(entry.title)  # タイトルには一切修飾を加えない
        fe.link(href=entry.link)
        fe.description(entry.get("summary", ""))  # 概要はオプション
        fe.pubDate(entry.get("published", ""))    # 投稿日時（なければ空）
        # GUIDにはsource名を含めない or 必要に応じて調整
        fe.guid(entry.link + "#" + entry.get("published", "2025"))

# 最終的なRSSファイルを出力（上書き）
fg.rss_file('rss_output/combined3.xml')
