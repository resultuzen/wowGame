import pygame
import moviepy.editor

pygame.init()
video = moviepy.editor.VideoFileClip("../video/acilisVideo.mp4")
video.preview()
pygame.quit()
