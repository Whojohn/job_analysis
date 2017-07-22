from selenium import webdriver
import time
import pymysql
from SqlControl import SqlControl

class lagou(object):

    def __init__(self):
        self.driver=webdriver.Firefox(executable_path=r"C:\Program Files\Mozilla Firefox\geckodriver.exe")
        super().__init__()

    def tryLogin(self):
        self.driver.get("https://www.lagou.com/")
        time.sleep(3)
        self.driver.find_element_by_xpath(r"id('changeCityBox')/ul/li[5]/a").click()
        time.sleep(1.5)
        self.driver.find_element_by_xpath(r"id('search_input')").send_keys("数据")
        time.sleep(0.5)
        self.driver.find_element_by_xpath(r"id('search_button')").click()
        time.sleep(3)
        sql=ThisSqlControl()
        self.catch_message(sql)


    def catch_message(self,sql):
        for x in range(1,16):
            time.sleep(0.1)
            str="id('s_position_list')/ul/li[%s]"%x
            text=self.driver.find_element_by_xpath(str).text
            after_split = text.split('\n')
            print(after_split)
            job_require = after_split[0]
            job_location = after_split[1]
            job_salary = after_split[3].split(" ")[0]
            job_company = after_split[4]
            str="id('s_position_list')/ul/li[%s]/div[1]/div[1]/div[1]/a"%x
            job_urls=self.driver.find_element_by_xpath(str).get_attribute("href")
            try:
                sql.process_item(job_require,job_location,job_salary,job_company,job_urls)
            except:
                pass
        self.next_page(sql)
        time.sleep(3)

    def next_page(self,sql):
        try:
            self.driver.find_element_by_xpath(r"id('s_position_list')/div[2]/div/span[contains(@action,'next')]").click()
            time.sleep(6)
            self.catch_message(sql)
        except:
            sql.kill_sql()
            return 0


class ThisSqlControl(SqlControl):


    def process_item(self, *item):
        sqlCommand='insert into lagou(job_require,job_location,job_salary,job_company,job_urls) ' \
                   'values("%s","%s","%s","%s","%s")'%(item)
        self.cur.execute(sqlCommand)
        self.conn.autocommit(1)


if __name__ == '__main__':
    lg=lagou()
    lg.tryLogin()
    print("werwr")