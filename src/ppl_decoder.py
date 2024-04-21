"""
author: anhnt
update: 20230508
"""

import traceback

from converter import convert_unixtime_to_datetime
from smart_camera_human_schema.upload_data import UploadData


def decode_od_result(ori_buf, device_id):
    """
    This function decodes and extracts information from a binary buffer and populates a
    dictionary with the extracted data.

    :param buf: A dictionary containing inferences for a video stream, including information
    about people detected in the stream
    :param gender_head_age: It is a dictionary that maps gender and head age codes to their
    corresponding values. This is used to decode the gender and age information of the people
    detected in the input buffer
    :return: the modified `buf` dictionary with additional information about dead tracks, including
    track ID, timestamp, watch start time, watch time, age, gender, status, customer ID, store ID,
    device ID, detail watch time, and maximum watch duration.
    """
    raw = []
    raw_all = []
    decode_labels = ["male", "female", "unknown"]
    error_count = 0
    try:
        # Deserialize
        ppl_out = UploadData.GetRootAsUploadData(ori_buf, 0)
        num_dead_tracks = ppl_out.ListDeadTrackLength()
    except:
        pass

    # Deserialize
    for i in range(num_dead_tracks):
        try:
            dead_track_data = ppl_out.ListDeadTrack(i)
            timestamp = dead_track_data.Timestamp()
            timestamp = convert_unixtime_to_datetime(timestamp)
            watch_start_time = dead_track_data.WatchStartTime()
            watch_start_time = convert_unixtime_to_datetime(watch_start_time)
            detail_watch_time_length = dead_track_data.DetailWatchTimeLength()
            detail_watch_time = []
            max_watch_time = 0
            direction_yaw = 0
            direction_pitch = 0
            _watch_time = 0
            for j in range(detail_watch_time_length):
                detail_watch_time_pair_data = dead_track_data.DetailWatchTime(j)
                detail_watch_time_pair = {}
                detail_watch_time_pair["start_time"] = (
                    detail_watch_time_pair_data.Start()
                )
                detail_watch_time_pair["end_time"] = detail_watch_time_pair_data.End()
                detail_watch_time.append(detail_watch_time_pair)
                watch_time = (
                    detail_watch_time_pair["end_time"]
                    - detail_watch_time_pair["start_time"]
                )

                max_watch_time = max(max_watch_time, watch_time)
                _watch_time += watch_time
            if dead_track_data.DirectionYaw() >= 18:
                direction_yaw = 999
            else:
                direction_yaw = (dead_track_data.DirectionYaw() - 9) * 10
            if dead_track_data.DirectionPitch() >= 18:
                direction_pitch = 999
            else:
                direction_pitch = (dead_track_data.DirectionPitch() - 9) * 10

            first_bbox_data = dead_track_data.BboxCoords().First()
            last_bbox_data = dead_track_data.BboxCoords().Last()
            highest_bbox_data = dead_track_data.BboxCoords().Conf()

            raw.append(
                [
                    timestamp,
                    dead_track_data.TrackId().decode(),
                    watch_start_time,
                    dead_track_data.Age(),
                    dead_track_data.StayTime(),
                    decode_labels[dead_track_data.Gender()],
                    direction_yaw,
                    direction_pitch,
                    ppl_out.CustomerId().decode(),
                    ppl_out.StoreId().decode(),
                    device_id,
                    _watch_time,
                    len(detail_watch_time),
                    max_watch_time,
                    "counted",
                    first_bbox_data.Top(),
                    first_bbox_data.Left(),
                    first_bbox_data.Width(),
                    first_bbox_data.Height(),
                    last_bbox_data.Top(),
                    last_bbox_data.Left(),
                    last_bbox_data.Width(),
                    last_bbox_data.Height(),
                    highest_bbox_data.Top(),
                    highest_bbox_data.Left(),
                    highest_bbox_data.Width(),
                    highest_bbox_data.Height(),
                ]
            )
            raw_all.append(
                {
                    "age": dead_track_data.Age(),
                    "device_id": device_id,
                    "stay_time": dead_track_data.StayTime(),
                    "direction_pitch": direction_pitch,
                    "direction_yaw": direction_yaw,
                    "customer_id": ppl_out.CustomerId().decode(),
                    "detail_watch_time": detail_watch_time,
                    "gender": decode_labels[dead_track_data.Gender()],
                    "max_watch_duration": max_watch_time,
                    "status": "counted",
                    "store_id": ppl_out.StoreId().decode(),
                    "timestamp": timestamp,
                    "tracking_id": dead_track_data.TrackId().decode(),
                    "watch_start_time": watch_start_time,
                    "watch_time": _watch_time,
                    "first": parse_bbox(first_bbox_data),
                    "last": parse_bbox(last_bbox_data),
                    "conf": parse_bbox(highest_bbox_data),
                }
            )
        except Exception as e:
            error_count += 1
            continue

    return raw_all


def parse_bbox(obj):
    left = obj.Left()
    top = obj.Top()
    width = obj.Width()
    height = obj.Height()
    return [left, top, width, height]
