import pygame
import moviepy.editor

pygame.init()
video = moviepy.editor.VideoFileClip("video.mp4")

video = video.volumex(0.5)
#video.ipython_display(width = 1920, height = 1080)

video.preview(width = 1920, height = 1080)
pygame.quit()
