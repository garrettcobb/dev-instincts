# Licensing lessons

Not legal advice. This is what was checked in the trial and what to check next time.

## Look-alike UI (copying Windows File Explorer)
- **Allowed:** Fluent UI React and Fluent System Icons are Microsoft's MIT-licensed libraries, meant for building apps in Microsoft's style.
- **Allowed:** using the system font (Segoe UI) by name without bundling it.
- **Allowed:** truthful mentions such as "Use my Windows setting".
- **Not allowed:** Microsoft's trademark guidelines list trade dress as theirs and say not to use their "logos, icons, or designs, in any manner" or imply endorsement. A pixel-faithful copy of a Microsoft product sits closer to that line than ordinary Fluent styling.
- **Risk:** low for an internal tool with its own name that isn't sold. Get a real legal read before selling or distributing anything that looks like this.

## Icon packs
- **Icons8 free license:** personal use, a visible clickable link back wherever the icons are used, no team or co-worker use. A company app used by staff needs a paid license or different icons.
- **Rule:** check the license of every asset **when you add it**, and keep a `THIRD-PARTY-NOTICES` file listing each one.

## Open-source notices
- MIT (React, Fluent UI) requires the copyright and license notice in copies. Bundlers strip comments, so ship a notices file with the app.
- Apache-2.0 (pdf.js) requires the license and NOTICE to be kept.

## Sources
- https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general.aspx
- https://intercom.help/icons8-7fb7577e8170/en/articles/5534926-universal-multimedia-license-agreement-for-icons8
