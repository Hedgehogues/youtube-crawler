{
	"owner_channel": {
		"id": .header.c4TabbedHeaderRenderer.channelId,
		"title": .header.c4TabbedHeaderRenderer.title, 
		"verified":  .header.c4TabbedHeaderRenderer | has("badges"),
		"count_subscribers": .header.c4TabbedHeaderRenderer.subscriberCountText.simpleText,
		"tags": [.microformat.microformatDataRenderer.tags[]?]
	}, 
	"videos": .contents.twoColumnBrowseResultsRenderer.tabs[]? | select(.tabRenderer.selected == true) | .tabRenderer.content.sectionListRenderer | {
 		"others": [
			.contents[1:]? | .[]?.itemSectionRenderer.contents[]?.shelfRenderer | { 
				"title": .title.runs[0].text,  			
				"videos": .content.horizontalListRenderer.items	| [
					.[]?.gridVideoRenderer | select(.videoId != null) | {
                        "id": .videoId,
                        "title": .title.simpleText,
                        "published_time": .publishedTimeText.simpleText,
                        "view_counts": .viewCountText.simpleText,
                        "has_custom_subtitles": has("badges"),
                        "verified": has("ownerBadges"),
                        "duration": .thumbnailOverlays[0].thumbnailOverlayTimeStatusRenderer.text.simpleText
					}
				]   
			}
		],  		
		"general": .contents[0].itemSectionRenderer.contents[0].channelVideoPlayerRenderer | { 			
			"id": .videoId,
			"title": .title.runs[0].text, 
 			"description_parts": [ 	.description.runs[]?.text ],
			"published_time": .publishedTimeText.simpleText,  	
			"count_views": .viewCountText.simpleText
		} 	
	},
	"channels": .contents.twoColumnBrowseResultsRenderer.secondaryContents.browseSecondaryContentsRenderer.contents | [ 
		.[]?.verticalChannelSectionRenderer.items | .[]?.miniChannelRenderer | {
			"channel_id": .channelId, 
			"channel_name": .title.runs[0].text,
			"count_videos": .videoCountText.simpleText, 
			"count_subscribers": .subscriberCountText.simpleText, 
			"verified": has("ownerBadges")
		}
	]
}



