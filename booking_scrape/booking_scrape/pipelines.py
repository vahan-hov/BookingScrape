# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#
#
# from scrapy.exporters import JsonItemExporter
#
#
# class BookingScrapeJSONPipeline:
#     def __init__(self):
#         self.file = open("booking.json", 'wb')
#         self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
#         self.exporter.start_exporting()
#
#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item


import time
import psycopg2


class DatabasePipeline:
    def open_spider(self, spider):
        self.start = time.time()
        self.conn = psycopg2.connect(user="book_user",
                                     password="booking",
                                     host="127.0.0.1",
                                     port="5432",
                                     database="booking_db")
        self.cursor = self.conn.cursor()

        create_table_query = '''CREATE TABLE IF NOT EXISTS booking_hotels
                                    (hotel_name TEXT,
                                    location TEXT,
                                    imgs TEXT,
                                    score_category TEXT,
                                    score TEXT,
                                    description TEXT,
                                    host_info TEXT,
                                    surroundings_type TEXT,
                                    surroundings_info TEXT,
                                    facilities TEXT,
                                    house_rules TEXT,
                                    fine_print TEXT,
                                    faq TEXT,
                                    hotel_url TEXT
                                    ); '''

        self.cursor.execute(create_table_query)
        self.conn.commit()

    def process_item(self, item, spider):
        sql = "INSERT INTO booking_hotels (hotel_name,location,imgs,score_category,score,description,host_info, \
               surroundings_type, surroundings_info,facilities,house_rules,fine_print,faq,hotel_url)\
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql,
                            (
                                item.get('hotel_name'),
                                item.get('location'),
                                item.get('imgs'),
                                item.get('score_category'),
                                item.get('score'),
                                item.get('description'),
                                item.get('host_info'),
                                item.get('surroundings_type'),
                                item.get('surroundings_info'),
                                item.get('facilities'),
                                item.get('house_rules'),
                                item.get('fine_print'),
                                item.get('faq'),
                                item.get('hotel_url')

                            )
                            )
        self.conn.commit()
        return item

    def close_spider(self, spider):
        end = time.time()
        print(f'elapsed time {end} - {self.start}s')

        self.cursor.close()
        self.conn.close()
