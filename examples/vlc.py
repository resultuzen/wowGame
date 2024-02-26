import pygame
import moviepy.editor

pygame.init()
video = moviepy.editor.VideoFileClip("../video/acilisVideo.mp4")

video = video.volumex(0.5)
video.resize((1920, 1080))

video.preview()
pygame.quit()
