This repo holds files to pull, analyze and visualize Meta ad spend data for a 2024 Columbia Journalism Review story on Courier Newsroom.

# Pulling Meta Ad Library Data from the API
To analyze data from Courier Newsroom and other outlets since 2020, we utilized a copy of the Meta Ad repo found here: https://github.com/Lejo1/facebook_ad_library.

To pull from the API, run import_requests.py in the api_pull folder first to create CSVs of the ads from each page_id listed. It will also parse low/high spend and impression ranges into seperate columns. Then run consolitdate.py to combine the CSVs into one. Make sure to change any folders in the top of the files.

To get page IDs, we searched for Courier Newsroom and any of their local newsrooms in the [Meta Ad Library Report](https://www.facebook.com/ads/library/report/?source=nav-header) that had any spending in the past 90 days (as of November 3). For Metric Media and other networks, we searched only for the wider network. For Courier newsrooms, we found that the 'Disclaimer' could be either Courier Newsroom or the name of the local paper itself. Because of this, we may be undercounting papers from other networks that list themselves as the 'Disclaimer' and have no listed connection to the broader network. 

This data fuels every chart and statistic in the story aside from the main table of October spend.

# Pulling Meta Ad Library Report from the site
To get the meta ad library report, visit https://www.facebook.com/ads/library/report/?source=nav-header and scroll to the bottom of the page. The file is only available to look back at different windows with the last seven days as possible snapshot dates, so our data will not be available for download in the future. 

# Other notes on analysis 
More can be found in the methodology section of the story, but the main difference between these two data sources lie in the way we measure spend. In the Ad Library API, we have data of ad creation date, ad delivery start date and end date. Most of the analysis in the story relies on ad delivery start day. Ads can run for multiple weeks though, so a ad that spends $50,000 over multiple weeks would show up as spending all of it in the week they launched the ad. In the report extract from the site, this measures actual spend in the dates provided. 

top_oct_spend.xlsx is a Excel file that shows the results of the manual coding I did to classify October ads above $30K into GOTV or not. You can find the source output as a CSV in the R Markdown file. I utlized the body and image of the advertisement to determine the its nature.
