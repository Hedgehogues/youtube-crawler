.[1].response.continuationContents.gridContinuation | {
	"videos": [
		.items[]?.gridVideoRenderer | {
			"id": .videoId,
			"title": .title.simpleText,
			"published_time": .publishedTimeText.simpleText,
			"view_counts": .viewCountText.simpleText,
			"has_custom_subtitles": has("badges"),
			"verified": has("ownerBadges"),
			"duration": .thumbnailOverlays[0].thumbnailOverlayTimeStatusRenderer.text.simpleText
 		}
	], 
	"next_page_token": .continuations[0].nextContinuationData | {
		"ctoken": .continuation, 
		"itct": .clickTrackingParams
	}
}
