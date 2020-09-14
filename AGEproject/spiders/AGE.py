# -*- coding: utf-8 -*-
import scrapy
import requests,time
from AGEproject.items import AgeprojectItem
from settings import GET_PROXY_URL

class AgeSpider(scrapy.Spider):
    name = 'AGE'
    allowed_domains = ['age.fan']
    domain_url = "https://age.fan"
    error_time = 0
    start_urls = []
    formation_url = "https://age.fan/detail/{}"
    page_year = 2000
    page_num = 1
    max_year = 2020
    max_page = 400

    get_proxy_url = GET_PROXY_URL
    proxy_ip = ""
    proxies = {
        "https": "https://" + proxy_ip,
    }

    def parse(self, response):
        print("正在爬取第%s部动漫" % (str(self.page_year) + str(self.page_num).zfill(4)))

        # 如果找到元素,提取
        if response.css("h4::text").extract():
            old_anime_item = response.css("span.detail_imform_value::text").extract()
            download_url = response.css(".res_links  a::attr(href)").extract()
            chinese_name = (response.css("h4::text").extract())[0].strip()
            detail = (response.css(".detail_imform_desc_pre p::text").extract())[0].strip()
            item = AgeprojectItem()
            anime_item = []
            for i in old_anime_item:
                anime_item.append(i.strip())
            item['chinese_name'] = chinese_name
            item['detail'] = detail
            item["region"] = anime_item[0]
            item["anime_type"] = anime_item[1]
            item["original_name"] = anime_item[2]
            item["other_name"] = anime_item[3]
            item["author"] = anime_item[4]
            item["company"] = anime_item[5]
            item["time"] = anime_item[6]
            item["status"] = anime_item[7]
            item["plot_type"] = anime_item[8]
            item["tag"] = anime_item[9]
            item["website"] = anime_item[10]
            item['origin_url'] = response.url

            if len(download_url) == 2:
                # download_site 应该使用request访问后获取跳转页面
                item['download_site1'] = self.get_pan_url(download_url[0])
                item['download_site2'] = self.get_pan_url(download_url[1])
                if response.css(".res_links_pswd::text").extract():
                    item['pwd1'] = response.css(".res_links_pswd::text").extract()[0][:4]
                    item['pwd2'] = response.css(".res_links_pswd::text").extract()[1][:4]
            elif len(download_url) == 1:
                item['download_site1'] = self.get_pan_url(download_url[0])
                if response.css(".res_links_pswd::text").extract():
                    item['pwd1'] = response.css(".res_links_pswd::text").extract()[0][:4]

            print(item)
            yield item

        if self.page_year <= self.max_year:
            if self.page_num < self.max_page:
                self.page_num += 1
            else:
                self.page_year += 1
                self.page_num = 1
            new_url = self.formation_url.format(str(self.page_year) + str(self.page_num).zfill(4))
            yield scrapy.Request(url=new_url, callback=self.parse)

    def get_pan_url(self, url):
        return self.domain_url + url
        # try:
        #     h = requests.head(self.domain_url + url, allow_redirects=False, proxies=self.proxies, timeout=10)

        #     if h.headers['Location'] == '/captcha':
        #         # print(h.headers)
        #         self.refresh_proxy_ip()
        #         t = requests.head(self.domain_url + url, allow_redirects=False, proxies=self.proxies)
        #         return t.headers['Location']

        #     return h.headers['Location']
        # except KeyError:
        #     return "no link"
        # except:
        #     self.refresh_proxy_ip()
        #     return self.get_pan_url(url)


    def start_requests(self):
        # self.refresh_proxy_ip()
        url = self.formation_url.format(str(self.page_year) + str(self.page_num).zfill(4))
        return [scrapy.FormRequest(url=url, callback=self.parse)]

    def refresh_proxy_ip(self):
        ip = requests.get(self.get_proxy_url).text.replace(
            "\r\n", "")
        proxies = {
            "https": "https://" + ip,
        }
        self.proxies = proxies
        self.proxy_ip = ip
        return ip

    def get_next_url(self):

        pass



