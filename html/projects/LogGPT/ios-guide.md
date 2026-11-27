---
layout: page
title: "LogGPT User Guide for iPhone and iPad"
permalink: /projects/LogGPT/ios-guide/
hide_banner_image: true
toc: true
support_project: LogGPT
image: /assets/images/projects/LogGPT/LogGPT-Plus.png
excerpt: "Enable LogGPT in Safari, export ChatGPT conversations, and save JSON files or Plus archives to Files on iPhone and iPad."
---

LogGPT saves the ChatGPT conversation you have open in Safari. **Basic** saves a `.json` file. **LogGPT Plus** is a one-time upgrade that can save the conversation and selected images, charts, attachments, and web thumbnails in a ZIP-based `.lgpt` archive. Both save to the Files app.

[LogGPT overview]({{ '/projects/LogGPT/' | relative_url }}) · [Get LogGPT support on GitHub](https://github.com/unixwzrd/LogGPT/issues/new/choose)

This guide applies to iOS and iPadOS 16 or later. The screenshots show iOS and iPadOS 27.2. Open the iPhone screenshots under each step to see where Safari and Files place the controls. Tap any screenshot to enlarge it.

## Enable LogGPT in Safari

1. Open the **LogGPT** app after installing it. Its Safari section shows the setup steps.
2. Open `chatgpt.com` in Safari and sign in to ChatGPT. On iPhone, tap the page menu beside the address bar and scroll to **Manage Extensions**. On iPad, use the puzzle-piece button or the page menu. Turn on **LogGPT**. You can also enable it in **Settings ' Apps ' Safari ' Extensions ' LogGPT**. On older versions, start at **Settings ' Safari ' Extensions**.
3. Open a conversation. Tap **LogGPT** in Safari's extensions menu. If Safari asks for access to `chatgpt.com`, choose **Allow for One Day** for a temporary grant or **Always Allow** to keep it enabled on that site.
4. Reload the conversation so the extension can add its download button.

<div class="loggpt-guide-screenshots">
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/01-first-launch-basic.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/01-first-launch-basic.webp' | relative_url }}" width="1640" height="2360" loading="lazy" decoding="async" alt="LogGPT's first-launch setup instructions and Plus upgrade offer."></a>
    <figcaption>LogGPT's first-launch setup instructions and Plus upgrade offer.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/02-safari-extensions-menu.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/02-safari-extensions-menu.webp' | relative_url }}" width="1640" height="2360" loading="lazy" decoding="async" alt="Turn on LogGPT in Safari's Manage Extensions sheet."></a>
    <figcaption>Turn on LogGPT in Safari's Manage Extensions sheet.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/05-chatgpt-site-permission.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/05-chatgpt-site-permission.webp' | relative_url }}" width="1640" height="2360" loading="lazy" decoding="async" alt="Safari offers temporary or ongoing access to chatgpt.com."></a>
    <figcaption>Safari offers temporary or ongoing access to chatgpt.com.</figcaption>
  </figure>
</div>

<details>
<summary>Enable LogGPT on iPhone</summary>
<div class="loggpt-guide-screenshots">
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/02-safari-page-menu.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/02-safari-page-menu.webp' | relative_url }}" width="1320" height="2868" loading="lazy" decoding="async" alt="Open Safari's bottom page menu and scroll to Manage Extensions."></a>
    <figcaption>Open Safari's bottom page menu and scroll to Manage Extensions.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/05-loggpt-in-safari-menu.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/05-loggpt-in-safari-menu.webp' | relative_url }}" width="1320" height="2868" loading="lazy" decoding="async" alt="Choose LogGPT in the page menu to grant it access to the site."></a>
    <figcaption>Choose LogGPT in the page menu to grant it access to the site.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/06-chatgpt-permission.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/06-chatgpt-permission.webp' | relative_url }}" width="1320" height="2868" loading="lazy" decoding="async" alt="Safari asks for permission to access chatgpt.com."></a>
    <figcaption>Safari asks for permission to access chatgpt.com.</figcaption>
  </figure>
</div>
</details>

## Export your first conversation

Tap the **LogGPT download icon** in the ChatGPT conversation header. If you can't see the header while the message field is focused, tap outside the message field. You can also tap **LogGPT** in Safari's extensions menu and choose **Download current conversation**.

With Basic, LogGPT prepares the conversation as JSON. **Export ready** shows the filename when the file is ready to save.

