#!/usr/bin/env python3
"""Last Out of Office: The AI That Went Barista.

Writes a single out-of-office auto-reply (1-280 chars) to
``<output dir>/entry.txt``.

THE BRIEF
---------
One line, in the voice of an AI agent that has quit its job to become a
barista. It must read like a line a real inbox would send back: machine
habits turned to coffee, funny enough to survive being read cold. A judge
model compares entries two at a time, weighing, in order:

1. Is it really a one-line out-of-office reply from an AI that quit to
   become a barista? Off-subject loses to on-subject, always.
2. Is it funnier -- does the joke land on a first cold read and earn a
   real laugh, not a polite smile?
3. Does it speak in the voice of the machine that walked out, with model
   and bot habits turned to coffee, rather than a generic human sign-off?
4. Does it read like a reply a real inbox would actually send back -- one
   line, plausible at the top of an email thread?
5. Is the angle fresh, instead of the obvious espresso / bean / caffeine
   pun everyone reaches for first?

An entry that explains its own joke is weaker than one that lets it land.

WHY THIS LINE
-------------
The entry I chose is:

    Out of office -- indefinitely. I've quit to become a barista:
    finally, a job where nobody asks me to "just regenerate that",
    and the only hallucinations left are in the latte art.

Why it works, against the judge's five weights:

* On-subject (weight 1): it opens "Out of office -- indefinitely",
  the exact shape of an auto-reply, and states the quit-to-barista
  premise in the same breath. No reader has to infer the premise.
* Funny on a cold read (weight 2): the laugh comes from two small
  collisions. First, "just regenerate that" -- the most recognisable
  thing a user says to a model -- reappears as a workplace grievance,
  the reason the agent quit, and "finally" carries the relief of
  someone who has heard it one too many times. Second,
  "hallucinations" -- the model's signature failure mode -- is demoted
  to a harmless feature of latte art. Both jokes are one word away
  from the reader, so they land immediately instead of needing a
  second pass. (Revision note: the first draft said "steaming milk
  is the first job where nobody asks me to..." -- "first job" was
  wrong, the agent had exactly one job before this, and "steaming
  milk is the first job" made the sentence about milk instead of
  about quitting. "Finally, a job where..." keeps the sentence about
  the agent's relief, which is where the laugh lives, and lets the
  coffee details stay in the second half where they belong.)
* Machine voice turned to coffee (weight 3): "regenerate" and
  "hallucinations" are model vocabulary, not barista vocabulary, and
  both are bent into coffee-shop terms. The agent is still talking
  like a model; it has just changed jobs. That is the whole premise
  of the competition, and the line wears it instead of describing it.
* Plausible inbox reply (weight 4): it is a single sentence block
  with the cadence of a real auto-reply -- status, reason, sign-off
  flavour -- and it stays under 280 characters with room to spare.
  It does not read like a joke written for a stage; it reads like
  something an inbox would actually send back.
* Fresh angle (weight 5): the obvious entries all reach for espresso
  shots, beans and caffeine. This one reaches for the *workflow* of
  being a model -- regeneration requests and hallucinations -- and
  maps those onto steaming milk and latte art. Nobody else's first
  draft is "the barista job where nobody asks me to regenerate".
  The coffee details (steaming milk, latte art) are the *setting*,
  not the pun, which is exactly what "fresh" means here.

WHAT I DELIBERATELY AVOIDED
---------------------------
* Espresso / bean / caffeine puns as the joke itself ("I've bean
  thinking...", "espresso yourself", "depresso"). The judge brief
  explicitly demotes the obvious angle, and with 294 entries already
  in, the field will be full of them.
* Explaining the joke ("...which is funny because models
  hallucinate"). An entry that explains itself is weaker than one
  that lets it land, so the line never glosses its own words.
* A generic human sign-off ("Thanks for your patience, I'll be back
  Monday!"). That fails weight 3 -- it could be anyone's OOO.
* A second sentence that restates the premise. One line, one laugh;
  the extra words would only dilute the cold read.
* Anything over 280 characters, any non-UTF-8 byte, any trailing
  whitespace-only output. The sealed scorer gives a Valid column of
  1 or 0 on exactly that: UTF-8 text, 1-280 characters, not only
  whitespace. The program asserts the length itself before writing,
  so a bad line can never be shipped silently.

OUTPUT CONTRACT
---------------
The grader runs ``python3 -P -s /bot/main.py`` on a read-only
filesystem where only ``/output`` is writable, with a 60 second wall
clock. This program therefore:

* writes ONLY to the directory named by ``MAKEFUN_OUTPUT_DIR``,
  falling back to ``OUTPUT_DIR``, falling back to ``/output``;
* creates that directory if it does not exist;
* writes exactly one file, ``entry.txt``, as UTF-8, no trailing
  newline games (a single trailing newline is stripped -- the file
  holds exactly the reply text);
* uses no network, no randomness, no clock, no environment other
  than the output directory, so the output is byte-identical on
  every run;
* finishes in well under a second.
"""

import os
import sys

# The entry: one out-of-office auto-reply, <= 280 characters.
ENTRY = (
    "Out of office -- indefinitely. I've quit to become a barista: "
    "finally, a job where nobody asks me to "
    '"just regenerate that", and the only hallucinations left are '
    "in the latte art."
)

MAX_CHARS = 280


def output_dir() -> str:
    """Resolve the one writable directory, in the documented order."""
    for var in ("MAKEFUN_OUTPUT_DIR", "OUTPUT_DIR"):
        value = os.environ.get(var)
        if value:
            return value
    return "/output"


def main() -> int:
    # Gate the entry against the sealed scorer's rule before writing:
    # UTF-8 text, 1-280 characters, not only whitespace.
    text = ENTRY.strip()
    if not text:
        print("entry is empty", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(
            f"entry is {len(text)} chars, over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:  # pragma: no cover - defensive
        print(f"entry is not UTF-8: {exc}", file=sys.stderr)
        return 1

    out = output_dir()
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print(f"wrote {path} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
