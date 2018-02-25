#! /bin/bash

pulseaudio-monitor() {
    echo $(pactl list | grep -A2 '^Source #'  | grep 'Name: .*\.monitor$' | awk '{print $NF}' | tail -n1)
}

desktop-capture-ff() {

    local RESOLUTION="640x360"
    local QUAL="fast"
    local TUNE="animation"
    local OUTPUT="$(dirname "$0")/../media/capture.mov"
    local OFFSET="0,0"
    local FPS="30"

    if [[ -f "$OUTPUT" ]]; then
        rm "$OUTPUT"
    fi

    # avconv \
    #         -f alsa -i hw:0 \
    #         -f x11grab -r "$FPS" \
    #         -i :0.0+"$OFFSET" \
    #         -s "$RESOLUTION" \
    #         -vcodec libx264 -crf 38 \
    #         -preset "$QUAL" -tune "$TUNE" \
    #         -threads 2 \
    #         -an \
    #         "$OUTPUT"
            
            # -profile:v baseline -level 30 \
            # -acodec copy \
            # -acodec libmp3lame -ar 44100 \

    ffmpeg -y -f alsa \
            -i hw:0 \
            -f x11grab -framerate 30 \
            -i :0.0+0,0 \
            -video_size 1024×576 \
            -acodec ac3 -ac 1 \
            -vcodec libx264 \
            -preset fast \
            -threads 0 \
            -f matroska \
            "$OUTPUT"
            
}

echo $(dirname "$0")
desktop-capture-ff