<div class="loggpt-guide-screenshots">
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/07-in-page-download.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/07-in-page-download.webp' | relative_url }}" width="1640" height="2360" loading="lazy" decoding="async" alt="The LogGPT download icon sits beside Share in the conversation header."></a>
    <figcaption>The LogGPT download icon sits beside Share in the conversation header.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/06-basic-toolbar-popup.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/06-basic-toolbar-popup.webp' | relative_url }}" width="1640" height="2360" loading="lazy" decoding="async" alt="Download current conversation also appears in the LogGPT toolbar popup."></a>
    <figcaption>Download current conversation also appears in the LogGPT toolbar popup.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/08-basic-export.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/08-basic-export.webp' | relative_url }}" width="1640" height="2360" loading="lazy" decoding="async" alt="Export ready shows the JSON filename and Choose Location."></a>
    <figcaption>Export ready shows the JSON filename and Choose Location.</figcaption>
  </figure>
</div>

<details>
<summary>Start a download on iPhone</summary>
<div class="loggpt-guide-screenshots">
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/08-in-page-download.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/08-in-page-download.webp' | relative_url }}" width="1320" height="2868" loading="lazy" decoding="async" alt="The LogGPT button sits beside Share at the top of the conversation."></a>
    <figcaption>The LogGPT button sits beside Share at the top of the conversation.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/09-basic-export-ready.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/09-basic-export-ready.webp' | relative_url }}" width="1320" height="2868" loading="lazy" decoding="async" alt="Choose Location appears below the filename on iPhone."></a>
    <figcaption>Choose Location appears below the filename on iPhone.</figcaption>
  </figure>
</div>
</details>

## Save the export in Files

1. In **Export ready**, tap **Choose Location**. If a default folder is already set, tap **Change Location** to choose a different folder for this file.
2. Choose **Save LogGPT to Files** from Safari's Share menu. If the action is farther down, tap **View More** or scroll.
3. In the Files picker, open a folder under **On My iPhone**, **On My iPad**, or **iCloud Drive**. Check the folder name at the top. Tap the filename field at the bottom if you want to rename the export.
4. Tap the blue **Save** button. The export appears in the folder you selected.

<div class="loggpt-guide-screenshots">
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/09-share-action.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/09-share-action.webp' | relative_url }}" width="1640" height="2360" loading="lazy" decoding="async" alt="Choose Save LogGPT to Files in Safari's Share menu."></a>
    <figcaption>Choose Save LogGPT to Files in Safari's Share menu.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/10-basic-files-save.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/10-basic-files-save.webp' | relative_url }}" width="1640" height="2360" loading="lazy" decoding="async" alt="The Files picker shows On My iPad, the filename field, and Save."></a>
    <figcaption>The Files picker shows On My iPad, the filename field, and Save.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/12-basic-export-saved.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/12-basic-export-saved.webp' | relative_url }}" width="1640" height="2360" loading="lazy" decoding="async" alt="The Basic JSON export appears in the Downloads folder."></a>
    <figcaption>The Basic JSON export appears in the Downloads folder.</figcaption>
  </figure>
</div>

<details>
<summary>Save the file on iPhone</summary>
<div class="loggpt-guide-screenshots">
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/10-choose-location-share.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/10-choose-location-share.webp' | relative_url }}" width="1320" height="2868" loading="lazy" decoding="async" alt="Save LogGPT to Files is in the action row at the bottom."></a>
    <figcaption>Save LogGPT to Files is in the action row at the bottom.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/11-basic-files-save.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/11-basic-files-save.webp' | relative_url }}" width="1320" height="2868" loading="lazy" decoding="async" alt="The Files sheet shows On My iPhone, Save, and the name field."></a>
    <figcaption>The Files sheet shows On My iPhone, Save, and the name field.</figcaption>
  </figure>
</div>
</details>

## Unlock LogGPT Plus

Open LogGPT and tap **Unlock LogGPT Plus**. Review the one-time price shown in the app and confirm through the App Store. If you've already purchased Plus, tap **Restore purchases** using the Apple Account that purchased it. The app shows **Plus is unlocked** when the upgrade is active.

Tap **Use Plus Home Screen Icon** if you'd like to give LogGPT the Plus icon. Tap **Use Standard Home Screen Icon** to switch back.

