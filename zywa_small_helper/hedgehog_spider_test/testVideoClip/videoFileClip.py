from moviepy.editor import VideoFileClip
import imageio.plugins.ffmpeg
imageio.plugins.ffmpeg.download()
clip = VideoFileClip("/Users/magic/Desktop/fileAnnieDownload/test.flv")
print(clip.duration)  # seconds
