import subprocess


def convert_480p(source):
    target = source + '_480p.mp4'
    cmd = (
        'ffmpeg -i "./{src}" -s hd480 -c:v libx264 '
        '-crf 23 -c:a aac -strict -2 "./{tgt}"'
    ).format(src=source, tgt=target)
    subprocess.run(cmd)


def convert_720p(source):
    target = source + '_720p.mp4'
    cmd = (
        'ffmpeg -i "./{src}" -s hd720 -c:v libx264 '
        '-crf 23 -c:a aac -strict -2 "./{tgt}"'
    ).format(src=source, tgt=target)
    subprocess.run(cmd)


def convert_1080p(source):
    target = source + '_1080p.mp4'
    cmd = (
        'ffmpeg -i "./{src}" -s hd1080 -c:v libx264 '
        '-crf 23 -c:a aac -strict -2 "./{tgt}"'
    ).format(src=source, tgt=target)
    subprocess.run(cmd)
