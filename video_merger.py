from moviepy import VideoFileClip, concatenate_videoclips


def merge_videos(video1_path, video2_path, output_path):
    """
    Merge two video files by concatenating them.

    Parameters:
    video1_path (str): Path to the first video file
    video2_path (str): Path to the second video file
    output_path (str): Path where the merged video will be saved
    """
    try:
        # Load the video clips
        clip1 = VideoFileClip(video1_path)
        clip2 = VideoFileClip(video2_path)

        # Concatenate the clips
        final_clip = concatenate_videoclips([clip1, clip2])

        # Write the merged video to file
        final_clip.write_videofile(output_path)

        # Close the clips to free up system resources
        clip1.close()
        clip2.close()
        final_clip.close()

        print(f"Successfully merged videos to: {output_path}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Example usage
if __name__ == "__main__":
    merge_videos(
        video1_path="C:/Users/avet_/Videos/video1.mp4",
        video2_path="C:/Users/avet_/Videos/video2.mp4",
        output_path="C:/Users/avet_/Videos/video.mp4"
    )