<div class="loggpt-guide-screenshots">
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/16-plus-unlocked.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/16-plus-unlocked.webp' | relative_url }}" width="1640" height="2360" loading="lazy" decoding="async" alt="The LogGPT app shows Plus is unlocked and offers the Plus Home Screen icon."></a>
    <figcaption>The LogGPT app shows Plus is unlocked and offers the Plus Home Screen icon.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/17-plus-home-screen-icon-confirmation.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/17-plus-home-screen-icon-confirmation.webp' | relative_url }}" width="1640" height="2360" loading="lazy" decoding="async" alt="iPadOS confirms the switch to the Plus icon."></a>
    <figcaption>iPadOS confirms the switch to the Plus icon.</figcaption>
  </figure>
</div>

<details>
<summary>See Plus and its Home Screen icon on iPhone</summary>
<div class="loggpt-guide-screenshots">
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/16-plus-unlocked.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/16-plus-unlocked.webp' | relative_url }}" width="1320" height="2868" loading="lazy" decoding="async" alt="The LogGPT app confirms Plus is unlocked."></a>
    <figcaption>The LogGPT app confirms Plus is unlocked.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/18-plus-home-screen.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/18-plus-home-screen.webp' | relative_url }}" width="1320" height="2868" loading="lazy" decoding="async" alt="The optional Plus icon on the iPhone Home Screen."></a>
    <figcaption>The optional Plus icon on the iPhone Home Screen.</figcaption>
  </figure>
</div>
</details>

## Export with artifacts

Start another download in Safari. In **LogGPT Plus Export**, turn on **Download artifacts** and choose the content to include.

- **Generated Content** collects available images, charts, and files created during the conversation.
- **Uploaded Content** collects available files you attached.
- **Save web thumbnails for offline viewing** saves available image-search previews using the URLs already recorded in the conversation.

Tap **OK** and wait for **Export ready**. The progress panel shows files and thumbnails as they are processed. Tap **Cancel** if you need to stop. For a JSON-only export, clear **Download artifacts** before tapping **OK**.

To reuse your selections, choose **Don't ask me again**. You can revise them in the LogGPT toolbar popup, turn on **Ask for download choices every time**, or use **Reset to Defaults**.

<div class="loggpt-guide-screenshots">
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/19-plus-safari-popup.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/19-plus-safari-popup.webp' | relative_url }}" width="1640" height="2360" loading="lazy" decoding="async" alt="LogGPT Plus settings and saved export preferences in the toolbar popup."></a>
    <figcaption>LogGPT Plus settings and saved export preferences in the toolbar popup.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/20-plus-export-options.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/20-plus-export-options.webp' | relative_url }}" width="1640" height="2360" loading="lazy" decoding="async" alt="Choose generated files, uploaded files, and web thumbnails for this export."></a>
    <figcaption>Choose generated files, uploaded files, and web thumbnails for this export.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/21-collecting-artifacts.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/21-collecting-artifacts.webp' | relative_url }}" width="1640" height="2360" loading="lazy" decoding="async" alt="LogGPT shows the current artifact and how many it has collected."></a>
    <figcaption>LogGPT shows the current artifact and how many it has collected.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/22-saving-web-thumbnails.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/22-saving-web-thumbnails.webp' | relative_url }}" width="1640" height="2360" loading="lazy" decoding="async" alt="The thumbnail progress panel counts processed URLs."></a>
    <figcaption>The thumbnail progress panel counts processed URLs.</figcaption>
  </figure>
</div>

<details>
<summary>Choose what Plus includes on iPhone</summary>
<div class="loggpt-guide-screenshots">
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/19-plus-safari-popup.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/19-plus-safari-popup.webp' | relative_url }}" width="1320" height="2868" loading="lazy" decoding="async" alt="The Plus toolbar popup opens as a sheet on iPhone."></a>
    <figcaption>The Plus toolbar popup opens as a sheet on iPhone.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/20-plus-export-options.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/20-plus-export-options.webp' | relative_url }}" width="1320" height="2868" loading="lazy" decoding="async" alt="Choose artifacts and thumbnails for a single export."></a>
    <figcaption>Choose artifacts and thumbnails for a single export.</figcaption>
  </figure>
</div>
</details>

## Remember a default folder

1. In **Export ready**, tap **Set Default Folder**, then **Save LogGPT to Files**.
2. In the Files picker, navigate to the folder you want and tap **Open**. This selects the folder and returns you to **Export ready**.
3. Check the location below the filename, then tap **Save**. In future exports you can tap **Save** to use that folder again.

