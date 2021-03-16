# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 17:02:20 2021

@author: shane
"""
from seltools import mydriver,main
from HCM_main import hcm
from datetime import datetime
from selenium.webdriver.common.by import By

class cjr(hcm,main):
    def __init__(self,driver):
        self.driver=driver
        self.url='https://hrsa.cunyfirst.cuny.edu/psp/cnyhcprd_1/EMPLOYEE/HRMS/c/CU_HCM.CU_R1013.GBL'
    def report_get(self,id=None):
        if id:
            id=id
        #TODO add error handling here. Perhaps look in Administration for 'processing'
        if self.driver.title!='Report Manager':
            self.driver.get('https://hrsa.cunyfirst.cuny.edu/psp/cnyhcprd_2/EMPLOYEE/HRMS/c/REPORT_MANAGER.CONTENT_LIST.GBL')
        #because the table's identity isprocedurally generated, must grab individually
        self.switch_tar()
        flag=''
        while flag!="go":
            print("checking if ID is in page source")
            if id in self.driver.page_source:
                flag="go"
            else:
                self.switch_tar()
                self.waitid("PSRF_RFLTER_WRK_REFRESH_BTN")
                print('clicking refresh')
                self.cf_save(1)
                self.switch_tar()
        else:
            print('done checking, apparently')
            self.switch_tar()
            print('trying to grab table')
            table=self.grab_table('',obj=self.driver.find_element(By.CLASS_NAME,'PSLEVEL1GRID'))
            #each row in this table has 7 pieces of information, so we'll split into groups
            #and search for our instance number
            urls=table[1::7]
            print(urls)
            instances=[i.text for i in table[6::7]]
            print(instances)
            #urls are in the second column and instances are in the second to last.
            for ix,i in enumerate(instances):
                if i==id:
                    print('got one!')
                    urls[ix].click()
            #TODO add error handling here. What happens if we miss the instance?
            self.waitid('URL$1')
    def run_current(self,datadict=None,date=None):
        self.cf_save(1)
        self.switch_tar()   #what we want is in the Target Content frame
        self.waitid("#ICSearch")    #if you've only saved one of this search..
        self.cf_save(1) #waiting because it will take you to search params
        #filling out search params
        #for best results, we are doing as of today, always, Full Report
        #all fields other than Business Unit blank
        #if you've run this before, it shuld still have the prior details
        if date!=None:
            date=date
        else:
            date=datetime.now().strftime('%m/%d/%Y')
        if datadict!=None:
            datadict=datadict
        else:
            datadict={'CU_R1013_RUNCNT_ASOFDATE': date,
             'CU_R1013_COMPAN_COMPANY$0': '',
             'CU_R1013_DEPT_DEPTID$0': '',
             'CU_R1013_BU_BUSINESS_UNIT$0': 'YRK01',
             'CU_R1013_EMPCLA_EMPL_CLASS$0': '',
             'CU_R1013_JOBCD_JOBCODE$0': '',
             'CU_R1013_EEO_EEO_JOB_GROUP$0': '',
             'CU_R1013_JOBFCT_JOB_FUNCTION$0': '',
             'CU_R1013_RUNCNT_FULL_PART_TIME': '',
             'CU_R1013_RUNCNT_HR_STATUS': '',
             'CU_R1013_PAYSTS_EMPL_STATUS$0': '',
             'PRCSRQSTDLG_WRK_OUTDESTTYPE$0':'Web',
             'PRCSRQSTDLG_WRK_OUTDESTFORMAT$0':'XLS'
                    }
        self.switch_tar()
        self.data_distribute(datadict)
        self.switch_tar()
        self.waitid("PRCSRQSTDLG_WRK_LOADPRCSRQSTDLGPB") #pressing the Run button
        self.cf_save(1)
        self.data_distribute(datadict)
        self.switch_tar()
        #the save button has the same properties as the OK button here
        self.cf_save(0)     
        #now the run process has started.
        #we're going to go to report manager and obsessively check if its done
        #but first, grab process instance
        self.switch_tar()
        if 'PRCSRQSTDLG_WRK_DESCR100' in self.driver.page_source:
            instance=self.driver.find_element_by_id("PRCSRQSTDLG_WRK_DESCR100").text.split(':')[1]
        else:
            print("Couldn't get the instance number.")
            instance='0'
        self.waitid("PRCSRQSTDLG_WRK_LOADRPTLIST")
        print("now navigating to get the report")
        self.report_get(id=instance)
        
def main(USERNAME,PASSWORD,download_dir=None):
    if download_dir:
        download_dir=download_dir
    else:
        download_dir="C:\\insert\\default\\folder\\here"
    driver=mydriver.setupbrowser(mydriver(download_dir))
    home=hcm(driver,un=USERNAME,pw=PASSWORD)
    home.loginnow()
    thecjr=cjr(home.driver)
    thecjr.nav()
    thecjr.run_current()
    #thecjr.driver.quit()   #using quit instead of close because 2 windows.

if __name__ == "__main__":
    main(USERNAME,PASSWORD,download_dir=DIR)    