from moviepy.editor import VideoFileClip

# Videoyu yükleyin
video_path = "../video/acilisVideo.mp4"
video_clip = VideoFileClip(video_path)

# Videoyu gösterin (örneğin, bir pencerede oynatmak için)
video_clip.preview()
