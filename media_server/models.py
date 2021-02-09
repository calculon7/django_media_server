from django.db import models
from jsonfield import JSONField
from typing import List
from subprocess import Popen
import os
import time
import shutil
import psutil


class LibraryType(models.TextChoices):
    MOVIE = 'MOVIE'
    OTHER = 'OTHER'
    TV = 'TV'


class MediaLibrary(models.Model):
    name = models.CharField(max_length=200)
    paths = JSONField(default=[])  # list of strings
    library_type = models.CharField(max_length=200, choices=LibraryType.choices, default=LibraryType.OTHER)

    def __str__(self) -> str:
        return self.name

    def update(self):
        from .media_scanners.MediaScanner import MediaScanner
        
        scanner = MediaScanner.create(self)
        scanner.run()


class TvShow(models.Model):
    name = models.CharField(max_length=200)
    sort_name = models.CharField(max_length=200)
    library = models.ForeignKey(MediaLibrary, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class TvSeason(models.Model):
    library = models.ForeignKey('media_server.MediaLibrary', on_delete=models.CASCADE)
    tv_show = models.ForeignKey('media_server.TvShow', on_delete=models.CASCADE)
    season_index = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.tv_show.name + ' - S' + str(self.season_index).zfill(2)


class TvEpisode(models.Model):
    library = models.ForeignKey('media_server.MediaLibrary', on_delete=models.CASCADE)
    tv_show = models.ForeignKey('media_server.TvShow', on_delete=models.CASCADE)
    tv_season = models.ForeignKey('media_server.TvSeason', on_delete=models.CASCADE)
    episode_index = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.tv_show.name + ' - S' + str(self.tv_season.season_index).zfill(2) + 'E' + str(self.episode_index).zfill(2)


class MediaFile(models.Model):
    library = models.ForeignKey('media_server.MediaLibrary', on_delete=models.CASCADE)
    tv_show = models.ForeignKey('media_server.TvShow', on_delete=models.CASCADE)
    tv_season = models.ForeignKey('media_server.TvSeason', on_delete=models.CASCADE)
    tv_episode = models.ForeignKey('media_server.TvEpisode', on_delete=models.CASCADE)
    filepath = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.filepath


class TvShowDetail(models.Model):
    tv_show = models.ForeignKey('media_server.TvShow', on_delete=models.CASCADE)

    backdrop_path = models.CharField(max_length=200, null=True, blank=True)
    first_air_date = models.DateField(null=True, default=None, blank=True)
    last_air_date = models.DateField(null=True, default=None, blank=True)
    genres = JSONField(default=[], blank=True)
    tmdb_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=True)
    overview = models.TextField(blank=True)
    poster_path = models.CharField(max_length=200, null=True, blank=True)
    production_companies = JSONField(default=[], blank=True)
    type = models.CharField(max_length=200, blank=True)
    vote_average = models.FloatField(null=True, blank=True)

    sort_name = models.CharField(max_length=200, blank=True)

    def __str__(self) -> str:
        return self.name


