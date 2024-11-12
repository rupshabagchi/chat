import { useState } from 'react';
import { DefaultButton, TextField, Stack, StackItem } from "@fluentui/react";
import { UserChatMessage } from '../UserChatMsg/UserChatMsg';
import { Answer } from '../Answer/Answer';
import { Chat, UserRoles } from "../../types/types"
import styles from "./Chatbot.module.css";


const assistantQuestion = "How may I help you?";
const assistantInitialMessage = [
    { role: UserRoles.Assistant, content: { response: assistantQuestion } }
];

const Chatbot = () => {
    const [message, setMessage] = useState<string>('');
    const [chatHistory, setChatHistory] = useState<Chat[]>(assistantInitialMessage);
    const [loading, setLoading] = useState<boolean>(false);

    const handleSendMessage = async () => {
        if (!message.trim()) return;

        setLoading(true);

        try {
            const response = await fetch('http://localhost:5000/chat', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();

            // Add user and bot messages to the chat history
            setChatHistory([
                ...chatHistory,
                { role: UserRoles.User, content: { response: message } },
                { role: UserRoles.Assistant, content: data },
            ]);
        } catch (error) {
            console.error("Error is the following:", error);
        } finally {
            setMessage('');
            setLoading(false);
        }
    };

    return (
        <div className="chatbot">
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

            <Stack horizontal>
                <StackItem>
                    <TextField
                        value={message}
                        onChange={(e) => setMessage((e.target as HTMLInputElement).value)}
                        placeholder="Type a message..."
                    />
                </StackItem>
                <StackItem>
                    <DefaultButton onClick={handleSendMessage} disabled={loading}>
                        {loading ? 'Sending...' : 'Send'}
                    </DefaultButton>
                </StackItem>
            </Stack>
        </div>
    );
};

export default Chatbot;
