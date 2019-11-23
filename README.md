# AGESpider
一个基于scrapy框架的爬虫脚本，对[age.fun](https://age.fan/)进行动漫的爬取，最后将json数据存入数据库。
## About
### 数据库表结构  
**请注意由于存在中文，请将table和column的字符集设置为utf8mb4**  
| column  | type |
|:--------- | :--------|
|id  | int |
|chinese_name  | varchar(255)|
|region  | varchar(255) |
|anime_type  | varchar(255) |
|original_name  | varchar(255) |
|other_name  | varchar(255) |
|author  | varchar(255) |
|company  | varchar(255) |
|time  | date |
|status  | varchar(255) |
|plot_type  | varchar(255) |
|tag  | varchar(255) |
|website  | varchar(255) |
|download_site1  | varchar(255) |
|download_site2  | varchar(255) |
|pwd1  | varchar(255) |
|pwd2  | varchar(255) |
## Usage  
1.修改spider爬虫文件中的代理获取地址，动态获取代理ip.  
2.执行scrapy crawl AGE -o anime.json 获取动漫数据  
3.执行sorting_data.py 将数据存入数据库




