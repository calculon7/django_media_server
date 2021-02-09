from django.http.response import Http404, JsonResponse
from media_server.models import MediaFile, Hls, TvEpisode, TvEpisodeDetail, TvSeason, TvSeasonDetail, TvShow, MediaLibrary, LibraryType, TvShowDetail
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from datetime import datetime
import subprocess


def index(request):
    libraries = MediaLibrary.objects.all()
    context = {
        'libraries': libraries,
    }
    return render(request, 'media_server/index.html', context)


def library(request, library_id):
    libr = MediaLibrary.objects.get(id=library_id)

    tv_shows = None
    movies = None
    other_videos = None

    if libr.library_type == LibraryType.TV:
        template = 'media_server/library_tv_shows.html'

        tv_shows = TvShow.objects.filter(library=libr).order_by('name')
        tv_show_details = TvShowDetail.objects.filter(tv_show__in=tv_shows)

        for show in tv_shows:
            show_detail = tv_show_details.filter(tv_show=show).first()

            if show_detail:
                show.backdrop_path = show_detail.backdrop_path
                show.first_air_date = show_detail.first_air_date
                show.last_air_date = show_detail.last_air_date
                show.genres = show_detail.genres
                show.tmdb_id = show_detail.tmdb_id
                show.detail_name = show_detail.name
                show.overview = show_detail.overview
                show.poster_path = show_detail.poster_path
                show.production_companies = show_detail.production_companies
                show.type = show_detail.type
                show.vote_average = show_detail.vote_average

    elif libr.library_type == LibraryType.MOVIE:
        template = 'media_server/library_movies.html'

    else:
        template = 'media_server/library_other_video.html'

    context = {
        'library': libr,
        'tv_shows': tv_shows,
        'movies': movies,
        'other_videos': other_videos,
    }

    return render(request, template, context)


def tv_show(request, tv_show_id):
    tv_show = TvShow.objects.get(id=tv_show_id)
    seasons = TvSeason.objects.filter(tv_show=tv_show).order_by('season_index')

    if len(seasons) == 1:
        # redirect single season shows to season page
        return redirect(tv_season, tv_season_id=seasons.first().id, permanent=False)

    tv_show_detail = TvShowDetail.objects.filter(tv_show=tv_show).first()

    if tv_show_detail:
        tv_show.backdrop_path = tv_show_detail.backdrop_path
        tv_show.first_air_date = tv_show_detail.first_air_date
        tv_show.last_air_date = tv_show_detail.last_air_date
        tv_show.genres = tv_show_detail.genres
        tv_show.tmdb_id = tv_show_detail.tmdb_id
        tv_show.detail_name = tv_show_detail.name
        tv_show.overview = tv_show_detail.overview
        tv_show.poster_path = tv_show_detail.poster_path
        tv_show.production_companies = tv_show_detail.production_companies
        tv_show.type = tv_show_detail.type
        tv_show.vote_average = tv_show_detail.vote_average

    season_details = TvSeasonDetail.objects.filter(tv_season__in=seasons)
    assert len(season_details) <= len(seasons)

    for season in seasons:
        season_detail = season_details.filter(tv_season=season).first()

        if season_detail:
            season.air_date = season_detail.air_date
            season.name = season_detail.name
            season.overview = season_detail.overview
            season.tmdb_id = season_detail.tmdb_id
            season.poster_path = season_detail.poster_path
            season.season_number = season_detail.season_number

    context = {
        'library': tv_show.library,
        'tv_show': tv_show,
        'seasons': seasons,
    }
    return render(request, 'media_server/tv_show.html', context)


