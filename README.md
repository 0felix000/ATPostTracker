# ATPostTracker
Using post.at's graphql API to track &amp; monitor shippings 

Data which needs to be filled in:

### in numbers.txt:
  #### 1)all your tracking numbers, one in each line
  
### in settings.json:
  #### 1)delayms - a delay the script will wait until requesting the tracking endpoint again for each shipment | 
  #### 2)webhook - a (discord)webhook which all tracking updates will be posted to | 
  #### 3)sendWebhookOnStartup - decide if the script should send a webhook for the most recent Event, even though it may already have been sent | 
  
just start the script & let it run. As of now no Proxies were needed to monitor the endpoint. 
