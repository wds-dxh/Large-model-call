import ffmpeg   # pip install ffmpeg-python

def push_stream(input_file, output_url):
    try:
        (
            ffmpeg
            .input(input_file)
            .output(output_url,
                    format='flv',  # 使用flv格式推流
                    vcodec='libx264',
                    acodec='aac',
                    preset='ultrafast',
                    tune='zerolatency',
                    pix_fmt='yuv420p')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print('ffmpeg error:', e.stderr.decode())

if __name__ == "__main__":
    input_file = './test.mkv' # 输入视频文件e
    output_url = 'rtmp://your_rtmp_server/live/stream_key'  # 目标RTMP服务器URL和流密钥

    push_stream(input_file, output_url)
