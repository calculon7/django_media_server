from typing import List
from abc import ABC, abstractmethod
from ..models import MediaLibrary, LibraryType

file_extensions = {
    'video': [
        ".webm",
        ".mp4",
        ".mpg",
        ".mp2",
        ".mpeg",
        ".mpe",
        ".mpv",
        ".mkv",
        ".ts",
        ".ogg",
        ".m4p",
        ".m4v",
        ".avi",
        ".wmv",
        ".qt",
        ".flv",
        ".swf",
        ".avchd",
        ".3g2",
        ".3gp",
        ".amv",
        ".asf",
        ".f4v",
        ".f4p",
        ".f4a",
        ".f4b",
        ".gif",
        ".m2v",
        ".mts",
        ".m2ts",
        ".ogv",
        ".vob", 
    ],
    'audio': [],
    'subtitle': [],
}


class MediaScanner(ABC):
    library_id: int
    paths: List[str]
    verbose = False
    
    @abstractmethod
    def run(self):
        pass

    @staticmethod
    def create(media_library: MediaLibrary):
        scanner = None

        

        if media_library.library_type == LibraryType.TV:
            from ..media_scanners.TvScanner import TvScanner
            scanner = TvScanner()

        elif media_library.library_type == LibraryType.MOVIE:
            from ..media_scanners.MovieScanner import MovieScanner
            scanner = MovieScanner()

        else:
            from ..media_scanners.OtherVideoScanner import OtherVideoScanner
            scanner = OtherVideoScanner()

        scanner.paths = media_library.paths
        scanner.library_id = media_library.id  # type: ignore

        return scanner
