.contents.twoColumnBrowseResultsRenderer.tabs[]? | select(.tabRenderer.selected == true) | .tabRenderer.content.sectionListRenderer | {
	"channels": .contents | [
		.[]?.itemSectionRenderer.contents[]?.gridRenderer.items[]?.gridChannelRenderer | {
			"verified": has("ownerBadges"), 
			"count_subscribers": .subscriberCountText.simpleText, 
			"title": .title.simpleText, 
			"count_videos": .videoCountText.simpleText,
			"channelId": .channelId
		}
	],
	"tabs": .subMenu.channelSubMenuRenderer.contentTypeSubMenuItems | [
		.[]? | {
			"title": .title,
			"url": .endpoint.commandMetadata.webCommandMetadata.url
		}
	],
	"next_page_token": .contents[0].itemSectionRenderer.contents[0].gridRenderer.continuations[0].nextContinuationData | {
		"ctoken": .continuation,
		"itct":  .clickTrackingParams
	},
}
