# DanSebo Global Services website

A static website ready for Vercel. There is no build step and no framework.

## What's in this folder

| File / folder | What it is |
|---|---|
| `index.html`, `about.html`, `services.html`, `training.html`, `gallery.html`, `contact.html` | The six pages |
| `404.html` | Shown for any link that doesn't exist |
| `site.css`, `site.js` | Shared styles and scripts |
| `assets/` | Photos, logos, certificates and icons |
| `vercel.json` | Clean URLs (`/about` instead of `/about.html`), caching and security headers |
| `robots.txt` | Lets search engines index the site |
| `_source/` | Build script for editing content. **Not uploaded to Vercel** (see `.vercelignore`) |

## Deploy on Vercel

**Option A: GitHub (recommended, so every change redeploys itself)**
1. Create a new GitHub repository and upload the *contents* of this folder (`index.html` should be at the top level of the repo).
2. In Vercel, click **Add New → Project** and import the repository.
3. On the settings screen, choose **Framework Preset: Other**. Leave the Build Command and Output Directory **empty**, and leave Root Directory as `./`.
4. Click **Deploy**.

**Option B: Vercel CLI**
```
npm i -g vercel
cd dansebo-website
vercel          # first deploy (preview)
vercel --prod   # production
```

## Connect your domain
1. In the Vercel project, open **Settings → Domains** and add your domain (for example `dansebo.com`), and also `www.dansebo.com`.
2. Vercel shows the DNS records to add. Add them at the company where you bought the domain. They are usually:
   - `A` record for `@` → `76.76.21.21`
   - `CNAME` record for `www` → `cname.vercel-dns.com`

   Always use the exact values Vercel shows you.
3. Wait for DNS to update (minutes, sometimes a few hours). Vercel adds HTTPS automatically.

## After you have the domain: sitemap and share previews
Rebuild once with your domain so Google gets a sitemap and links shared on WhatsApp/Facebook show a preview:
```
cd _source
SITE_URL=https://www.yourdomain.com python3 build.py deploy
```
Then copy everything from `_source/deploy/` back into this folder, replacing the old files.

## Editing content
All text lives in `_source/build.py` (courses and fees in `COURSES`, services, partners, CEO bio, certificates). Styles are in `_source/src/site.css`. Scripts are in `_source/src/site.js`. Run `python3 build.py deploy` and copy `_source/deploy/` over this folder.

## Online payments
The **Proceed to payment** button on each course calls `window.DanSebo.proceedToPayment()` in `site.js`. Set `paymentUrl` there to a Paystack payment page link, or replace the function with Paystack Inline checkout when you're ready.
