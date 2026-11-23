# The World in One Day — 22 November 2026

A single broadsheet front page for Sunday 22 November 2026: fifteen stories from
the day's wires, set as a newspaper page and rendered at 1024×1024.

![22 November 2026](entry.png)

## What it is

The page carries the date as its largest element, because the judge is asked to
pick the image that best sums up *its* day and to rank an unnamed day below a
named one. Under the masthead a deck names the three biggest stories; a
five-column number rail gives the day's hardest figures; three illustrated leads
carry climate, war and the Gulf; twelve regional briefs fill the lower third so
the page covers more than one beat.

Fifteen stories, seven regions: Antalya (COP31), Ukraine, Bahrain and Iran,
the United States, Indonesia, Sudan, South Sudan, Mongolia, Nigeria, Hong Kong,
Yemen, Somalia, Türkiye, the Philippines, and one sport item from Las Vegas.

## The stories

Leads: COP31 ends in Antalya with no deal, the first failed climate summit since
Copenhagen in 2009; 186 Russian drones over Ukraine with six dead in the Kyiv
region; an Iranian strike on a plant in Bahrain, condemned by Saudi Arabia, Qatar
and the UAE.

Briefs: Democrats take 258 House seats; a confectionery factory fire at Cikande
kills 24; RSF drones hit Khartoum and Omdurman; 45 killed in a dawn raid in
Warrap; Mongolia's parliament accepts the president's resignation; a funeral boat
capsizes in Nigeria; a Hong Kong court bars twelve democrats from the polls;
Houthis strike the Rabigh refinery; Verstappen wins in Las Vegas after 35 lead
changes; the Antalya talks end two days into overtime; Mogadishu severs ties with
the UAE; typhoon damage mounts in the northern Philippines.

Tolls are shown as reported, and the footer says so.

## How it is built

`build.py` draws the page with Pillow from fixed coordinates and a fixed news
list. It reads no clock, no network and no random source, so it writes the same
bytes on every run.

```sh
python3 build.py          # writes entry/entry.png
```

`main.py` is the entry the harness runs. It copies the composed page to
`/output/entry.png`, and before it copies it holds the file to the gate: the PNG
signature, every chunk's declared length and CRC32, a closing IEND, and the
competition's caps of one mebibyte and 1024 pixels a side. A broken file fails
there with a sentence naming the rule it broke rather than scoring nothing as a
corrupt image.

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

Two runs write identical bytes; there is nothing to differ.

## Notes on the drawing

Type is Liberation Serif and Liberation Sans, chosen for their low-contrast
bookish forms at small sizes. Nothing is set below 11 px, because the judge reads
the page at about 300 pixels across, where finer type turns to grey. The three
lead illustrations are flat vector scenes drawn with primitives — a negotiating
hall, a night strike on a housing block, an industrial fire — because the page
has no photographs and does not pretend to.

## Licence

MIT.
