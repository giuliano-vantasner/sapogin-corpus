# Sapogin corpus download report

Date: 2026-09-01 · Inventory: 54 documents · **OK: 54 · Failed: 0** · Total bytes: 78584681 (74.9 MiB)

Method: sequential curl (browser UA, `--referer https://sapogin.com/`, 120 s timeout, one retry).
Google Drive files: `uc?export=download` with cookie jar, confirm-form follow-up; content verified
by magic bytes (%PDF / OLE2 / PK) before storage. All 54 files verified as PDF documents.

| doc_id | section | status | bytes | magic | notes |
|---|---|---|---|---|---|
| AR01 | articles | ok | 576490 | %PDF-1.5 |  |
| AR02 | articles | ok | 345704 | %PDF-1.4 |  |
| AR03 | articles | ok | 233434 | %PDF-1.5 |  |
| AR04 | articles | ok | 551314 | %PDF-1.5 |  |
| AR05 | articles | ok | 802892 | %PDF-1.5 |  |
| AR06 | articles | ok | 582672 | %PDF-1.5 |  |
| AR07 | articles | ok | 660647 | %PDF-1.5 |  |
| AR08 | articles | ok | 697209 | %PDF-1.5 |  |
| AR09 | articles | ok | 536002 | %PDF-1.5 |  |
| AR10 | articles | ok | 299033 | %PDF-1.5 |  |
| BR01 | brochure | ok | 6242288 | %PDF-1.4 |  |
| BR02 | brochure | ok | 825849 | %PDF-1.5 |  |
| BR03 | brochure | ok | 605938 | %PDF-1.5 |  |
| BR04 | brochure | ok | 1958545 | %PDF-1.5 |  |
| DI01 | dissertation | ok | 820972 | %PDF-1.4 |  |
| DI02 | dissertation | ok | 8898370 | %PDF-1.4 |  |
| MO01 | monography | ok | 4880949 | %PDF-1.5 |  |
| MO02 | monography | ok | 6427711 | %PDF-1.4 |  |
| MO03 | monography | ok | 1308227 | %PDF-1.4 |  |
| PA01 | patents | ok | 4012383 | %PDF-1.5 |  |
| PA02 | patents | ok | 738175 | %PDF-1.5 |  |
| PA03 | patents | ok | 956880 | %PDF-1.5 |  |
| PM01 | perpetual_motion | ok | 448167 | %PDF-1.5 | Google Drive file; title_ru taken from Drive-stored filename (Latin transliteration, no Russian title on source); retrieved via uc?export=download flow with cookie jar |
| PM02 | perpetual_motion | ok | 1485296 | %PDF-1.7 | Google Drive file; title_ru taken from Drive-stored filename (Latin transliteration, no Russian title on source); retrieved via uc?export=download flow with cookie jar |
| TE01 | teaching | ok | 427335 | %PDF-1.5 |  |
| TE02 | teaching | ok | 1175295 | %PDF-1.5 |  |
| TE03 | teaching | ok | 544069 | %PDF-1.5 |  |
| TE04 | teaching | ok | 646902 | %PDF-1.5 |  |
| TE05 | teaching | ok | 1586165 | %PDF-1.4 |  |
| TE06 | teaching | ok | 498085 | %PDF-1.5 |  |
| TE07 | teaching | ok | 458037 | %PDF-1.5 |  |
| TE08 | teaching | ok | 924597 | %PDF-1.5 |  |
| TE09 | teaching | ok | 10087730 | %PDF-1.5 |  |
| TE10 | teaching | ok | 3731681 | %PDF-1.7 |  |
| TE11 | teaching | ok | 315576 | %PDF-1.5 | inventory URL (as linked by sapogin.com) returns HTTP 404 twice; server stores file under all-lowercase name — retrieved successfully from lowercase variant |
| TE12 | teaching | ok | 2785072 | %PDF-1.5 |  |
| TE13 | teaching | ok | 234163 | %PDF-1.5 |  |
| TE14 | teaching | ok | 432180 | %PDF-1.5 |  |
| TE15 | teaching | ok | 686763 | %PDF-1.5 |  |
| TC01 | technologies | ok | 299212 | %PDF-1.3 |  |
| TC02 | technologies | ok | 871471 | %PDF-1.5 |  |
| TC03 | technologies | ok | 697654 | %PDF-1.5 |  |
| TC04 | technologies | ok | 629852 | %PDF-1.5 |  |
| TC05 | technologies | ok | 777406 | %PDF-1.5 |  |
| TC06 | technologies | ok | 567795 | %PDF-1.5 |  |
| TC07 | technologies | ok | 481155 | %PDF-1.5 |  |
| TC08 | technologies | ok | 1495809 | %PDF-1.5 |  |
| WO01 | works | ok | 374373 | %PDF-1.5 |  |
| WO02 | works | ok | 606184 | %PDF-1.5 |  |
| WO03 | works | ok | 553495 | %PDF-1.5 |  |
| WO04 | works | ok | 552491 | %PDF-1.5 |  |
| WO05 | works | ok | 390636 | %PDF-1.5 | inventory URL (as linked by sapogin.com) returns HTTP 404 twice; server stores file under all-lowercase name — retrieved successfully from lowercase variant |
| WO06 | works | ok | 420087 | %PDF-1.5 |  |
| WO07 | works | ok | 438264 | %PDF-1.5 |  |

## Failures

None. Every inventory URL yielded a verified document.

## Notes

- The site sapogin.com links `Проект электростатического электрометра с измерительной шкалой.pdf` (TE11)
  and `Панегирик Неисчерпаемому Персональному Накопителю Электрической Энергии.pdf` (WO05) with exactly
  the inventory spelling, but the storage server (case-sensitive nginx) hosts both files under
  all-lowercase names; the inventory URLs 404. Both were recovered from the lowercase variants and the
  working URLs recorded in MANIFEST.yaml `source_url`.
- dissertation/DI02 and monography/MO02 share the title “Механизмы удержания вещества
  самосогласованным полем” but are **not** byte-identical (8.9 MB vs 6.4 MB, different md5) — both kept.
- PM01/PM02 (Google Drive): Drive-stored filenames are Latin transliterations; recorded as title_ru.
- `retrieved` is the actual download date (2026-09-01), not the 2026-08-31 date in the contract example.
