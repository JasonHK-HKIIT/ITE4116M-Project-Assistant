---
title: Configure Assistant — Staff & Admin User Guide
lang: en
---

# Configure Assistant

The Configure Assistant feature allows staff and administrators to create and customise AI assistant profiles. Each assistant configuration defines the AI model, the tools available, the system prompt, and the visibility of the assistant.

## Opening the Configuration Interface

1. Click the **Configure** (or settings) button in the top navigation area.
2. The configuration panel opens, showing the list of existing assistant configurations on the left and the editor on the right.

## Creating a New Assistant Configuration

1. Click **New Assistant** (or the **+** button) in the configuration list.
2. Fill in the fields described below.
3. Click **Save** to create the assistant.

## Configuration Fields

### Name

A human-readable name for the assistant configuration. This name appears in the assistant dropdown when starting a new chat.

**Example:** `Student Support Assistant`

### System Prompt

The system prompt is a set of instructions given to the AI at the beginning of every conversation. It defines the assistant's role, tone, and behaviour.

**Tips for writing a good system prompt:**

- Be clear and specific about the assistant's purpose.
- Define the audience (e.g. *"You are a helpful assistant for HKIIT students."*).
- Specify any restrictions (e.g. *"Only answer questions related to academic matters."*).
- You can instruct the assistant to use a specific language.

**Example:**

```
You are a helpful academic assistant for students at HKIIT.
You have access to the student's timetable, news, and activity information.
Always respond in polite, clear English.
```

### Tools

Tools extend the assistant's capabilities by allowing it to fetch real-time information from MyPortal and external sources. Select the tools that are appropriate for the assistant's purpose.

#### MyPortal Tools

| Tool | Description |
| ---- | ----------- |
| **News Articles** | Retrieve the latest VTC and institutional news by keyword |
| **Student Activities** | Search for active and upcoming campus activities |
| **User Profile** | Retrieve the configured user's profile from MyPortal |
| **Timetable** | Retrieve the configured user's timetable and calendar events |
| **Current Time** | Return the current date and time in Hong Kong Time |

> **Note:** The **User Profile** and **Timetable** tools require a `user_id` to be specified in their tool configuration. Enter the MyPortal user ID of the student or staff member whose data the assistant should access. You should only configure these tools with the `user_id` of users whose data you are authorised to access. Configuring these tools with another user's ID without appropriate authorisation may violate institutional privacy policies. In most deployments, these tools are configured with the ID of the authenticated user only.

#### Other Tools

| Tool | Description |
| ---- | ----------- |
| **DuckDuckGo Search** | Search the web using DuckDuckGo |
| **Arxiv** | Search academic papers on Arxiv |
| **Wikipedia** | Search Wikipedia |
| **DALL-E** | Generate images from text descriptions |
| **Retrieval** | Search documents uploaded by the user within the chat |

### Visibility

- **Private** — The assistant is visible only to you.
- **Public** — The assistant is visible to all users of the platform.

Set an assistant to **Public** only if it is intended for broad use by students or other staff members.

## Editing an Existing Configuration

1. Click on the assistant configuration you want to edit in the left panel.
2. Modify the fields as needed.
3. Click **Save** to apply the changes.

> **Note:** Changes to an assistant configuration affect all new chats that use that configuration. Existing chat threads retain the configuration that was active when they were created.

## Deleting a Configuration

1. Select the configuration in the left panel.
2. Click the **Delete** button.
3. Confirm the deletion when prompted.

> **Warning:** Deleting an assistant configuration cannot be undone. Existing chat threads that used the configuration will no longer have access to it.

## Best Practices

- Create separate configurations for different audiences (e.g. one for students, one for staff).
- Keep system prompts focused and concise.
- Only enable tools that are needed for the assistant's purpose to reduce irrelevant responses.
- Test a new configuration by starting a chat and asking sample questions before making it public.
