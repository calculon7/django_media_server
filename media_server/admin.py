from django.contrib import admin

# Register your models here.

from .models import Hls, MediaLibrary, TvShow, TvSeason, TvEpisode, MediaFile, LibraryType, TvShowDetail, TvSeasonDetail, TvEpisodeDetail


admin.site.register(MediaLibrary)

admin.site.register(TvShow)
admin.site.register(TvSeason)
admin.site.register(TvEpisode)
admin.site.register(MediaFile)

admin.site.register(TvShowDetail)
admin.site.register(TvSeasonDetail)
admin.site.register(TvEpisodeDetail)

admin.site.register(Hls)
