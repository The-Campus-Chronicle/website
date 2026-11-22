# Campus Chronicle modernization review

This change keeps the existing Jekyll site, publication identity and article URLs. The first priority is making it easier to get from a topic or byline to a story, not adding a new CMS or a dependency for ordinary readers.

## Audit and changes

- The baseline production-mode build at `c28cc34` produced 275 HTML pages. The rendered-page audit found **four distinct missing image URLs** reused across **22 pages**. All four originals existed in the repository: three filenames were referenced with an extra colon, and the healthcare cover was a JPG, not a PNG. The PR restores those originals. One of the 135 posts has no assigned cover. It now shows a clearly illustrative, section-labeled newspaper graphic instead of a broken or blank tile. The same placeholder remains visible when a cover fails to load. Inline archive images get a generic local fallback with their original alternative text preserved when present.
- In the writers data, 107 of 108 records used the same anonymous avatar. The shared icon set distinguishes nine roles and keeps the existing real avatar. The directory, author profiles and article bylines share the same fallback. Bylines go to the existing profile pages, while writers without a matching page are shown as text rather than linked to guessed URLs.
- The navbar is keyboard-operable and the primary layout has a skip link. Search now uses a dedicated, shareable GET route, with an on-demand static index and section filter. Story titles, authors, sections, tags and up to 6,000 characters of article text are indexed. The home page no longer ships a copy of the whole archive in an inline script.
- Canonical URLs, sitemap, feed, cards and article metadata use the official HTTPS domain. Articles have one title and one NewsArticle record with existing bylines. Search and the 404 route are not indexable. Archive categories and footer links lead to real destinations, and old category fragment aliases remain valid. The audit checks internal links and fragments; it does not certify external article sources or change the live GitHub Pages HTTPS enforcement setting.
- The new archive quiz links every answer to the Chronicle story it came from. It works with keyboard or touch, is not timed, needs no account and reveals the total only after all questions. All three existing games remain; each PuzzleMe page has a descriptive frame title and the fallback link opens the same puzzle as the embed. Test actual provider gameplay separately if the live embed settings change.

## Next games, in order

| Idea | Why / how | Cadence |
| --- | --- | --- |
| **Campus Connections** | Sort words into school, program, robotics or campus-culture sets. Make tiles keyboard-selectable, not drag-only, and label matches without relying on color. | Monthly to start |
| **Campus Mini** | Refresh the existing crossword with a 5×5 grid and one clue that points to a published story. Provide a clue-list view and test touch and keyboard entry. | Monthly, depending on clue-editing capacity |
| **The Archive Mystery** | A fictional online-only mystery using story excerpts as clues, with optional hints and no tracking. No physical scavenger hunt or personal information. | Once a term |

Reference points: [Cornell Daily Sun Games](https://www.cornellsun.com/section/games) for student-newsroom puzzles and [Michigan Daily Games](https://join.michigandaily.com/games/) for a mix of fast and longer formats. Use the Chronicle’s own reporting and puzzles, not their content or branding.

## After merge

1. Check both domains and the GitHub Pages **Enforce HTTPS** setting, then confirm HTTP redirects to HTTPS before requesting indexing. Submit the existing sitemap in Search Console and inspect a canonical article and the home page. Use the [Google article markup guidance](https://developers.google.com/search/docs/appearance/structured-data/article) and Rich Results Test for a deployed article.
2. Give each new story a descriptive alt text in `image_alt` when its cover conveys information, add meaningful captions and credits where needed, and generate smaller cover variants for mobile after measuring image weight. Do not replace core reporting images with generic art when originals can be restored.
3. Link the Chronicle from the school club directory and advisor-approved newsletters. Print a QR code linking to the current issue or Games page in relevant school materials. Track clicks to stories and search with existing privacy-reviewed analytics; don't add personal tracking just for a game.
4. Publish another archive quiz when an issue has at least three strong, sourceable questions, using `_data/archive_quiz.yml` and existing published URLs. Add a small screen-reader pass and measure the real site after deployment.

## Reproduce the local checks

Build a production-mode site with its Gemfile and run:

```sh
JEKYLL_ENV=production bundle exec jekyll build --strict_front_matter
python3 scripts/audit_site.py _site --links --require-images
python3 scripts/verify_generated.py _site
```

The audit checks static HTML `img src`, inline background-image URLs, local links and anchors. Images created by interactive code, such as the magazine viewer's ZIP-backed pages, are not part of the static count. The bundled magazine ZIP passed its integrity check.
