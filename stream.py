import gi
import cv2
import argparse
import numpy as np
import threading
import console_data_loader
import yaml
import time
from queue import Queue


# import required library like Gstreamer and GstreamerRtspServer
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

class StreamQueue():
    def __init__(self, **properties):
        self.last_frame = np.zeros((300, 300, 3), dtype=np.uint8)
        self.frame_queue = Queue()
    def recive_data(self):
        if not self.frame_queue.empty():
            self.last_frame = self.frame_queue.get()
        return self.last_frame
    def push_data(self, frame):
        if self.frame_queue.qsize() > 100:
            self.frame_queue.get()
        self.frame_queue.put(frame)
    def get_size(self):
        return self.frame_queue.qsize()

stream_queue = StreamQueue()

# Sensor Factory class which inherits the GstRtspServer base class and add
# properties to it.
class SensorFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, **properties):
        super(SensorFactory, self).__init__(**properties)
        self.number_frames = 0
        self.fps = opt.fps
        self.duration = 1 / self.fps * Gst.SECOND  # duration of a frame in nanoseconds
        self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                             'caps=video/x-raw,format=BGR,width={},height={},framerate={}/1 ' \
                             '! videoconvert ! video/x-raw,format=I420 ' \
                             '! x264enc speed-preset=ultrafast tune=zerolatency ' \
                             '! rtph264pay config-interval=1 name=pay0 pt=96' \
                             .format(opt.image_width, opt.image_height, self.fps)
    # method to capture the video feed from the camera and push it to the
    # streaming buffer.
    def on_need_data(self, src, length):
        frame = stream_queue.recive_data()
        frame = cv2.resize(frame, (opt.image_width, opt.image_height), \
            interpolation = cv2.INTER_LINEAR)
        data = frame.tostring()
        buf = Gst.Buffer.new_allocate(None, len(data), None)
        buf.fill(0, data)
        buf.duration = self.duration
        timestamp = self.number_frames * self.duration
        buf.pts = buf.dts = int(timestamp)
        buf.offset = timestamp
        self.number_frames += 1
        retval = src.emit('push-buffer', buf)
        if retval != Gst.FlowReturn.OK:
            print(retval)
    # attach the launch string to the override method
    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)
    
    # attaching the source element to the rtsp media
    def do_configure(self, rtsp_media):
        self.number_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)

# Rtsp server implementation where we attach the factory sensor with the stream uri
class GstServer(GstRtspServer.RTSPServer):
    def __init__(self, **properties):
        super(GstServer, self).__init__(**properties)
        self.factory = SensorFactory()
        self.factory.set_shared(True)
        self.set_service(str(opt.port))
        self.get_mount_points().add_factory(opt.stream_uri, self.factory)
        self.attach(None)

# getting the required information from the user 
parser = argparse.ArgumentParser()
parser.add_argument("--device_id", required=True, help="device id for the \
                video device or video file location")
parser.add_argument("--fps", required=True, help="fps of the camera", type = int)
parser.add_argument("--image_width", required=True, help="video frame width", type = int)
parser.add_argument("--image_height", required=True, help="video frame height", type = int)
parser.add_argument("--port", default=8554, help="port to stream video", type = int)
parser.add_argument("--stream_uri", default = "/video_stream", help="rtsp video stream uri")
opt = parser.parse_args()


try:
    opt.device_id = int(opt.device_id)
except ValueError:
    pass

with open('config/crowd_count_app.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)
    data_loader = console_data_loader.ConsoleDataLoader(
        config['data_source_settings']['console_data_settings'])
    
def start_rtsp_server():
    # initializing the threads and running the stream on loop.
    print("Start rtsp")
    GObject.threads_init()
    Gst.init(None)
    server = GstServer()
    loop = GObject.MainLoop()
    loop.run()

def get_data_inference_and_write_video():
    while (True):
        if data_loader.is_writing_video:
            ret = data_loader.get_inferences()
            if ret == "OK":
                # for time_, image_and_data in data_loader.match_image_infrence.items():
                    # cv_image, deserialize_data = image_and_data
                count = 0
                for object_pos in data_loader.deserialize_data:
                    if data_loader.deserialize_data[object_pos]['P'] < 0.55:
                        continue
                    x_top = data_loader.deserialize_data[object_pos]['X']
                    y_top = data_loader.deserialize_data[object_pos]['Y']
                    x_bot = data_loader.deserialize_data[object_pos]['x']
                    y_bot = data_loader.deserialize_data[object_pos]['y']
                    x_center_bot = (x_top + x_bot) / 2
                    if cv2.pointPolygonTest(data_loader.pts, (x_center_bot, y_bot), False):
                        count += 1
                    cv2.rectangle(data_loader.cv_mat_image, (x_top, y_top), (x_bot, y_bot), (0,0,255), 1)
                data_loader.cv_mat_image = cv2.putText(data_loader.cv_mat_image, "Count: " + str(count), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
                data_loader.cv_mat_image = cv2.polylines(data_loader.cv_mat_image, [data_loader.pts], True, (255, 0, 0), 1)
                # cv2.imwrite("test.jpg", data_loader.cv_mat_image)
                
                stream_queue.push_data(data_loader.cv_mat_image)
        data_loader.is_writing_video = False


if __name__ =="__main__":
    # creating thread
    t1 = threading.Thread(target=start_rtsp_server, args=())
    t1.start()
    t2 = threading.Thread(target=get_data_inference_and_write_video, args=())
    t2.start()
    while (True):
        start_time = round(time.time()*1000)
        ret = data_loader.get_images()
        done_time = round(time.time()*1000)
        print("Done after: ", done_time - start_time)

    t1.join()
    t2.join()