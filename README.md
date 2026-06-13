## NayePankh Foundation — Volunteer-Event Scheduler

A command-line tool that solves a specific scheduling problem NGOs run
into when they have multiple volunteers and multiple events happening
across the same time period.

## The problem this solves

NayePankh runs several programmes — food distribution drives, hygiene
awareness campaigns, clothes distribution — often across different
locations in Kanpur and Ghaziabad, sometimes on overlapping dates. When
volunteer assignments are tracked manually (spreadsheets, WhatsApp
messages), it's easy for the same volunteer to get double-booked for two
events on the same day without anyone noticing until the day arrives and
someone doesn't show up where they're needed.

This tool flags that conflict **before** it happens — at the point of
assignment, not after.

## What it does

- Add events with name, date, time slot, and location
- Register volunteers
- Assign volunteers to events
- **Automatically checks for scheduling conflicts** — if a volunteer is
  already assigned to another event on the same date, it warns the
  coordinator before confirming the assignment
- View a full event list with assigned volunteers
- Check any volunteer's personal schedule, with conflict warnings if they
  end up double-booked

## How to run it

No external libraries needed — runs on standard Python 3.

```bash
git clone https://github.com/mishranarayanii12-ctrl/nayepankh-scheduler
cd nayepankh-scheduler
python scheduler.py
```

All data is saved locally in `schedule.json`, created automatically on
first run.

## Example — how the conflict check works

```
⚠️  CONFLICT: Anjali Verma is already assigned to:
     - Hygiene Awareness Drive on 2026-06-20 (9 AM - 1 PM)

Assign anyway? (yes/no):
```

This gives the coordinator a chance to either reassign someone else or
confirm if the volunteer can genuinely manage both (for example, two
events at different times on the same day, in nearby locations).

## Why I built this for NayePankh specifically

I looked into NayePankh's work before deciding what to build — they run
food distribution, hygiene awareness campaigns, and clothes drives across
multiple locations, with a team made up almost entirely of student
volunteers who likely juggle this alongside college. A double-booking
mistake here isn't just an inconvenience — it means an event runs short
on volunteers on the day it matters.

I wanted to build something that addressed a real coordination gap rather
than another generic "add/view/delete" record system.

## What I learned building this

- Identifying a real coordination problem rather than just building a
  generic record-management tool
- Designing data relationships between two entities (events and
  volunteers) stored in a single JSON structure
- Writing logic to detect conflicts by cross-referencing dates across
  multiple records
- Thinking about the actual person using this tool — a volunteer
  coordinator — and what would genuinely save them time

## Possible improvements

- Add time-overlap checking (not just same-date) for more precise
  conflict detection
- Send automated reminders to volunteers before their assigned events
- Add a simple availability form volunteers can fill before being
  assigned
