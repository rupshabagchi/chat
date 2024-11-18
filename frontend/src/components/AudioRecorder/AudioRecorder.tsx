import React, { useState, useRef } from "react";
import { DefaultButton } from "@fluentui/react";

interface AudioRecorderProps {
    onRecordingComplete: (audioURL: string) => void;
}

const AudioRecorder: React.FC<AudioRecorderProps> = ({ onRecordingComplete }) => {
    const [recording, setRecording] = useState(false);
    const [audioURL, setAudioURL] = useState<string | null>(null);
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const audioChunks = useRef<Blob[]>([]);

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.current.push(event.data);
                }
            };

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks.current, { type: "audio/wav" });
                const url = URL.createObjectURL(audioBlob);
                setAudioURL(url);
                onRecordingComplete(url); // Pass the audio URL to the parent component
                audioChunks.current = []; // Reset chunks for the next recording
            };

            mediaRecorderRef.current = mediaRecorder;
            mediaRecorder.start();
            setRecording(true);
        } catch (error) {
            console.error("Error accessing microphone:", error);
        }
    };

    const stopRecording = () => {
        mediaRecorderRef.current?.stop();
        setRecording(false);
    };

    return (
        <>
            <DefaultButton
                onClick={startRecording}
                disabled={recording}
                style={{
                    backgroundColor: recording ? "#ddd" : "#4CAF50",
                    color: "white",
                    margin: "0 10px 0 0"
                }}
            >
                Start Recording
            </DefaultButton>
            <DefaultButton
                onClick={stopRecording}
                disabled={!recording}
                style={{
                    backgroundColor: recording ? "#f44336" : "#ddd",
                    color: "white",
                    margin: "0 10px 0 0"
                }}
            >
                Stop Recording
            </DefaultButton>

            {audioURL && (
                <div style={{ marginTop: "20px"}}>
                    <h4>Recorded Audio:</h4>
                    <audio controls src={audioURL}></audio>
                </div>
            )}
        </>
    );
};

export default AudioRecorder;
