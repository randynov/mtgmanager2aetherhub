Run the command example: python scryfall.py inside the Randall_Noval folder on the command line
must be installed python3+, openpyxl(pip install openpyxl), requests(pip install requests), pandas(pip install pandas),base64(pip install base64), selenium(pip install selenium), webdriver_manager(pip install webdriver-manager)
You have to edit config.py:
csv_file = 'cards-sample.csv' # fixed for repo
github_username  # fixed for repo randynov
github_repo_name  # fixed for repo mtgmanager2aetherhub

branch_github_user_name  # The name of the account that will make a pull request example(tekin7 my github account name)
branch_name  # branch name. change, if change your github account branch
password= '' # The pasword of the account that will make a pull request
message = "Update cards-sample" # commit and pull request message

github_token = ''	# your github access token (login github->settings->Developer settings->personal access token->generate new token you can slect all scopes and generate token

Written using the pep-8 standard

Please do not forget to fork the main repo from the account for which you will make a pull request request.