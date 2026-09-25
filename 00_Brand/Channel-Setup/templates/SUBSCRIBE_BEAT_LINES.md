# Subscribe beat — line library

One line per long, spoken by Ben Orbit Narrator, right after the film's first payoff (25–50% through the spoken script). About 5 seconds. The picture keeps moving underneath: no cut to a card, no pause in the story. Orbit can give a small in-scene nod or point toward the lower-right corner, where a 4-second subscribe cue plays.

`npm run gate:episode` fails a script with no beat, with more than one, or with a beat that:
- sits outside 25–50% of the spoken words;
- runs over 20 words;
- quotes a number;
- uses a stock phrase ("like and subscribe", "smash", "don't forget", "hit the bell", "before we begin").

Why: an ask at the end makes people leave before the end screen, and a small subscriber count tells strangers nobody else is watching. The ask goes mid-film, where the viewer has just got something. The count goes in the pinned comment, which `07_Content-Ops/scripts/update-pinned-comment.ts` keeps current.

## How to use

1. Pick a line you haven't used in the last four longs, and log it in the film's `production-status.md`.
2. Fill `{next}` with the next film's promise in plain words ("what happens when the Sun dies"). If the next film isn't set yet, use a line without `{next}`.
3. Put it in the script like this:

```
[SUBSCRIBE BEAT]
If you want the next one, what happens when the Sun dies, subscribing is how you'll see it.
```

## Lines

1. If you want the next one, {next}, subscribing is how you'll see it.
2. Every Sunday Orbit goes somewhere new. Subscribe and you'll be there for {next}.
3. If this is your kind of question, subscribe. Next week is {next}.
4. We make one of these every week. Subscribing is how the next one finds you.
5. Orbit's already planning the next trip: {next}. Subscribe if you want to come.
6. If you've enjoyed the ride so far, subscribing is the best way to help Orbit keep going.
7. Stay for the rest of this one, and subscribe for {next}.
8. New space mysteries every Sunday. Subscribe and they'll come to you.
9. If you'd like more questions like this one, subscribing really helps a small channel.
10. There's more to come after this, starting with {next}. Subscribe so you don't miss it.

## The end of the film

No goodbye and no second ask. The last spoken line hands off to the next film ("Next, Orbit falls into Jupiter."), and the Studio end screen shows it.
