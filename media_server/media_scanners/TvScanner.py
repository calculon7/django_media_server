from media_server.models import TvEpisode, TvSeason, TvSeasonDetail, TvShow, TvShowDetail, TvEpisodeDetail
from .MediaScanner import MediaScanner, file_extensions
from typing import List, Tuple
import os
import glob
import re
from ..web_agents.tmdb import TmdbClient
from datetime import datetime


class TvScanner(MediaScanner):
    # TODO (re)scan specific subset/object and replace data
    def run(self):
        self.verbose = True

        # file scan
        print(f'File scan started')

        tv_shows_added, seasons_added, episodes_added, media_files_added = self.add_new()

        print(f'Added {tv_shows_added} new TV shows')
        print(f'Added {seasons_added} new TV seasons')
        print(f'Added {episodes_added} new TV episodes')
        print(f'Added {media_files_added} new media files')

        tv_shows_removed, seasons_removed, episodes_removed, media_files_removed = self.remove_missing()

        print(f'Removed {tv_shows_removed} empty TV shows')
        print(f'Removed {seasons_removed} empty TV seasons')
        print(f'Removed {episodes_removed} empty TV episodes')
        print(f'Removed {media_files_removed} missing media files')

        print('File scan completed')

        assert tv_shows_added <= seasons_added
        assert seasons_added <= episodes_added
        assert episodes_added <= media_files_added

        assert tv_shows_removed <= seasons_removed
        assert seasons_removed <= episodes_removed
        assert episodes_removed <= media_files_removed


        # web agent
        print('Web agent scan started')
        tmdb = TmdbClient()

        for tv_show in TvShow.objects.filter(library_id=self.library_id):

            tv_show_detail = TvShowDetail.objects.filter(tv_show__id=tv_show.id).first()

            if not tv_show_detail:

                if self.verbose:
                    print(f'Fetching info for TV episode: {tv_show.name}')

                tmdb_tv_id = tmdb.search_tv_show(tv_show.name)

                if not tmdb_tv_id:
                    if self.verbose:
                        print('Failed, could not find TV show')
                    continue

                tv_show_detail_json = tmdb.tv_show(tmdb_tv_id)

                if not tv_show_detail_json:
                    if self.verbose:
                        print('Failed, no data for TV show')
                    continue

                tv_show_detail = TvShowDetail()
                tv_show_detail.tv_show = tv_show

                try:
                    first_air_date = datetime.strptime(tv_show_detail_json['first_air_date'], '%Y-%m-%d')
                except:
                    first_air_date = None

                try:
                    last_air_date = datetime.strptime(tv_show_detail_json['last_air_date'], '%Y-%m-%d')
                except:
                    last_air_date = None

                tv_show_detail.first_air_date =       first_air_date
                tv_show_detail.last_air_date =        last_air_date

                tv_show_detail.backdrop_path =        tmdb.image_url(tv_show_detail_json['backdrop_path'])
                tv_show_detail.genres =               tv_show_detail_json['genres']
                tv_show_detail.tmdb_id =              tv_show_detail_json['id']
                tv_show_detail.name =                 tv_show_detail_json['name']
                tv_show_detail.overview =             tv_show_detail_json['overview']
                tv_show_detail.poster_path =          tmdb.image_url(tv_show_detail_json['poster_path'])
                tv_show_detail.production_companies = tv_show_detail_json['production_companies']
                tv_show_detail.type =                 tv_show_detail_json['type']
                tv_show_detail.vote_average =         tv_show_detail_json['vote_average']

                tv_show_detail.save()

                tv_show.tv_show_details = tv_show_detail
                tv_show.save()


            for season in TvSeason.objects.filter(tv_show_id=tv_show.id):

                season_detail = TvSeasonDetail.objects.filter(tv_season__id=season.id).first()

                if not season_detail:

                    if self.verbose:
                        print(f'Fetching info for TV episode: {tv_show.name}, Season {season.season_index}')

                    season_details_json = tmdb.tv_season(tv_show_detail.tmdb_id, season.season_index)  # type: ignore

                    if not season_details_json:
                        if self.verbose:
                            print('Failed, no data for season')
                        continue

                    season_detail = TvSeasonDetail()
                    season_detail.tv_show = tv_show
                    season_detail.tv_season = season
                    season_detail.tv_show_detail = tv_show_detail

                    try:
                        air_date = datetime.strptime(season_details_json['air_date'], '%Y-%m-%d')
                    except:
                        air_date = None

                    season_detail.air_date =      air_date
                    season_detail.name =          season_details_json['name']
                    season_detail.overview =      season_details_json['overview']
                    season_detail.tmdb_id =       season_details_json['id']
                    season_detail.poster_path =   tmdb.image_url(season_details_json['poster_path'])
                    season_detail.season_number = season_details_json['season_number']

                    season_detail.save()


                for episode in TvEpisode.objects.filter(tv_season_id=season.id):

                    episode_details = TvEpisodeDetail.objects.filter(tv_episode__id=episode.id).first()

                    if not episode_details:

                        if self.verbose:
                            print(f'Fetching info for TV episode: {tv_show.name}, Season {season.season_index}, Episode {episode.episode_index}')

                        episode_details_json = tmdb.tv_episode(tv_show_detail.tmdb_id, season.season_index, episode.episode_index)  # type: ignore

                        if not episode_details_json:
                            if self.verbose:
                                print('Failed, no data for episode')
                            continue

                        episode_detail = TvEpisodeDetail()
                        episode_detail.tv_show = tv_show
                        episode_detail.tv_season = season
                        episode_detail.tv_episode = episode
                        episode_detail.tv_show_detail = tv_show_detail
                        episode_detail.tv_season_detail = season_detail

                        try:
                            air_date = datetime.strptime(episode_details_json['air_date'], '%Y-%m-%d')
                        except:
                            air_date = None

                        episode_detail.air_date =        air_date
                        episode_detail.episode_number =  episode_details_json['episode_number']
                        episode_detail.name =            episode_details_json['name']
                        episode_detail.overview =        episode_details_json['overview']
                        episode_detail.tmdb_id =         episode_details_json['id']
                        episode_detail.production_code = episode_details_json['production_code']
                        episode_detail.still_path =      tmdb.image_url(episode_details_json['still_path'])
                        episode_detail.vote_average =    episode_details_json['vote_average']
                        
                        episode_detail.save()


        print('Web agent scan completed')


    @staticmethod
    def parse_season_episode(filepath: str, show_root: str):
        basename = os.path.splitext(os.path.basename(filepath))[0]

        match1 = re.search(r'(?:s\.?\s?(\d{1,2}))?\.?\s?e\.?\s?(?:(\d{1,2})(?:[^\d]|$))', basename, re.IGNORECASE)  # S01E02, S1E2, E2, E02

        if match1:
            if match1[1]:
                return filepath, int(match1[1]), int(match1[2])

            else:
                # no season number found, check parent folders below tv_show root
                parent_dir = os.path.dirname(filepath)
                subdirs = os.path.split(os.path.relpath(parent_dir, show_root))

                for subdir in subdirs:
                    match1_1 = re.search(r'(?:s|season)\.?\s?(?:(\d{1,2})(?:[^\d]|$))', subdir, re.IGNORECASE)  # s01, season 1, asdf season 01 asdf

                    if match1_1:
                        return filepath, int(match1_1[1]), int(match1[2])

                return filepath, 1, int(match1[2])

        match2 = re.search(r'(\d{1,2})\.?\s?x\.?\s?(?:(\d{1,2})(?:[^\d]|$))', basename, re.IGNORECASE)  # 01x03, 1x03, 01x3, 1x3

        if match2:
            return filepath, int(match2[1]), int(match2[2])

        match3 = re.search(r'(\d{1,2})\.?\s?of\.?\s?(?:(\d{1,2})(?:[^\d]|$))', basename, re.IGNORECASE)  # 01of02, 2.of.05, 1of2, 02.of.5

        if match3:
            return filepath, 1, int(match3[1])

        match4 = re.search(r'(?:[^a-z]|^)part\.?\s?(?:(\d{1,2})(?:[^\d]|$))', basename, re.IGNORECASE)  # part1, part.02

        if match4:
            return filepath, 1, int(match4[1])

        return None

    def add_new(self):
        from ..models import TvShow, TvSeason, TvEpisode, LibraryType, MediaLibrary, MediaFile

        libr = MediaLibrary.objects.get(id=self.library_id)

        root_folders = []

        tv_shows_added = 0
        seasons_added = 0
        episodes_added = 0
        media_files_added = 0

        for path in self.paths:
            for subdir in os.listdir(path):
                full_path = os.path.abspath(os.path.join(path, subdir))

                if os.path.isdir(full_path):
                    root_folders.append(full_path)

        for root in root_folders:
            subfiles = glob.glob(root + '/**', recursive=True)

            # subfiles with a video file extension
            video_files = [f for f in subfiles if os.path.splitext(f)[1] in file_extensions['video']]

            # video files that match the tv naming convention
            episode_naming_tuples = [self.parse_season_episode(v, root) for v in video_files]
            episode_naming_tuples = [x for x in episode_naming_tuples if x is not None]  # only keep ones with episode number parsed

            if len(episode_naming_tuples) == 0:
                continue

            show_name = os.path.basename(root)

            tv_show = TvShow.objects.filter(library_id=self.library_id, name=show_name).first()

            if not tv_show:
                tv_show = TvShow()
                tv_show.name = show_name
                tv_show.library = libr
                # tv_show.tv_show_details = None
                tv_show.save()

                tv_shows_added += 1

                if self.verbose:
                    print('Created TV Show: ' + tv_show.name)

            elif self.verbose:
                print('Found TV Show: ' + tv_show.name)

            season_numbers: List[int] = list(set([x[1] for x in episode_naming_tuples]))

            for season_number in season_numbers:
                season = TvSeason.objects.filter(tv_show__library_id=self.library_id, tv_show__name=show_name, season_index=season_number).first()

                if not season:
                    season = TvSeason()
                    season.library = libr
                    season.tv_show = tv_show
                    season.season_index = season_number
                    season.save()

                    seasons_added += 1

                    if self.verbose:
                        print('Created TV season: ' + str(season))

                elif self.verbose:
                    print('Found TV season: ' + str(season))

                for filepath, _season_number, episode_number in episode_naming_tuples:
                    if season_number != _season_number:
                        continue

                    episode = TvEpisode.objects.filter(tv_show__library_id=self.library_id, tv_show__name=show_name, tv_season__season_index=season_number, episode_index=episode_number).first()

                    if not episode:
                        episode = TvEpisode()
                        episode.library = libr
                        episode.tv_show = tv_show
                        episode.tv_season = season
                        episode.episode_index = episode_number
                        episode.save()

                        episodes_added += 1

                        if self.verbose:
                            print('Created TV episode: ' + str(episode))

                    elif self.verbose:
                        print('Found TV episode: ' + str(episode))

                    media_file = MediaFile.objects.filter(tv_show__library_id=self.library_id, filepath=filepath).first()

                    if not media_file:
                        media_file = MediaFile()
                        media_file.library = libr
                        media_file.tv_show = tv_show
                        media_file.tv_season = season
                        media_file.tv_episode = episode
                        media_file.filepath = filepath
                        media_file.save()

                        media_files_added += 1

                        if self.verbose:
                            print('Created media file: ' + str(media_file))

                    elif self.verbose:
                        print('Found media file: ' + str(media_file))

        return tv_shows_added, seasons_added, episodes_added, media_files_added

    def remove_missing(self):
        from ..models import TvShow, TvSeason, TvEpisode, LibraryType, MediaLibrary, MediaFile

        tv_shows_removed = 0
        seasons_removed = 0
        episodes_removed = 0
        media_files_removed = 0

        # table1.objects.exclude(id__in=
        #     table2.objects.filter(your_condition).values_list('id', flat=True))

        # remove non-existent media_files
        # TODO only check media_files that weren't just added
        media_files = MediaFile.objects.select_related('tv_episode').filter()

        for media_file in media_files:
            if not os.path.isfile(media_file.filepath):
                media_file.delete()

                media_files_removed += 1

                if self.verbose:
                    print('Removed media file: ' + str(media_file))

        # remove empty episodes
        episodes = TvEpisode.objects.filter()

        for episode in episodes:
            files_in_episode = MediaFile.objects.filter(tv_episode__id=episode.id)

            if len(files_in_episode) == 0:
                episode.delete()

                episodes_removed += 1

                if self.verbose:
                    print('Removed TV episode: ' + str(episode))

        # remove empty seasons
        seasons = TvSeason.objects.filter()

        for season in seasons:
            episodes_in_show = TvEpisode.objects.filter(tv_season__id=season.id)

            if len(episodes_in_show) == 0:
                season.delete()

                seasons_removed += 1

                if self.verbose:
                    print('Removed TV season: ' + str(season))

        # remove empty tv_shows
        tv_shows = TvShow.objects.filter()

        for tv_show in tv_shows:
            seasons_in_show = TvSeason.objects.filter(tv_show__id=tv_show.id)

            if len(seasons_in_show) == 0:
                tv_show.delete()

                tv_shows_removed += 1

                if self.verbose:
                    print('Removed TV show: ' + str(tv_show))

        return tv_shows_removed, seasons_removed, episodes_removed, media_files_removed
