## Setup

```
pip install requirements.txt
brew update && brew install imagemagick
```

## How to Use

To get a blank csv in the correct format:
`python format.py [-h] abs_path csv_filename`

Where abs_path is a path to the folder with all your clips and csv_filename is a path to a output csv.

Fill in the CSV with start and end times and who scored.


To edit a video:
`python clip.py csv_file output_directory final_output_file`

where csv_file is your edited csv. output_directory is a temporary directory for clips and final_output_file is a mp4 filename for the final video.


## Features

- if a score occured in clip, notate Y/N in smite scored? column
    - if no score occurs, place any other string in column (note incomplete)
- if a point is missed, add a TEXT line and indicate corrected score in "smite-scored" column in `<smite score>-<opscore>` format
- if you wish to insert a blank text screen type TEXT in the file column, the text you wish to appear in "start timestamp"
- the final score and running score are automatically added to the video.
- chop off the front/end of any clip by typing in "start timestamp" or endtimestamp.

