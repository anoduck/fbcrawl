import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.exporters import CsvItemExporter
import pandas as pd

PAGE = 'mybcaf'
EMAIL = 'email'
PASSWORD = 'password'

class CommentPipeline(object):

    def open_spider(self, spider):
        self.csv_exporter = {}

    def close_spider(self, spider):
        for exporter in self.csv_exporter.values():
            exporter.finish_exporting()

    def _item_exporter(self, spider, item):
        spider_name = spider.name
        if spider_name not in self.csv_exporter:
            f =  open('{}-{}.csv'.format(PAGE ,spider_name), 'wb')
            if spider_name == 'fb':
                exporter = CsvItemExporter(
                    f, fields_to_export=[
                        "source", "shared_from", "date", "text",
                        "reactions", "likes", "ahah",
                        "love", "wow", "sigh", "grrr", "comments",
                        "post_id", "url"
                    ]
                )
            elif spider_name == 'comments':
                exporter = CsvItemExporter(
                    f, fields_to_export=[
                        'source', 'reply_to', 'date', 'reactions',
                        'text', 'source_url', 'post_id', 'url'
                    ]
                )
            exporter.start_exporting()
            self.csv_exporter[spider_name] = exporter
        return self.csv_exporter[spider_name]

    def process_item(self, item, spider):
        print(spider.name)
        exporter = self._item_exporter(spider, item)
        exporter.export_item(item)
        return item

results = []
settings = get_project_settings()
settings.set('FEED_FORMAT', 'csv')
#  settings.set('FEED_URI', 'yattarikun.csv')
settings.set('ITEM_PIPELINES', {'__main__.CommentPipeline':10})

process = CrawlerProcess(settings)
process.crawl(
    'fb', email=EMAIL,
    password=PASSWORD, page=PAGE, lang='en'
)
process.crawl(
    'comments', email=EMAIL,
    password=PASSWORD, page=PAGE, lang='en'
)

process.start()

#  settings_comment = get_project_settings()
#  settings_comment.set('FEED_FORMAT', 'csv')
#  settings_comment.set('FEED_URI', 'yattarikun_comments.csv')
#  process_comment = CrawlerProcess(settings_comment)
#  process_comment.crawl(
    #  'comments', email=EMAIL,
    #  password=PASSWORD,
    #  page='yattarikun', lang='en'
#  )

#  process_comment.start()
