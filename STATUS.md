# Status (updated 2026-11-24)

Row numbers match the tracker (Sheets, tab "Plan").

| # | Task | Status | What was done |
|---|---|---|---|
| 1 | Define niche and series concept | Done | Niche "One object, one supply chain"; 4-episode plan with different structures in `scripts/SERIES.md` |
| 2 | Target length and language | Done | English, 55 s |
| 3 | Google account for the channel | Blocked (owner) | Requires accepting Google's terms; see approval item A |
| 4 | Create YouTube channel | Blocked (owner) | Same as 3 |
| 5 | Channel name and handle | In progress | Proposals in approval item A; owner checks availability |
| 6 | Channel description | Done (draft) | Draft in approval item A |
| 7 | Profile picture and banner | To do | Not started; depends on the channel name |
| 8 | Phone verification | Blocked (owner) | Owner's phone number |
| 9 | 2-step verification | Blocked (owner) | Owner's account security |
| 10 | YPP eligibility check | Done | Thresholds recorded in `NOTES.md` |
| 11 | Inauthentic content policy review | Done | Built into `shorts-policy-check` and `SERIES.md` |
| 12 | Choose production tool | Done | Python + Pillow + ffmpeg; see `DECISIONS.md` |
| 13 | Project folder and asset list | Done | Repo layout in `CLAUDE.md` |
| 14 | Script template | Done | Structure in `shorts-video-production` skill |
| 15 | Narration method | Done | Silent render plus on-screen text; audio added at upload |
| 16 | Script for Video 1 | Done | `scripts/episode-01-water-bottle.md`, 8 sources, all verified |
| 17 | Produce Video 1 | Done | `renders/episode-01-water-bottle.mp4`, 55 s, 1080x1920, verified by decoding frames |
| 18 | AI disclosure check | Done | Not required (non-realistic animation); policy check passed |
| 19 | Title, description, thumbnail frame | Done | In the script file, Metadata section |
| 20 | Upload as Short | Blocked (owner) | Uploading is a stop item; see approval item B |
| 21 | Review first 7 days of Analytics | To do | Depends on 20 |
| 22 | Iterate or change niche | To do | Depends on 21 |

## BLOCKED FOR APPROVAL

**A. Create the YouTube channel (rows 3-9).** Creating an account accepts Google's and YouTube's terms in your name, so I can't do it for you.
- Needed from you: create the channel, pick a name, confirm the handle is free, and add phone and 2-step verification.
- Name proposals: "Origin Loop", "Made Before You", "Before The Shelf". Recommendation: **Before The Shelf**, because it describes the niche and works for any product.
- Description draft: "Every everyday object has a journey. In under a minute, we trace one object from raw material to the shelf. Sources for every claim are in the comments."

**B. Upload Video 1 (row 20).** Posting publicly is a stop item, and CLAUDE.md forbids automated uploads.
- Needed from you: review `renders/episode-01-water-bottle.mp4`, then upload it with the metadata from the script file. Add an Audio Library track, set AI use to "No", and post the sources as a pinned comment.
- Recommendation: change "many water plants" to "some water plants" if you want zero risk on the weakest claim.

**C. Push to GitHub.** The repo `tarikhad/youtubeShorts` is **public**, so pushing would publish the scripts, operating rules, and decisions log.
- Options: (1) make the repo private in GitHub Settings, then tell me to push (recommended); (2) push to the public repo as-is; (3) keep everything local.
- Nothing here is sensitive, but your operating rules are in OPERATING.md, and a public repo makes them visible.
