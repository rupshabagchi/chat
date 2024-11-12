export type Chat = { role: string; content: { response: string }; };

export const enum UserRoles {
    User = "user",
    Assistant = "assistant"
}
