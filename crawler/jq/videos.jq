.contents.twoColumnBrowseResultsRenderer.tabs[1].tabRenderer.content.sectionListRenderer | {
	"tabs": .subMenu.channelSubMenuRenderer.contentTypeSubMenuItems | [
		.[]? | {
			"title": .title, 
			"url": .endpoint.commandMetadata.webCommandMetadata.url
		}
	], 
	"page_loader": .contents[0].itemSectionRenderer.contents[0].gridRenderer.continuations[0].nextContinuationData | {
		"ctoken": .continuation, 
		"itct":  .clickTrackingParams
	}, 
	"owner_videos": .contents[0].itemSectionRenderer.contents[0].gridRenderer.items | [
		.[]?.gridVideoRenderer | {
			"title": .title.simpleText, 
			"video_id": .videoId, 
			"published_time": .publishedTimeText.simpleText, 
			"view_counts": .viewCountText.simpleText, 
			"has_custom_subtitles": has("badges"), 
			"verified": has("ownerBadges"), 
			"count_views": .shortViewCountText.simpleText
		}
	]
}
