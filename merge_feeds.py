from glob import glob
import feedparser
from feedgen.feed import FeedGenerator
from dateutil import parser
from datetime import timezone

# RSSフィード生成器の初期設定
fg = FeedGenerator()
fg.title('学会RSS統合')
fg.link(href='https://example.com/rss_output/combined.xml', rel='self')
fg.description('複数フィードを統合したマスターRSS')
fg.language('ja')
fg.generator("python-feedgen")
fg.docs("http://www.rssboard.org/rss-specification")

# 各フィードファイルを走査
for xml_file in glob('rss_output/*.xml'):
    if 'combined' in xml_file:
        continue  # 自分自身の統合ファイルはスキップ

    d = feedparser.parse(xml_file)

    # 例：「日本緩和医療薬学会トピックス」→「日本緩和医療薬学会」
    feed_title = d.feed.get("title", "")
    if feed_title.endswith("トピックス"):
        source = feed_title.replace("トピックス", "").strip()
    else:
        source = feed_title.strip() or "出典不明"

    # 各記事を統合
    for entry in d.entries:
        fe = fg.add_entry()
        fe.title(f"【{source}】{entry.title}")
        fe.link(href=entry.link)
        fe.description(entry.get("summary", ""))

        # 日付の文字列をパースして datetime に変換
        pub_str = entry.get("published", "")
        try:
            pub_date = parser.parse(pub_str).replace(tzinfo=timezone.utc)
            fe.pubDate(pub_date)
            guid = f"{entry.link}#{pub_date.strftime('%Y%m%d')}"
        except Exception:
            fe.pubDate(pub_str)  # パース失敗時は文字列のまま
            guid = f"{entry.link}#{pub_str[:10]}"

        fe.guid(guid, permalink=False)

# 出力ファイル生成
fg.rss_file('rss_output/combined.xml')
print("✅ 統合RSS生成完了: rss_output/combined.xml")
