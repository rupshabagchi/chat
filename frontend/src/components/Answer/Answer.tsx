import { Stack } from "@fluentui/react";
import styles from "./Answer.module.css";
import ReactMarkdown from "react-markdown";
import { Chat } from "../../types/types"

interface Props {
    response: Chat;
    isSelected?: boolean;

}

export const Answer = ({
    response,
    isSelected,
}: Props) => {


    return (
        <Stack className={`${styles.answerContainer} ${isSelected && styles.selected}`} verticalAlign="space-between">
            <Stack.Item grow>
                <div className={styles.replacedText}>
                    <ReactMarkdown>{response.content.response}</ReactMarkdown>
                </div>
            </Stack.Item>
        </Stack>
    );
};
