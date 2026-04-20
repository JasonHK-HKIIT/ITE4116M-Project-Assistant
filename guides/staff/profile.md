---
title: My Profile — Staff & Admin User Guide
lang: en
---

# My Profile

The Profile feature lets you view your personal account details as stored in MyPortal. Staff and administrators can retrieve this information at any time by asking the AI assistant.

## Viewing Your Profile

In the chat, ask a question such as:

- *"Show me my profile."*
- *"What is my username?"*
- *"What is my role in the system?"*

The assistant will fetch your profile from MyPortal and display the details in the chat.

## Profile Information

Your profile includes account information and, if applicable, student details.

### Account Information

| Field | Description |
| ----- | ----------- |
| **Name** | Your full name (family name and given name) |
| **Username** | Your MyPortal login username |
| **Role** | Your account role (e.g. staff, admin) |
| **Chinese name** | Your Chinese name, if provided |
| **Avatar** | A link to your profile picture, if set |

### Student Details

If your MyPortal account also has a student record, additional details will be shown:

| Field | Description |
| ----- | ----------- |
| **Institute** | The institute you are associated with |
| **Campus** | Your assigned campus |
| **Current class** | Your current class code and academic year |
| **Programmes** | The academic programme(s) linked to your account |

### Example Response

> **Your profile:**
> - Name: Lee Siu Ming
> - Username: t98765432
> - Role: staff
>
> No student record is available for this account.

## Configuring the Profile Tool

The User Profile tool can be included in an assistant configuration to allow users to retrieve their own profile. Each instance of the tool requires a `user_id` to be specified in the tool configuration.

To configure the tool:

1. Open the [Configure Assistant](./configure-assistant.md) interface.
2. Enable the **User Profile** tool.
3. Enter the MyPortal user ID in the `user_id` field of the tool configuration.
4. Optionally, set the `locale` field to control the language of the profile data (e.g. `en` for English, `zh-HK` for Traditional Chinese).

See the [Configure Assistant Guide](./configure-assistant.md) for full instructions.

## Updating Your Profile

Your profile information is managed in MyPortal. If any details are incorrect or need to be updated, please:

1. Log in to MyPortal directly.
2. Navigate to your account or profile settings.
3. Update the relevant fields and save.

For changes that require administrative action (such as name corrections), contact your HR department or system administrator.

## Frequently Asked Questions

**My role is shown incorrectly. What should I do?**
Role assignments are managed in MyPortal by system administrators. Contact your administrator to correct your role.

**Why is my Chinese name not shown?**
The Chinese name field is optional. If it has not been entered in MyPortal, it will not appear in the profile output.

**Is my personal data secure?**
Yes. Your profile is retrieved directly from MyPortal using your authenticated session and displayed only in your personal chat. The data is not shared with other users.