def tv_season(request, tv_season_id):
    season = TvSeason.objects.get(id=tv_season_id)
    tv_show = season.tv_show
    libr = season.library
    episodes = TvEpisode.objects.filter(tv_season=season).order_by('episode_index')

    tv_show_detail = TvShowDetail.objects.filter(tv_show=tv_show).first()

    if tv_show_detail:
        tv_show.backdrop_path = tv_show_detail.backdrop_path
        tv_show.first_air_date = tv_show_detail.first_air_date
        tv_show.last_air_date = tv_show_detail.last_air_date
        tv_show.genres = tv_show_detail.genres
        tv_show.tmdb_id = tv_show_detail.tmdb_id
        tv_show.detail_name = tv_show_detail.name
        tv_show.overview = tv_show_detail.overview
        tv_show.poster_path = tv_show_detail.poster_path
        tv_show.production_companies = tv_show_detail.production_companies
        tv_show.type = tv_show_detail.type
        tv_show.vote_average = tv_show_detail.vote_average

    season_detail = TvSeasonDetail.objects.filter(tv_season=season).first()

    if season_detail:
        season.air_date = season_detail.air_date
        season.name = season_detail.name
        season.overview = season_detail.overview
        season.tmdb_id = season_detail.tmdb_id
        season.poster_path = season_detail.poster_path
        season.season_number = season_detail.season_number

    episode_details = TvEpisodeDetail.objects.filter(tv_episode__in=episodes)
    assert len(episode_details) <= len(episodes)

    for episode in episodes:
        episode_detail = episode_details.filter(tv_episode=episode).first()

        if episode_detail:
            episode.air_date = episode_detail.air_date
            episode.episode_number = episode_detail.episode_number
            episode.name = episode_detail.name
            episode.overview = episode_detail.overview
            episode.tmdb_id = episode_detail.tmdb_id
            episode.production_code = episode_detail.production_code
            episode.still_path = episode_detail.still_path
            episode.vote_average = episode_detail.vote_average

    context = {
        'library': libr,
        'tv_show': tv_show,
        'season': season,
        'episodes': episodes,
    }
    return render(request, 'media_server/tv_season.html', context)


def tv_episode(request, tv_episode_id):
    episode = TvEpisode.objects.get(id=tv_episode_id)
    libr = episode.library
    tv_show = episode.tv_show
    season = episode.tv_season
    files = MediaFile.objects.filter(tv_episode=episode).order_by('filepath')  # TODO order_by quality

    tv_show_detail = TvShowDetail.objects.filter(tv_show=tv_show).first()

    if tv_show_detail:
        tv_show.backdrop_path = tv_show_detail.backdrop_path
        tv_show.first_air_date = tv_show_detail.first_air_date
        tv_show.last_air_date = tv_show_detail.last_air_date
        tv_show.genres = tv_show_detail.genres
        tv_show.tmdb_id = tv_show_detail.tmdb_id
        tv_show.detail_name = tv_show_detail.name
        tv_show.overview = tv_show_detail.overview
        tv_show.poster_path = tv_show_detail.poster_path
        tv_show.production_companies = tv_show_detail.production_companies
        tv_show.type = tv_show_detail.type
        tv_show.vote_average = tv_show_detail.vote_average

    season_detail = TvSeasonDetail.objects.filter(tv_season=season).first()

    if season_detail:
        season.air_date = season_detail.air_date
        season.name = season_detail.name
        season.overview = season_detail.overview
        season.tmdb_id = season_detail.tmdb_id
        season.poster_path = season_detail.poster_path
        season.season_number = season_detail.season_number

    episode_detail = TvEpisodeDetail.objects.filter(tv_episode=episode).first()

    if episode_detail:
        episode.air_date = episode_detail.air_date
        episode.episode_number = episode_detail.episode_number
        episode.name = episode_detail.name
        episode.overview = episode_detail.overview
        episode.tmdb_id = episode_detail.tmdb_id
        episode.production_code = episode_detail.production_code
        episode.still_path = episode_detail.still_path
        episode.vote_average = episode_detail.vote_average

    context = {
        'library': libr,
        'tv_show': tv_show,
        'season': season,
        'episode': episode,
        'files': files,
    }
    return render(request, 'media_server/tv_episode.html', context)