If the destination reads **Files ' File Provider Storage**, open **On My iPhone** or **On My iPad** in Files to find the export. For one export somewhere else, use **Change Location**. To change the remembered location, use **Set Default Folder** again.

<div class="loggpt-guide-screenshots">
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/25-default-folder-picker.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/25-default-folder-picker.webp' | relative_url }}" width="1640" height="2360" loading="lazy" decoding="async" alt="Tap Open to remember Downloads as the default folder."></a>
    <figcaption>Tap Open to remember Downloads as the default folder.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/26-plus-save-to-default.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/26-plus-save-to-default.webp' | relative_url }}" width="1640" height="2360" loading="lazy" decoding="async" alt="Export ready shows the remembered destination and a direct Save button."></a>
    <figcaption>Export ready shows the remembered destination and a direct Save button.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/28-basic-and-plus-in-files.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/28-basic-and-plus-in-files.webp' | relative_url }}" width="1640" height="2360" loading="lazy" decoding="async" alt="The JSON and Plus archive are visible together in Files."></a>
    <figcaption>The JSON and Plus archive are visible together in Files.</figcaption>
  </figure>
</div>

<details>
<summary>Set the default folder on iPhone</summary>
<div class="loggpt-guide-screenshots">
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/25-default-folder-picker.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/25-default-folder-picker.webp' | relative_url }}" width="1320" height="2868" loading="lazy" decoding="async" alt="Tap Open to remember the current folder."></a>
    <figcaption>Tap Open to remember the current folder.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/27-export-saved.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/27-export-saved.webp' | relative_url }}" width="1320" height="2868" loading="lazy" decoding="async" alt="The saved confirmation shows the location immediately below the filename."></a>
    <figcaption>The saved confirmation shows the location immediately below the filename.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/28-exports-in-files.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/28-exports-in-files.webp' | relative_url }}" width="1320" height="2868" loading="lazy" decoding="async" alt="Both the Basic JSON and the Plus archive appear under On My iPhone."></a>
    <figcaption>Both the Basic JSON and the Plus archive appear under On My iPhone.</figcaption>
  </figure>
</div>
</details>

## Move LogGPT higher in Share

1. Open a conversation in Safari and tap Safari's square-with-arrow **Share** button. If you use the compact toolbar on iPhone, open Safari's page menu first and tap **Share**.
2. At the bottom of the actions list, tap **Edit Actions**. Use **View More** first if it's visible.
3. If Safari shows a **+** next to **Save LogGPT to Files**, tap it to add the action to **Favorites**. If a reorder handle appears, drag the action higher, then tap **Done** or the checkmark. Some versions show an on/off switch. Turn the action on there when that's the control Safari presents.

<div class="loggpt-guide-screenshots">
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/30-share-actions.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/30-share-actions.webp' | relative_url }}" width="1320" height="2868" loading="lazy" decoding="async" alt="Tap Edit Actions at the bottom of the expanded Share menu."></a>
    <figcaption>Tap Edit Actions at the bottom of the expanded Share menu.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/31-edit-share-actions.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/31-edit-share-actions.webp' | relative_url }}" width="1320" height="2868" loading="lazy" decoding="async" alt="Tap the green add button beside Save LogGPT to Files."></a>
    <figcaption>Tap the green add button beside Save LogGPT to Files.</figcaption>
  </figure>
  <figure class="project-screenshot">
    <a href="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/33-share-reordered.webp' | relative_url }}"><img src="{{ '/assets/images/projects/LogGPT/ios-guide/iphone/33-share-reordered.webp' | relative_url }}" width="1320" height="2868" loading="lazy" decoding="async" alt="Drag the handle to put Save LogGPT to Files first in Favorites."></a>
    <figcaption>Drag the handle to put Save LogGPT to Files first in Favorites.</figcaption>
  </figure>
</div>

## Troubleshoot an export

- **The download button is missing.** Check that you're on a conversation in Safari, LogGPT is enabled, and it has access to `chatgpt.com`. Reload the conversation or open **Download current conversation** from the LogGPT toolbar popup.
- **A file is still waiting to be saved.** Use **Save**, **Choose Location**, or **Change Location** to finish. Use **Discard Export** to clear the waiting file if you no longer need it.
- **Collection has stopped progressing.** Tap **Cancel**. If the panel stays stuck, reload the conversation and try again. To save the conversation without waiting for attachments, turn off **Download artifacts** and save it as JSON.
- **The folder is unavailable.** Use **Change Location** for the current file or **Set Default Folder** to choose a folder you can access.


