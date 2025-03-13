from googleapiclient.discovery import build
import urllib.parse

API_KEY = "AIzaSyBe9xgoexRzMosB8GQH4yD0L-ydDRPsgtM"  

def get_latest_comments(username, max_results=50):
    youtube = build("youtube", "v3", developerKey=API_KEY)

    encoded_username = urllib.parse.quote(username)

    # Step 1
    search_request = youtube.search().list(
        part="snippet",
        q=username,
        type="channel",
        maxResults=1
    )
    search_response = search_request.execute()

    if not search_response["items"]:
        print("Channel not found!")
        return

    channel_id = search_response["items"][0]["id"]["channelId"]
    print(f"Channel ID: {channel_id}\n")

    # Step 2
    comment_request = youtube.commentThreads().list(
        part="snippet",
        allThreadsRelatedToChannelId=channel_id,
        maxResults=max_results,  
        order="time"
    )
    
    comment_response = comment_request.execute()

    if not comment_response["items"]:
        print("No comments found for this channel.")
        return

    # Step 3
    print(f"Latest {max_results} Comments by {username}:")
    for item in comment_response["items"]:
        comment_data = item["snippet"]["topLevelComment"]["snippet"]
        author = comment_data["authorDisplayName"]
        comment_text = comment_data["textOriginal"]
        video_id = item["snippet"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        print(f"\nAuthor: {author}")
        print(f"Comment: \"{comment_text}\"")
        print(f"On Video: {video_url}")


get_latest_comments("MrBeast", max_results=50)
