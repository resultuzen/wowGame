from moviepy.editor import VideoFileClip

# Videoyu yükleyin
video_path = "../video/acilisVideo.mp4"
video_clip = VideoFileClip(video_path)

original_width, original_height = video_clip.size

# Yeni genişlik ve yüksekliği belirleyin
new_width = 1920  # örnek olarak 1920 piksel
new_height = 1080  # örnek olarak 1080 piksel

# Videoyu gösterin (örneğin, bir pencerede oynatmak için)
resized_video_clip = video_clip.resize(width=new_width, height=new_height)

# Videoyu gösterin (örneğin, bir pencerede oynatmak için)
resized_video_clip.preview()
