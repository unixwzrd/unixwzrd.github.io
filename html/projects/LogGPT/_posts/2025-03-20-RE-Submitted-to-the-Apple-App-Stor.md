---
excerpt: "## UPDATE: [LogGPT Available Now on the Apple App Store Now!](https://apps.apple.com/us/app/loggpt/id6743342693)"
image: /assets/images/projects/LogGPT/LogGPT.png
layout: post
title: "Submitted (Again) to the Apple App Store"
date: "2025-03-20"
category: LogGPT
tags: [update, apple-app-store, resubmission, development]
published: true
redirect_from:
  - /projects/LogGPT/2025/03/20/RE-Submitted-to-the-Apple-App-Stor/
---
excerpt: "## UPDATE: [LogGPT Available Now on the Apple App Store Now!](https://apps.apple.com/us/app/loggpt/id6743342693)"

## UPDATE: [LogGPT Available Now on the Apple App Store Now!](https://apps.apple.com/us/app/loggpt/id6743342693)

I've finally got LogGPT approved by Apple and it is now available on the App Store.

## **The Long Road to Resubmission**

After what feels like an eternity, I've **finally** resubmitted the Safari extension to the Apple App Store. If you've ever dealt with Apple's review process, you know the frustration that comes with seemingly arbitrary rejections. And yes, that happened to me.

Initially, my app was rejected because the screenshot **looked too much like ChatGPT**. Well… yeah, because it's a Safari extension for ChatGPT! The extension simply lets you **download your ChatGPT conversation history** as a JSON file. Nothing more, nothing less.

## **Fixing the Issues & Jumping Through Hoops**

Getting this app back into Apple's review queue was not straightforward. Here's a **quick summary** of the madness:

- **Name Change**: The original name was identical to an existing **open-source MIT-licensed project** that provides a similar extension for Firefox and Chrome. Even though there was no Safari version, I decided to change the name to avoid confusion and conflicts.
- **The Icon Issue**: Apple rejected my submission because the icon **looked too much like ChatGPT's branding** and was used by other apps. I had to create a new icon to meet their guidelines.
- **Privacy Policy & Website Updates**: Since I changed the app's name, I also had to **update my privacy policy and make website changes** to reflect the new branding. More work I wasn't expecting.
- **New Apple Submission Hurdles**: Apple, true to its Steve Jobs-era philosophy of always having **"one more thing"**, kept introducing additional steps I had to complete. Just when I thought I was done, they added another requirement.
- **New `Info.plist` Property for Encryption**: Apple now requires a new **data encryption property** in `Info.plist`. I had to manually add it to comply with their updated security policies.
- **Chinese App Store Removal**: Since **ChatGPT is not allowed in China**, I had to **remove the app from the Chinese App Store** entirely. While users there could still purchase it, it wouldn't work anyway due to ChatGPT restrictions.
- **Regions Affected**: I assume that **Hong Kong and Shanghai** are also included in this restriction since they are part of China, though I wouldn't be surprised if an alternative ChatGPT-like service exists that the extension could work with.
- **Final Submission & Price**: After fixing these issues, I resubmitted the app with a price of **$1.99**-mostly to help offset the annual **Apple Developer Tax** ($99/year).

## **What This Extension Does**

To reiterate, this is a **simple, no-nonsense Safari extension** that lets you **export your ChatGPT conversations to JSON**. No ads, no tracking-just a clean way to download your chat logs for archival or content reuse. The file is saved in your **Downloads folder** using the conversation's title from OpenAI.

I personally use this extension for:
- Printing chat logs for reference.
- Extracting useful responses and formatting them into Markdown.
- Archiving conversations for future use.
- **Splitting** exported files and uploading them into a new ChatGPT session to **continue conversations seamlessly** (I'll be writing more about that technique soon).

![App Screenshot](/assets/images/projects/LogGPT/Screenshot%202025-03-19%20at%2016.56.28.png)

## **Used Just Today for AI Context Transfer**

An unexpected but incredibly useful scenario happened just this morning: we hit the **maximum conversation length** in ChatGPT. Instead of losing our discussion, we used this extension to **export the conversation to JSON**, split it into Markdown, and reload it into a fresh session-**seamlessly continuing** without missing a beat. This proves how useful it is for those working with AI over long discussions, ensuring no context is lost.

## **Extra Tools for Command Line Users**

If you're comfortable with the command line, check out my [VenvUtil](https://github.com/unixwzrd/venvutil) project. It includes tools to:
- Convert exported JSON files into **HTML or Markdown**.
- Format and clean up conversations for **printing**.
- Make archiving and retrieval **easier**.

## Feeling Adventurous?

If you want to build it yourself, you may download the source code as well as a pre-compiled binary of the app on my [GitHub Repository page](https://github.com/unixwzrd/LogGPT). There is a release there as well you may download and install it on your system.

## **Support My Work**

This extension is priced at **$1.99**, but if you'd like to support me further, you can do so here:
- [Patreon](https://patreon.com/unixwzrd)
- [Ko-Fi](https://ko-fi.com/unixwzrd)

This has been an exhausting process, and I'm just glad to finally have it back in Apple's queue. Fingers crossed for a smooth approval this time!

If you are looking fro someone to help you with a project, I am available for hire. I have a wide range of skills and can be a great asset to your team. My specialties are Unix/Linux/macOS system and database administration, automation, and application development and am rather adept with Python, Bash, and a variety of other tools.




