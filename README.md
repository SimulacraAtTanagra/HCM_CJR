## The purpose of this project is as follows:
This project runs the Current Job Report from CUNYfirst Human Capital Management.
## Here's some back story on why I needed to build this:
The CJR is an incredibly useful report for auditing data in HCM, as well as for supplying data to other programs and people. This automates a crucial part of the process to take the human element out of it. 
## This project leverages the following libraries:
pandas, fuzzywuzzy, selenium, webdriver_manager, xlrd
## In order to use this, you'll first need do the following:
The user will need to have `USERNAME` and `PASSWORD` for CUNYfirst stored as vars, whether running from commandline or in an IDE. If the user does not add a download directory to the main call, like `main(USERNAME,PASSWORD,download_dir=X:\\somedir)`, they will need to modify the code in the main function to reflect the desired default directory. User must, obviously, have both a valid CUNYfirst account AND access to the CJR. Be warned that CJR access is not coincident with any other HCM access and has to be specifically requested separately from other roles. 
## The expected frequency for running this code is as follows:
Daily