---
title: Manage Threads — Staff & Admin User Guide
lang: en
---

# Manage Threads

Chat threads are individual conversation sessions between a user and the AI assistant. Each thread preserves the full message history and the assistant configuration that was active when the thread was created.

## Viewing Your Threads

All your chat threads are listed in the left sidebar of the main interface. The list shows:

- The name of the thread (automatically generated or manually renamed).
- The most recent message or activity timestamp.

Click on any thread to open it and review the conversation.

## Creating a New Thread

1. Click **New Chat** in the sidebar.
2. Select the assistant configuration to use from the dropdown.
3. Begin typing your message to start the thread.

A new thread is created automatically when you send your first message.

## Renaming a Thread

By default, threads are named based on the first message in the conversation. To rename a thread:

1. Hover over the thread name in the sidebar.
2. Click the **pencil** (edit) icon that appears.
3. Type the new name and press **Enter** to save.

Clear, descriptive names help you find specific conversations later.

## Deleting a Thread

To delete a thread:

1. Hover over the thread in the sidebar.
2. Click the **trash** (delete) icon that appears.
3. Confirm the deletion when prompted.

> **Warning:** Deleting a thread permanently removes the entire conversation history. This action cannot be undone.

## Thread and Assistant Configuration

Each thread is associated with an assistant configuration at the time of creation. The assistant configuration determines:

- The AI model used in the conversation.
- The tools available to the assistant.
- The system prompt guiding the assistant's behaviour.

If you need to use a different configuration, start a new chat thread. The configuration of an existing thread cannot be changed.

## Understanding Thread Metadata

Each thread stores the following metadata:

| Field | Description |
| ----- | ----------- |
| **Thread ID** | A unique identifier for the thread |
| **User ID** | The ID of the user who owns the thread |
| **Assistant ID** | The ID of the assistant configuration used |
| **Name** | The display name of the thread |
| **Last updated** | The date and time of the most recent message |

This information is used internally by the system and is not directly visible in the standard interface.

## Best Practices

- Rename threads with meaningful names to make them easy to find later.
- Use separate threads for distinct topics or tasks rather than mixing unrelated questions in one thread.
- Periodically delete old or unnecessary threads to keep the sidebar organised.
- If you are testing a new assistant configuration, create a dedicated test thread and delete it after testing.
