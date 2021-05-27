from subprocess import call, PIPE
from picamera import PiCamera, PiCameraCircularIO

file_h264 = '/home/pi/Desktop/test.h264'
file_mp4 = '/home/pi/Desktop/test.mp4'
slow_file_mp4 = '/home/pi/Desktop/test_slow.mp4'
video_length = 12

camera = PiCamera(rotation=180, resolution=(1640, 922), framerate=40)

if __name__ == "__main__":
    stream = PiCameraCircularIO(camera, seconds=video_length)
    camera.start_recording(stream, format='h264')

    camera.start_preview()

    while True:
        # Waiting for a key to be pressed
        camera.annotate_text = ''
        if input('Press a key to continue...') == 'q':
            break
        print('You pressed a key!')

        # Saving buffer to file
        camera.wait_recording(2)
        stream.copy_to(file_h264)

        # Converting saved buffer into .mp4 files
        camera.annotate_text = 'GET READY FOR REPLAY'
        # Normal speed
        call([f'ffmpeg -r 40 -i {file_h264} -c copy -y {file_mp4}'], shell=True)
        # Slow (1/2) speed
        call([f'ffmpeg -r 20 -i {file_h264} -c copy -y {slow_file_mp4}'], shell=True)
        print('\r\nRasp_Pi => Video Converted! \r\n')

        # Play normal speed
        # Stop camera preview
        camera.stop_preview()
        # Start replay (normal speed)
        call(['omxplayer', file_mp4], stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
        # Start replay (slow motion)xw
        call(['omxplayer', slow_file_mp4], stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
        camera.start_preview()

    camera.close()
