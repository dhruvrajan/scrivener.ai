scrivener.ai
-----------

Engage in your meetings, and with your colleauge. Simply discuss, and count on scrivener as your virtual scribe.

## Inspiration
At the internship I've had, many of the meetings were boring, and difficult for any engineer or manager to engage in thoughtfully. Generally, managers have to project their Gantt chart creation system, like microsoft Project on the board, and go through the tedious process of manipulating them manually.

## What it does
My idea is to create these Gantt charts automatically, just by having a system listening to the meeting, and transcribing it.

## How I built it
I built this project with python and NLTK. I use syntax parsing: once the speech (individual sentences) is parsed, the system looks for pairs of regular and subordinate clauses with subordinators like "before", "after", etc to determine the relative priority of the tasks in each clause. It then assigns each task a priority level, and outputs an html file with (as of yet, unpolished) list indented based on priority.
## Challenges I ran into
The main challenge I ran into was creating a grammar that was complex and expansive enough to capture the the notion of relative priority of clauses. It took a while, but eventually I figured that a reasonable way to split up a sentence was into clauses. Another challenge I ran into was to expand the lexicon to include a very large set of english words; I ended up finding a pos-tagged dictionary online, and updating the terminal grammar rules (such as N -> 'fox').

## Accomplishments that I'm proud of
I'm really happy I was able to complete this project; I've been wanting to do it for a while. Definitely my project has limitations, but I'm proud that I was able to, in pretty much half a day, figure out how to capture the concept of relative priority from language. I think that this field wil be one of the most important going forward: giving computers real human-like understanding of textual data, and I'm really excited.

## What I learned
This was the second time I had used parsing on a project. I developed a sense for how to construct grammars iteratively and make them more complex. I also looked into statistical parsing derived from text; it worked, but the grammars which resulted were too complex to use for this project.


## What's next for scrivener.ai
There are many ways to go next, including
- Instead of relative priority, have a clear idea of inter-task dependencies
- Add the concept of timelines and relative dates
- Improve the parsing using statistical parsing, and expanding the allowable grammar as much as possible
- Use machine learning to, given extracted clauses / tasks, help determine the relationships between them
- Lemmatize / stem the words

And much much more. I plan on developing this more, and I cant wait to see what results!
