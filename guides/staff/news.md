---
title: News & Announcements — Staff & Admin User Guide
lang: en
---

# News & Announcements

The News & Announcements feature provides access to the latest news and official announcements from the Vocational Training Council (VTC) and its member institutions, including HKIIT. Staff and administrators can use this feature to stay informed and to verify the news content that students see.

## Searching for News

In the chat, ask a question such as:

- *"What is the latest news from VTC?"*
- *"Are there any recent announcements about staff development?"*
- *"Show me news about the upcoming academic year."*
- *"Any updates about the new campus facilities?"*

The assistant will search MyPortal for the most relevant articles matching your query and display them in the chat.

## Understanding the Results

Each news item shows:

| Field | Description |
| ----- | ----------- |
| **Title** | The headline of the news article |
| **Date** | The date the article was published |
| **Content** | A summary or the full body of the article |
| **Link** | A link to read the full article on MyPortal |

### Example Response

> **VTC Staff Development Programme 2024/25 (2024-09-01)**
>
> The VTC is pleased to announce a series of professional development workshops for teaching and non-teaching staff. Courses will be offered throughout the academic year on topics including pedagogy, digital literacy, and leadership…
>
> https://portal.vtc.edu.hk/news/staff-development-2024

## Following a News Link

If an article includes a link, click or tap the URL to open the full article in your browser. You will be taken to the relevant page on MyPortal or the VTC website. Ensure you are logged in to MyPortal to access staff-only content.

## Configuring the News Tool

The News Articles tool can be included in an assistant configuration to allow users to search for news. See the [Configure Assistant Guide](./configure-assistant.md) for details on enabling this tool.

Administrators can also control the maximum number of articles returned per query by setting the `MYPORTAL_NEWS_LIMIT` environment variable on the server (default: 5, maximum: 20). This is a system-wide setting that applies to all assistant configurations; changing it requires access to the server environment and a service restart.

## Frequently Asked Questions

**How recent is the news?**
News articles are fetched in real time from MyPortal whenever you ask. The results reflect the most recently published content available.

**How many articles are shown?**
By default, the assistant shows up to 5 articles per search. This limit can be adjusted via the `MYPORTAL_NEWS_LIMIT` environment variable, or by asking for more in the chat (e.g. *"Give me 10 news articles about scholarships"*).

**Can I search news by category or date?**
Currently, the news tool searches by keyword. Include date-related or category-related terms in your query to narrow down results (e.g. *"news about scholarships in September 2024"*).

**I cannot see the full article. What should I do?**
Follow the link provided in the assistant's response to read the full article on MyPortal. Make sure you are logged in to MyPortal to access all content.
