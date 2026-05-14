# CLAUDE.md — 1tech-www

The source for the public **1tech.us** website. Plain HTML + CSS, no framework, no build step, no JS dependencies. Eight pages plus one stylesheet.

## What this repo is

The static-site source for `1tech.us`, deployed via **Cloudflare Pages** on push to `main`. A push to `main` updates the live site automatically.

## What this repo is NOT

**Not a place to add a framework.** The decision to stay on plain HTML + CSS is deliberate.

## Layout

```
/
├─ index.html       — homepage
├─ about.html       — about
├─ work.html        — what 1tech does + how it works
├─ contact.html     — contact form (posts to FormSubmit)
├─ thanks.html      — post-submit landing
├─ style.css        — single stylesheet, CSS-variable palette
└─ legal/
   ├─ index.html    — legal landing
   ├─ privacy.html  — privacy policy
   └─ terms.html    — terms of use
```

## Local preview

From the repo root:

```
python -m http.server 8000
```

Then open `http://localhost:8000/`. The contact form's POST flow is best tested under the Python server (rather than `file://`).

## Deploy

Pushes to `main` trigger a Cloudflare Pages build. Custom domain: `1tech.us`. The Pages project also gets a `*.pages.dev` URL — fine for preview, not the canonical URL.

## Contact form

The form on `/contact.html` POSTs to `https://formsubmit.co/hello@1tech.us`. After submit, FormSubmit redirects the visitor to `https://1tech.us/thanks.html` (the `_next` hidden field). First-ever submission to a new FormSubmit endpoint triggers a one-time confirmation at `hello@1tech.us`; subsequent submissions deliver straight through.

If FormSubmit ever needs to be replaced, the migration path is a Cloudflare Pages Function calling MailChannels.

## Operator

1tech LLC (Virginia LLC, Wise County). Solo operator.
