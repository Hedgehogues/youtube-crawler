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
                        "count_views": .viewCountText.simpleText,
                        "has_custom_subtitles": has("badges"),
                        "verified": has("ownerBadges"),
                        "duration": .thumbnailOverlays[0].thumbnailOverlayTimeStatusRenderer.text.simpleText
					}
				]   
			}
		],  		
		"general": .contents[0].itemSectionRenderer.contents[0] |
		 [
		    (
                select(.channelVideoPlayerRenderer != null) | .channelVideoPlayerRenderer | {
                    "id": .videoId,
                    "title": .title.runs[0].text,
                    "description_parts": .description.simpleText,
                    "published_time": .publishedTimeText.simpleText,
                    "count_views": .viewCountText.simpleText
                }
            ),
		    (
                select(.channelFeaturedContentRenderer != null) | .channelFeaturedContentRenderer.items[0].videoRenderer | {
                    "id": .videoId,
                    "title": .title.simpleText,
                    "description_parts": .descriptionSnippet.simpleText,
                    "published_time": .badges[0].metadataBadgeRenderer.label,
                    "count_views": .viewCountText.simpleText
                }
            ),
            (
                select(.shelfRenderer != null) | .shelfRenderer | {
                    "title": .title.runs[0].text,
                    "id": null,
                    "description_parts": .content.expandedShelfContentsRenderer.items[0].playlistRenderer.title.simpleText,
                    "published_time": .content.expandedShelfContentsRenderer.items[0].playlistRenderer.publishedTimeText.simpleText,
                    "count_views": null,
                }
            )
         ]
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