class TvSeasonDetail(models.Model):
    tv_show = models.ForeignKey('media_server.TvShow', on_delete=models.CASCADE)
    tv_season = models.ForeignKey('media_server.TvSeason', on_delete=models.CASCADE)

    tv_show_detail = models.ForeignKey('media_server.TvShowDetail', on_delete=models.CASCADE)

    air_date = models.DateField(null=True, default=None)
    name = models.CharField(max_length=200)
    overview = models.TextField()
    tmdb_id = models.IntegerField()
    poster_path = models.CharField(max_length=200, null=True)
    season_number = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class TvEpisodeDetail(models.Model):
    tv_show = models.ForeignKey('media_server.TvShow', on_delete=models.CASCADE)
    tv_season = models.ForeignKey('media_server.TvSeason', on_delete=models.CASCADE)
    tv_episode = models.ForeignKey('media_server.TvEpisode', on_delete=models.CASCADE)

    tv_show_detail = models.ForeignKey('media_server.TvShowDetail', on_delete=models.CASCADE)
    tv_season_detail = models.ForeignKey('media_server.TvSeasonDetail', on_delete=models.CASCADE)

    air_date = models.DateField(null=True, default=None)
    episode_number = models.IntegerField()
    name = models.CharField(max_length=200, null=True)
    overview = models.TextField()
    tmdb_id = models.IntegerField()
    production_code = models.CharField(max_length=200)
    still_path = models.CharField(max_length=200, null=True)
    vote_average = models.FloatField()

    sort_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Hls(models.Model):
    media_file = models.ForeignKey('media_server.MediaFile', on_delete=models.SET_NULL, null=True)

    pid = models.IntegerField(null=True)
    start_time = models.DateTimeField(null=True)
    last_poll = models.DateTimeField(null=True)

    STREAM_ROOT = 'media_server/static/hls'

    def __str__(self) -> str:
        return str(self.pid)


    def get_output_dir(self):
        if not self.id:  # type: ignore
            raise Exception('Did not save Hls object to database')

        return os.path.join(self.STREAM_ROOT, str(self.id))  # type: ignore

    # def start(self, filepath, seek, vcodec, vbr, acodec, preset):
    #     if not os.path.isfile(filepath):
    #         raise FileNotFoundError(filepath)

    #     if not self.id:  # type: ignore
    #         raise Exception('Did not save Hls object to database')

    #     # output_dir = os.path.join(self.STREAM_ROOT, str(self.id))  # type: ignore 
    #     output_dir = self.get_output_dir()
    #     os.mkdir(output_dir)

    #     m3u8_path = os.path.join(output_dir, 'stream.m3u8')
    #     segment_name = R'stream%%d.ts'

    #     args = (
    #         'ffmpeg ' + 
    #         '-y ' + 
    #         f'-ss {seek} ' + 
    #         # '-re ' + 
    #         f'-i "{filepath}" ' + 
    #         f'-vcodec {vcodec} ' + 
    #         (f'-b:v {vbr}k ' if vcodec != 'copy' else '') + 
    #         f'-acodec {acodec} ' + 
    #         '-ac 2 ' + 
    #         '-movflags +frag_keyframe+empty_moov+faststart ' + 
    #         (f'-preset {preset} ' if vcodec != 'copy' or acodec != 'copy' else '') + 
    #         '-f hls ' + 
    #         '-pix_fmt yuv420p ' + 
    #         '-hls_time 2 ' + 
    #         '-hls_list_size 10 ' + 
    #         '-hls_delete_threshold 1 ' + 
    #         '-hls_flags split_by_time+delete_segments+second_level_segment_index ' +
    #         '-strftime 1 ' + 
    #         f'-hls_base_url \"/static/hls/{self.id}/\" ' +  # type: ignore 
    #         f'-hls_segment_filename {os.path.join(output_dir, segment_name)} ' + 
    #         '-hls_segment_type mpegts ' + 
    #         f'{m3u8_path}'
    #     )

    #     p = Popen(args)

    #     while not os.path.isfile(m3u8_path):
    #         time.sleep(0.250)

    #     return p.pid

    # ffmpeg -re -i "Z:\Videos\TV Shows\American Dad\Season 01\American Dad! - S01E01 - Pilot.mkv" 
    # -f dash -seg_duration 2 -window_size 5 -extra_window_size 0 -remove_at_exit 1 playlist.m3u8


    def start(self, filepath, seek, vcodec, vbr, acodec, preset):
        if not os.path.isfile(filepath):
            raise FileNotFoundError(filepath)

        if not self.id:  # type: ignore
            raise Exception('Did not save Hls object to database')

        output_dir = self.get_output_dir().replace('\\', '/')
        os.mkdir(output_dir)

        m3u8_path = os.path.join(output_dir, 'stream.m3u8').replace('\\', '/')
        segment_name = R'stream%%d.ts'

        args = (
            'ffmpeg ' +
            '-y ' +
            f'-ss {seek} ' +
            '-re ' +
            f'-i "{filepath}" ' +
            f'-vcodec {vcodec} ' +
            (f'-b:v {vbr}k ' if vcodec != 'copy' else '') +
            f'-acodec {acodec} ' +
            '-ac 2 ' +
            (f'-preset {preset} ' if vcodec != 'copy' or acodec != 'copy' else '') +
            '-f dash ' +
            # f'-media_seg_name "{output_dir}/chunk-stream$RepresentationID$-$Number%05d$.$ext$" ' +
            '-seg_duration 2 ' +
            '-window_size 5 ' +
            '-extra_window_size 0 ' +
            # '-remove_at_exit 1 '
            f'{m3u8_path}'
        )

        p = Popen(args)

        while not os.path.isfile(m3u8_path):
            time.sleep(0.250)

        return p.pid






    def pause(self):
        psutil.Process(self.pid).suspend()

    def resume(self):
        psutil.Process(self.pid).resume()

    def stop(self):
        psutil.Process(self.pid).kill()
        shutil.rmtree(self.get_output_dir())

