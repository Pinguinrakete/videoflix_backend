import subprocess


def convert_480p(source):
    target = source + '_480p.mp4'
    cmd = (
        'ffmpeg -i "./{src}" -s hd1080 -c:v libx264 '
        '-crf 23 -c:a aac -strict -2 "./{tgt}"'
    ).format(src=source, tgt=target)
    subprocess.run(cmd)
