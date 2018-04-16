SELECT array_agg(tweet_id), tweet_text, array_agg(tweet_lat), array_agg(tweet_lon), array_agg(created_at), sum(1)
FROM tweet_collector_tweets
WHERE tweet_lat IS NOT NULL AND tweet_lon IS NOT NULL AND collection_id = 7
GROUP BY tweet_text