# Stock tweets analysis
Research Assistant Project - Stock Tweets Extraction and Analysis

This work is done as an very early stage project to study how informative social media is for predicting prices, and in particular, trading prices. 
I scraped several years of historical messages from the website Stocktwits (https://stocktwits.com/) using various cryptocurrency and stock hashtags and did a deep dive analysis into the platforms tweeting activities and userbase.

Processed billions of tweets and performed EDA to understand the tweeting pattern. 

Going through each set of stocks, created pairwise links across stocks by counting the number of times they are tweeted about in the same tweet and visualised the linkage strengths in a Network graph to see interesting stock tweeting patters observed for major stocks (Sample network graph is shown)


<img width="884" alt="Screenshot 2024-01-03 at 1 45 33 PM" src="https://github.com/chaitanyakota1/StockTweetsAnalysis/assets/105067802/4f715dcf-c8fc-4612-ad32-0fdb4c0342c7">






Performed LDA topic modeling on the text to create some pricing factors, and then relate these pricing factors to future movements in cryptocurrency prices (Download the LDA html file for the sample groups in TSLA tweets)

