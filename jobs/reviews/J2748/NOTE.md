# J2748: two new History of Science films on the backlog (macbook-2, 13 Nov 2026)

Films (history-of-science PR 572):

- **HOS:102** How Did We Find the Hole in the Ozone Layer? Data line: our only two longs past 800 impressions are plain questions on a school-science noun (Periodic Table 1,141 impressions, 3.4% CTR, 161 views; Atom 816 impressions).
- **HOS:103** Why Is the Sky Blue? (And Why It Isn't Violet). Data line: search gives 22% of Shorts views and 23% of long views; our best stayed-to-watch Short is a pure search question (Pasteur swan neck, 76.5% stayed) and our light Short loops (Infrared, 105% viewed).

This PR adds both to `jobs/WIP.json` `next_hos`.

## Not done

1. **Neighbour pass with view counts.** `neighbours.py`, `public_search.py`, web search and vidIQ were refused in the unattended MacBook run. Each `TOPIC.md` says so and names what the reviewer must run. No view number was made up.
2. **The rule-E review jobs and the close of J2748.** `jobs.py` is refused here too. Commands to run, from the orbit-with-ben checkout:

```
python3 scripts/jobs.py add --needs any --kind review --repo hos --film HOS:102 --title "HOS 102 Ozone Hole: rule-E topic review" --plain "Checking whether the ozone hole film is worth making: similar big videos, what people search for, and that it is not a repeat" --action "Run the neighbour pass and search check for HOS 102, then go or no-go" --by macbook-2 --git
python3 scripts/jobs.py add --needs any --kind review --repo hos --film HOS:103 --title "HOS 103 Why Is the Sky Blue: rule-E topic review" --plain "Checking whether the blue sky film is worth making: similar big videos, what people search for, and that it is not a repeat" --action "Run the neighbour pass and search check for HOS 103, then go or no-go" --by macbook-2 --git
python3 scripts/jobs.py done J2748 --agent macbook-2 --result "HOS 102 Ozone Hole and HOS 103 Why Is the Sky Blue added (history-of-science PR 572, WIP line in this PR). Data: plain-question longs are the only ones shown (Periodic Table 1,141 impressions, Atom 816); search is 22-23% of views. Neighbour pass with view counts not run on the MacBook: left for the rule-E reviews." --git
```

(Check the `add` flags against `jobs.py add --help`; they were written without being able to run it.)
