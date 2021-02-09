from subprocess import Popen, PIPE
import json


def probe(filepath: str) -> dict:
    p = Popen(f'ffprobe -v quiet -print_format json -show_format -show_streams "{filepath}"', stderr=PIPE, stdout=PIPE)
    stdout, stderr = p.communicate()
    return json.loads(stdout)


if __name__ == "__main__":
    probe(R"Z:\Videos\TV Shows\Family Guy\Family.Guy.S06.1080p.Waifu2x\Family Guy - S06E04 - Stewie Kills Lois.mkv")
