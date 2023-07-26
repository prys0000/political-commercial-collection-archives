from videohash import VideoHash

path1 = "E:\Speechpy\simcomp-1\P-1463-71759_Trim.mp4"
videohash1 = VideoHash(path=path1, ffmpeg_path="C:\\Users\\user\\Desktop\\ffmpeg-master-latest-win64-gpl-shared\\ffmpeg-master-latest-win64-gpl-shared\\bin\\ffmpeg.exe")


path2 = "E:\Speechpy\simcomp-1\P-1463-71760_Trim.mp4"
videohash2 = VideoHash(path=path1, ffmpeg_path="C:\\Users\\user\\Desktop\\ffmpeg-master-latest-win64-gpl-shared\\ffmpeg-master-latest-win64-gpl-shared\\bin\\ffmpeg.exe")


diff = videohash2 - videohash1
print(diff)

similar = videohash2.is_similar(videohash1)
print(similar)

path3 = "E:\Speechpy\simcomp-2\P-1139-49189.mp4"
videohash3 = VideoHash(path=path1, ffmpeg_path="C:\\Users\\user\\Desktop\\ffmpeg-master-latest-win64-gpl-shared\\ffmpeg-master-latest-win64-gpl-shared\\bin\\ffmpeg.exe")


similar = videohash3.is_similar(videohash1)
print(similar)

different = videohash3.is_different(videohash2)
print(different)

diff = videohash3 - videohash1
print(diff)

diff = videohash3 - videohash2
print(diff)

path4 = "path/to/video4.mp4"
videohash4 = VideoHash(path=path4)

equal = videohash4 == videohash1
print(equal)

diff = videohash4 - videohash1
print(diff)

similar = videohash4.is_similar(videohash2)
print(similar)

similar = videohash4.is_similar(videohash4)
print(similar)

similar = videohash4.is_similar(videohash3)
print(similar)
