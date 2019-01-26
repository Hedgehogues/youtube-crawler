.contents.twoColumnBrowseResultsRenderer.tabs[5].tabRenderer.content.sectionListRenderer.contents[0].itemSectionRenderer.contents[0].channelAboutFullMetadataRenderer | {
	"title": .title.simpleText, 
	"description": .description.simpleText, 
	"joined_date": .joinedDateText.simpleText, 
	"count_views": .viewCountText.runs[0].text, 
	"count_subscribers": .subscriberCountText.runs[0].text, 
	"links": .primaryLinks | [
		.[]? | {
			"title": .title.simpleText, 
			"url": .navigationEndpoint.commandMetadata.webCommandMetadata.url 
		}
	]
}
