<?php
if(isset($_POST['url'])){
    $url = $_POST['url'];
    $format = $_POST['format'];
    $resolution = $_POST['resolution'];
    $audio_bitrate = $_POST['audio-bitrate'];
    $video_bitrate = $_POST['video-bitrate'];
    $subtitles = isset($_POST['subtitles']) ? true : false;
    $thumbnail = isset($_POST['thumbnail']) ? true : false;
    
    $command = "youtube-dl -f 'bestvideo[height<=$resolution][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=$resolution][ext=webm]+bestaudio[ext=webm]/best[height<=$resolution]' --merge-output-format $format --audio-quality $audio_bitrate --video-bitrate $video_bitrate ";
    
    if($subtitles){
        $command .= "--all-subs ";
    }
    
    if($thumbnail){
        $command .= "--write-thumbnail ";
    }
    
    $command .= escapeshellarg($url);
    
    header("Content-Description: File Transfer");
    header("Content-Type: application/octet-stream");
    header("Content-Disposition: attachment; filename=\"video.$format\"");
    
    passthru($command);
    exit();
}
?>
