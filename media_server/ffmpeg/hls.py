# from ..models import MediaFile, HlsProcess


# class Hls:



# def delete_streamdir(media_file_id: int):
#     streamdir = 'media_server/static/hls-' + str(media_file_id)
#     shutil.rmtree(streamdir)


# def stream(file: MediaFile, seek, vcodec, vbr, acodec, preset) -> int:
#     streamdir = 'media_server/static/hls-' + str(file.id)  # type: ignore

#     m3u8_path = os.path.join(streamdir, 'stream.m3u8')

#     if not os.path.isdir(streamdir):
#         os.mkdir(streamdir)
    
#     else:
#         delete_streamdir(file.id)  # type: ignore
#         os.mkdir(streamdir)

#     args = (
#         'ffmpeg '
#         '-y '
#         f'-ss {seek} '
#         '-re '
#         f'-i "{file.filepath}" '
#         f'-vcodec {vcodec} '
#         f'-b:v {vbr}k '
#         f'-acodec {acodec} '
#         '-ac 2 '
#         '-movflags +frag_keyframe+empty_moov+faststart '
#         f'-preset {preset} '
#         '-f hls '
#         '-pix_fmt yuv420p '
#         '-hls_time 2 '
#         '-hls_list_size 10 '
#         '-hls_delete_threshold 1 '
#         '-hls_flags split_by_time+delete_segments+second_level_segment_index '
#         '-strftime 1 '
#         f'-hls_base_url \"/static/hls-{file.id}/\" '  # type: ignore
#         '-hls_segment_filename ' + os.path.join(streamdir, R'stream%%d.ts') + ' '
#         '-hls_segment_type mpegts '
#         '' + m3u8_path
#     )

#     p = Popen(args)

#     while not os.path.isfile(m3u8_path):
#         time.sleep(0.250)

#     return p.pid
