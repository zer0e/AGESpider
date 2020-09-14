# AGESpider
一个基于scrapy框架的爬虫脚本，对[agefans.tv](https://www.agefans.tv/)进行动漫的爬取，可将json数据存入数据库。   

## Usage  
0.执行`pip install -r requirements.txt` 安装依赖。  
1.可修改spider主文件中的开始年份与结束年份，默认爬取从2000-2020年间的动漫。  
2.执行scrapy crawl AGE -o anime.json 获取动漫数据  
3.根据需要，可修改settings中数据库的各项信息，执行sorting_data.py 将数据存入数据库

## Log
2020.07.05   
1.网站更改了百度云链接获取方式，需要添加Referer头。  
2.似乎改成了使用js跳转，并且对js进行了加密(sojson.v5加密)，在打开控制台同时取消了js跳转，具体跳转逻辑尚不明确。   
2020.09.14   
1.修复了由于网站404页面更改而导致爬虫终止的bug。  
2.减少了大量无效的请求  
3.取消了代理，使用更加简单。  
4.取消了获取百度云链接的功能，如需此功能，可以使用selenium从origin_url js跳转至download_url。可能会根据业余时间完成相应的转换脚本。  