def media_file(request, media_file_id):
    media_file = MediaFile.objects.get(id=media_file_id)

    libr = media_file.library
    tv_show = media_file.tv_show
    season = media_file.tv_season
    episode = media_file.tv_episode

    tv_show_detail = TvShowDetail.objects.filter(tv_show=tv_show).first()

    if tv_show_detail:
        tv_show.backdrop_path = tv_show_detail.backdrop_path
        tv_show.first_air_date = tv_show_detail.first_air_date
        tv_show.last_air_date = tv_show_detail.last_air_date
        tv_show.genres = tv_show_detail.genres
        tv_show.tmdb_id = tv_show_detail.tmdb_id
        tv_show.detail_name = tv_show_detail.name
        tv_show.overview = tv_show_detail.overview
        tv_show.poster_path = tv_show_detail.poster_path
        tv_show.production_companies = tv_show_detail.production_companies
        tv_show.type = tv_show_detail.type
        tv_show.vote_average = tv_show_detail.vote_average

    season_detail = TvSeasonDetail.objects.filter(tv_season=season).first()

    if season_detail:
        season.air_date = season_detail.air_date
        season.name = season_detail.name
        season.overview = season_detail.overview
        season.tmdb_id = season_detail.tmdb_id
        season.poster_path = season_detail.poster_path
        season.season_number = season_detail.season_number

    episode_detail = TvEpisodeDetail.objects.filter(tv_episode=episode).first()

    if episode_detail:
        episode.air_date = episode_detail.air_date
        episode.episode_number = episode_detail.episode_number
        episode.name = episode_detail.name
        episode.overview = episode_detail.overview
        episode.tmdb_id = episode_detail.tmdb_id
        episode.production_code = episode_detail.production_code
        episode.still_path = episode_detail.still_path
        episode.vote_average = episode_detail.vote_average

    from .ffmpeg.probe import probe

    ffprobe = probe(media_file.filepath)

    context = {
        'library': libr,
        'tv_show': tv_show,
        'season': season,
        'episode': episode,
        'media_file': media_file,
        'ffprobe': ffprobe,
    }

    if request.GET.get('action', None) == 'play':
        # context['stream_url'] = 'hls-' + str(media_file.id) + '/stream.m3u8'

        return render(request, 'media_server/play.html', context)

    else:
        return render(request, 'media_server/media_file.html', context)


def scan(request, library_id):
    libr = MediaLibrary.objects.get(id=library_id)
    libr.update()

    # TODO return scan started info
    return HttpResponse()


def hls_start(request, media_file_id):
    media_file = MediaFile.objects.get(id=media_file_id)

    seek = request.GET.get('seek', 0)
    vcodec = request.GET.get('vcodec', 'libx264')
    vbr = request.GET.get('vbr', 2000)
    acodec = request.GET.get('acodec', 'aac')
    preset = request.GET.get('preset', 'veryfast')

    hls = Hls()
    hls.start_time = datetime.now()
    hls.last_poll = None
    hls.media_file = media_file
    hls.save()

    hls.pid = hls.start(media_file.filepath, seek, vcodec, vbr, acodec, preset)
    hls.save()

    return JsonResponse({
        'hls_id': hls.id,  # type: ignore
    })


def hls_pause(request, hls_id):
    hls = Hls.objects.filter(id=hls_id).first()

    if hls:
        hls.pause()
        return HttpResponse(status=200)

    else:
        return HttpResponse(status=404)


def hls_resume(request, hls_id):
    hls = Hls.objects.filter(id=hls_id).first()

    if hls:
        hls.resume()
        return HttpResponse(status=200)

    else:
        return HttpResponse(status=404)


def hls_stop(request, hls_id):
    hls = Hls.objects.filter(id=hls_id).first()

    if hls:
        hls.stop()
        hls.delete()
        return HttpResponse(status=200)
    
    else:
        return HttpResponse(status=404)
