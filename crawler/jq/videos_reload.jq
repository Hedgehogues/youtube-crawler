.[1].response.continuationContents.gridContinuation | {
	"videos": [
		.items[]?.gridVideoRenderer | {
 			"title": .title.simpleText,
  			"video_id": .videoId,
  			"published_time": .publishedTimeText.simpleText,
  			"view_counts": .viewCountText.simpleText,
  			"has_custom_subtitles": has("badges"),
  			"verified": has("ownerBadges"),
  			"count_views": .shortViewCountText.simpleText
 		}
	], 
	"next_page_token": .continuations[0].nextContinuationData | {
		"ctoken": .continuation, 
		"itct": .clickTrackingParams
	}
}
