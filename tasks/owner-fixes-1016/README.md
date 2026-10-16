# Owner's list of 16 Oct 2026 (evening) — v133–v138

The owner sent six items from looking at the canvas. Each was published as its own version (v132 is a Design-type re-save, no content change;
the live files were compared with v131 byte for byte before building on them). After v138 all 25 changed live files read back byte-identical.

| Version | Item (owner's words) | What changed | Pictures |
|---|---|---|---|
| v133 | Darshan: "the gap between રેલવે … હવાઈ માર્ગ cards and the direction — no gap" | `.vx-dmap` had no spacing rule; now 24 px above the map (desktop + phone); Darshan frames +24 px | [1440](pictures/v133_travel_gap_1440.png) · [390](pictures/v133_travel_gap_390.png) |
| v134 | "ટ્રસ્ટ દ્વારા remove this word and check if we can set mandir and not require then dont add anything" | 15 texts on 12 pages; one sentence needs a subject → "મંદિર દ્વારા જાહેર થયેલ સત્તાવાર કાર્યક્રમ"; elsewhere nothing added | wording diff in CHANGELOG |
| v135 | "nava mandir no parichay : replace ટ્રસ્ટનો to Mandir no. remove દાન" | "એ જ મંદિરનો મુખ્ય હેતુ છે" (NewTemple + 5 Home boards); "મંદિરનો વિશ્વાસ છે કે ભક્તોના સહયોગ અને નિઃસ્વાર્થ સેવાથી" | wording diff in CHANGELOG |
| v136 | "પ્રાણ પ્રતિષ્ઠા page … ૮ ફેબ્રુ., સોમવાર full" | festival page date strip "૮ ફેબ્રુઆરી, સોમવાર"; Home banner keeps the short form (full form wraps on sideways phones) | [strip](pictures/v136_date_full.png) |
| v137 | "main page phto : mandir, mataji, karamshi bapa, suresh bapa" | Home strip order મંદિર · વિહત માઁ · મેલડી માઁ · કરમશીબાપા · સુરેશબાપા; phones now show all five (were three) | [1440](pictures/v137_home_photos_1440.png) · [390](pictures/v137_home_photos_390.png) |
| v138 | "[પ્રવેશથી ગર્ભગૃહ સુધી ભક્તનો અનુભવ] is that any way that we can showcase the proper image even if it will be visualise" | ૦૧–૦૩ area boxes show close-ups cut from the architectural render (35 doorway with માતાજી, 36 pillared hall, 37 entrance steps), labelled "સ્થાપત્ય ચિત્ર"; ૦૪ stays a placeholder | [1440](pictures/v138_route_images_1440.png) · [390](pictures/v138_route_images_390.png) |

Not published — **tagline** ("we need good slogan for mandir that will be tagline for everyone"): new devotional wording is the owner's / trust's
choice, so options were given in the conversation (see CHANGELOG note) and nothing was added to the site.

## Notes

- v138 images are crops of image 14 (`ade906…`, 2400×1881) — `route/` holds the exported WebPs (crop boxes in `tools/examples/apply_v138_route_images.py`
  and below). No AI enlargement. Crop boxes (x0, y0, x1, y1 in image 14): 35 (1020, 1300, 1420, 1700) · 36 (980, 760, 1460, 1240) ·
  37 (920, 1281, 1520, 1881) → 480 px.
- Real interior photographs or the architect's 3D views of the ગર્ભગૃહ and મંડપ would replace these later; ૦૪ needs the trust's list of other areas.
- Found while testing v136: the Home banner date strip overruns its box by 2 px at 320 px wide (short form). Tiny; not changed.

## Checks per version

`check_layout.py` on the touched boards against the previous stage (22–132 runs each, 0 new problems); `frame_heights.py` (frames updated where
the content height changed: Darshan 5054, DarshanMobile 7114, GalleryMobile 10403, NewTempleMobile 11812, HomeMobile2 5986); wording diffs
with `gen_page_content.py` show exactly the intended texts.
