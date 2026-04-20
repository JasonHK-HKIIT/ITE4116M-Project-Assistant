---
title: AI Chat — Staff & Admin User Guide
lang: en
---

# AI Chat

The AI Chat feature lets you have a natural-language conversation with the AI assistant. As a staff member or administrator, you can use the assistant to retrieve institutional information, test assistant configurations, and interact with MyPortal data.

## Starting a New Chat

1. Click **New Chat** in the left sidebar.
2. A new, empty chat thread opens on the right.
3. Select the assistant configuration you want to use from the dropdown at the top of the chat panel (if multiple configurations exist).
4. Type your message in the text box at the bottom of the screen.
5. Press **Enter** or click the **Send** button to submit your message.

## Using an Assistant Configuration

When starting or continuing a chat, you can associate it with a specific assistant configuration. Each configuration determines:

- Which AI model is used.
- Which tools are available (e.g. news, timetable, profile).
- The system prompt that sets the assistant's behaviour and tone.

To switch the configuration for a new chat:

1. Click **New Chat**.
2. From the **Assistant** dropdown, select the configuration you want to use.
3. Begin the conversation.

> **Note:** The assistant configuration cannot be changed for an existing chat thread. Start a new chat to use a different configuration.

## Example Questions

As a staff member, you may find the following types of questions useful:

- *"What is the latest news from VTC?"*
- *"Show me my profile."*
- *"What time is it now?"*
- *"Summarise the document I just uploaded."*

## Uploading Files

You can upload documents to give the assistant additional context. This is useful for reviewing reports, summarising materials, or answering questions based on uploaded content.

1. Click the **paper clip** (attachment) icon in the typing area.
2. Select one or more files from your device. Supported formats include PDF, DOCX, TXT, HTML, EPUB, ODT, and RTF.
3. The files are uploaded and indexed. Ask the assistant questions about the content.

> **Note:** Uploaded files are associated with the current chat thread and remain available for all subsequent messages in that thread.

## Chat History

All chat threads are saved automatically. You can:

- Return to any previous chat by clicking it in the sidebar.
- Rename a chat by clicking the pencil icon next to its name.
- Delete a chat by clicking the trash icon — this action cannot be undone.

## Keyboard Shortcuts

| Action | Shortcut |
| ------ | -------- |
| Send message | **Enter** |
| New line in message | **Shift + Enter** |

## Troubleshooting

**The assistant gives incorrect or irrelevant answers.**
Check the assistant configuration being used. The system prompt and selected tools determine the assistant's behaviour. See the [Configure Assistant Guide](./configure-assistant.md) for details on adjusting the configuration.

**The assistant cannot access MyPortal data.**
Ensure that the relevant MyPortal tools (News, Timetable, etc.) are enabled in the assistant configuration and that the `MYPORTAL_ENDPOINT` environment variable is correctly set.

**A chat thread is missing.**
Threads are stored per user. If a thread appears to be missing, check that you are logged in with the correct account.
