.[1].response.continuationContents.gridContinuation | {
 	"channels": [
 		.items[]?.gridChannelRenderer | {
 			"verified": has("ownerBadges"),
  			"count_subscribers": .subscriberCountText.simpleText,
  			"title": .title.simpleText,
  			"count_videos": .videoCountText.simpleText,
 			"channel_id": .channelId
		}
 	],  	
	"next_page_token": .continuations[0].nextContinuationData | {
		"ctoken": .continuation, 
 		"itct": .clickTrackingParams
 	}
}
