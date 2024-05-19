import os
import csv
import argparse
from datetime import datetime as dt
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import concatenate_videoclips, VideoFileClip, TextClip, CompositeVideoClip
from moviepy.editor import TextClip, ColorClip

def create_text_clip(text, duration=2, width=1280, height=720, fontsize=24, text_color='white', bg_color='black'):
    color_clip = ColorClip(size=(width, height), color=(0, 0, 0)).set_duration(duration).set_fps(24)
    
    # Create a text clip
    txt_clip = TextClip(text, fontsize=fontsize, color=text_color, font='Arial-Bold')
    txt_clip = txt_clip.set_pos('center').set_duration(duration)
    
    # Composite the text clip on the color clip
    final_clip = CompositeVideoClip([color_clip, txt_clip])
    
    return final_clip

def split_video(input_file, start_time, end_time, output_file):
    start_format = "%H:%M:%S" if len(start_time.split(":")) == 3 else "%M:%S"
    start = dt.strptime(start_time, start_format)
    end_format = "%H:%M:%S" if len(end_time.split(":")) == 3 else "%M:%S"
    print(end_time)
    end = dt.strptime(end_time, end_format)
    
    start_seconds = int((start - dt.strptime("00:00:00", "%H:%M:%S")).total_seconds())
    end_seconds = int((end - dt.strptime("00:00:00", "%H:%M:%S")).total_seconds())
    
    ffmpeg_extract_subclip(input_file, start_seconds, end_seconds, targetname=output_file)

def add_text_overlay(clip, text="TEST 0-0"):
    txt_clip = TextClip(text, fontsize=36, color='white', font='Arial-Bold')
    txt_clip = txt_clip.set_pos(('right', 'bottom')).set_duration(clip.duration)
    video = CompositeVideoClip([clip, txt_clip])
    return video

def process_videos_from_csv(csv_file, output_directory, final_output_file):
    clips = []

    time_text = ""

    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        home_score = 0
        away_score = 0

        for index, row in enumerate(reader):
            input_file = row['file path']
            start_time = row['start timestamp']
            end_time = row['end timestamp']
            score = row['smite scored?']

            if(input_file == "TEXT"):
                if(row['smite scored?']):
                    print(row['smite scored?'].split("-"))
                    home_str = row['smite scored?'].split("-")[0]
                    away_str = row['smite scored?'].split("-")[1]
                    home_score = int(home_str)
                    away_score = int(away_str)
                    last_score = str(home_score) + "-" + str(away_score)
                clips.append(create_text_clip(row["start timestamp"]))
                continue
                
            last_score = str(home_score) + "-" + str(away_score)

            if(score == "Y"):
                home_score += 1
            elif (score == "N"):
                away_score += 1
            #could be incomplete point, in that case, do not update score

            if not start_time or not end_time or start_time == "-" or end_time == "-":
                print(f"Skipping row {index+1} due to missing start or end timestamp")
                continue
            
            clip_name = f"clip_{index+1}.mp4"
            output_file = os.path.join(output_directory, clip_name)
            
            split_video(input_file, start_time, end_time, output_file)
            
            # Load the clip and add the text overlay
            clip = VideoFileClip(output_file)
            print(clip.w ,"x", clip.h)
            clip = add_text_overlay(clip, last_score)
            clips.append(clip)
    
    last_score = str(home_score) + "-" + str(away_score)
    clips.append(create_text_clip("Final Score: " + last_score))
    # Concatenate all clips
    if clips:
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(final_output_file, codec='libx264')
    else:
        print("No valid clips to concatenate.")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Cut and concatenate video clips based on CSV input.')
    parser.add_argument('csv_file', type=str, help='The CSV file containing video clip information.')
    parser.add_argument('output_directory', type=str, help='The directory to save the output clips.')
    parser.add_argument('final_output_file', type=str, help='The final concatenated video file name.')

    # Parse arguments
    args = parser.parse_args()

    # Ensure the output directory exists
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)
    
    # Process the videos
    process_videos_from_csv(args.csv_file, args.output_directory, args.final_output_file)

if __name__ == "__main__":
    main()
