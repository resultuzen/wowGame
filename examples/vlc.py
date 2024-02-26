import pygame
import moviepy.editor

pygame.init()
video = VideoFileClip("../video/acilisVideo.mp4")
#video.preview()

video = video.volumex(0.5)
video.ipython_display(width = 1920, height = 1080)

pygame.quit()
