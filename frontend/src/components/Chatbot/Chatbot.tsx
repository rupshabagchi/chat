import { useState, useEffect } from 'react';
import { io, Socket } from 'socket.io-client';
import { TextField, Stack, StackItem, DefaultButton, Toggle } from "@fluentui/react";
import { UserChatMessage } from '../UserChatMsg/UserChatMsg';
import { Answer } from '../Answer/Answer';
import AudioRecorder from '../AudioRecorder/AudioRecorder';
import { Chat, UserRoles } from "../../types/types"
import styles from "./Chatbot.module.css";


const assistantQuestion = "How may I help you?";
const assistantInitialMessage = [
    { role: UserRoles.Assistant, content: { response: assistantQuestion } }
];

const sleep = (ms: number) => new Promise(r => setTimeout(r, ms));

const socket: Socket = io('http://localhost:5000');

const Chatbot = () => {
    const [message, setMessage] = useState<string>('');
    // const [messages, setMessages] = useState<string[]>([]);
    const [chatHistory, setChatHistory] = useState<Chat[]>(assistantInitialMessage);
    const [loading, setLoading] = useState<boolean>(true);

    const [transcription, setTranscription] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [enableGenAI, setEnableGenAI] = useState<boolean>(false)


    useEffect(() => {
        // Listen for messages from the server
        socket.on('receive_message', () => {
            //setMessages((prevMessages) => [...prevMessages, newMessage]);
        });

        // Cleanup the socket connection on unmount
        return () => {
            socket.disconnect();
        };
    }, []);

    const sendHardCodedMessage = () => {
        if (message.trim()) {
            socket.emit('send_message', message);
            setMessage('');
        }
    };

    const handleRecordingComplete = async (audioURL: string) => {
        setLoading(true);
        setError(null);
        setTranscription(null);

        try {
            // Fetch the audio file as a Blob
            const response = await fetch(audioURL);
            await sleep(2000);
            const audioBlob = await response.blob();

            // Prepare form data
            const formData = new FormData();
            formData.append("audio", audioBlob);

            // Send the Blob to API
            await fetch("http://localhost:5000/speech-to-text", {
                method: "POST",
                body: formData,
            }).then(apiResponse => apiResponse.json())
                .then(data => setTranscription(data.text));
        } catch (err) {
            console.error("Error calling speech-to-text API:", err);
            setError("Failed to transcribe the audio. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    const handleSendMessage = async () => {
        if (!message.trim()) return;
        if (enableGenAI) {
            try {
                await fetch('http://localhost:5000/chat-openai', {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ message })
                }).then((response) => response.json())
                    .then((data) => {
                        // Add user and bot messages to the chat history
                        setChatHistory([
                            ...chatHistory,
                            { role: UserRoles.User, content: { response: message } },
                            { role: UserRoles.Assistant, content: data },
                        ]);
                    });
            } catch (error) {
                console.error("Error is the following:", error);
            } finally {
                setMessage('');
                setLoading(false);
            }
        } else {
            sendHardCodedMessage();
        }
    };

    return (
        <div className="chatbot" style={{ marginLeft: "30px"}}>
            <div className="chat-history">
                {chatHistory.map((answer, index) => (
                    <div key={index}>
                        {answer.role === "user" ? (
                            <UserChatMessage message={answer.content?.response} />
                        ) : (
                            <div className={styles.chatMessageGpt}>
                                <Answer
                                    key={index}
                                    response={answer}
                                    isSelected={false} />
                            </div>
                        )}
                    </div>
                ))}
            </div>

            <Stack horizontal style={{ marginLeft: "30px" }}>
                <StackItem>
                    <TextField
                        value={message}
                        onChange={(e) => setMessage((e.target as HTMLInputElement).value)}
                        placeholder="Type a message..."
                        style={{ width: "500px" }}
                    />
                </StackItem>
                <StackItem>
                    <DefaultButton onClick={handleSendMessage} style={{ margin: "0 10px 0 10px" }}>
                        Send
                    </DefaultButton>
                </StackItem>
                <StackItem style={{ marginLeft: "20px"}}>
                    <Toggle label="Enable genAI chat" inlineLabel defaultChecked onText="On" offText="Off" onChange={(e: React.MouseEvent<HTMLElement>, checked?: boolean) => setEnableGenAI(checked ?? false)} />
                </StackItem>
            </Stack>
            <Stack style={{ marginLeft: "30px", marginTop: "40px" }}>
                <StackItem>
                    <AudioRecorder onRecordingComplete={handleRecordingComplete} />
                    {loading && <p>Processing your audio...</p>}
                    {error && <p style={{ color: "red" }}>{error}</p>}
                    {transcription && (
                        <div>
                            <h3>Transcription:</h3>
                            <p>{transcription}</p>
                        </div>
                    )}
                </StackItem>
            </Stack>
        </div>
    );
};

export default Chatbot;
