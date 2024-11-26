import requests

#你的 API 密钥
API_KEY = 'AIzaSyAqFQETcR8pkeSXN68P3rThnQlhvw65itI'
#视频 ID
VIDEO_ID = 'reTsPn-t9i8'
proxies = {
    "http": "http://127.0.0.1:7890",  #Clash 的 HTTP 代理端口
    "https": "http://127.0.0.1:7890",  #Clash 的 HTTPS 代理端口
}
#构建 API 请求 URL
url = f'https://www.googleapis.com/youtube/v3/videos?id={VIDEO_ID}&part=snippet,contentDetails,statistics&key={API_KEY}'

#发送请求
response = requests.get(url,proxies=proxies)

#解析 JSON 响应
data = response.json()

#提取元数据
if 'items' in data and len(data['items']) > 0:
    video = data['items'][0]
    
    #基本信息
    snippet = video['snippet']
    title = snippet.get('title')
    uploader = snippet.get('channelTitle')
    date_added = snippet.get('publishedAt')
    category = snippet.get('categoryId')
    
    #视频时长
    content_details = video['contentDetails']
    video_length = content_details.get('duration')
    
    #统计信息
    statistics = video['statistics']
    number_of_views = statistics.get('viewCount')
    number_of_ratings = statistics.get('likeCount')  #现在通常是点赞数
    number_of_comments = statistics.get('commentCount')
    
    #输出元数据
    print(f"Title: {title}")
    print(f"Uploader: {uploader}")
    print(f"Date added: {date_added}")
    print(f"Category ID: {category}")
    print(f"Video length: {video_length}")
    print(f"Number of views: {number_of_views}")
    print(f"Number of ratings (likes): {number_of_ratings}")
    print(f"Number of comments: {number_of_comments}")
else:
    print("视频没有找到或ID无效")