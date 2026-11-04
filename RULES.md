# SafeSpace Hacks: rules and criteria

Source pages fetched on 4 November 2026:

* Overview: https://safespace-hacks.devpost.com/
* Rules: https://safespace-hacks.devpost.com/rules
* Resources: https://safespace-hacks.devpost.com/resources
* Updates: https://safespace-hacks.devpost.com/updates (no announcements yet)

Quoted text below is copied from those pages. Notes in plain paragraphs are ours.

## Key facts

| Item | Value |
| --- | --- |
| Build window | 17 October 2026, 12:00 AM ET to 22 November 2026, 5:00 PM ET |
| Deadline in India | Monday 23 November 2026, 03:30 IST |
| Judging | 23 November 9:00 AM ET to 24 November 5:00 PM ET |
| Results | 25 November 2026, 9:00 AM ET |
| Eligibility | Students at a recognized institution, above the legal age of majority; companies excluded; solo or team |
| Prize | 1st place, SafeSpace Grand Prize: $280 cash. 2nd, 3rd and runners up are honorary only |
| Themes listed | Beginner Friendly, Cybersecurity, Social Good |

## Judging criteria

Four criteria, scored 1 to 5, equal weight. Ranked by total score.

1. **Safety Benefit.** "Does the project address a clear security or safety problem for an identifiable user? Assess the practical benefit and credible evidence of a safer outcome, not the size of the claim."
2. **Practical Functionality.** "Does the core workflow work in the demo? Assess reliability, thoughtful implementation, and a sensible response to errors or failure. Complexity alone earns no bonus."
3. **Trust & Responsible Design.** "Does the project respect privacy, use appropriate data, explain uncertainty, and avoid creating new risks? Reward thoughtful safeguards and honest limitations."
4. **Clarity & User Experience.** "Can the intended user understand and use the solution? Assess accessibility, clear guidance, and a demo that explains the problem, event contributions, credits, and limitations."

Tie breaks: "Ties are resolved by Safety Benefit, then Practical Functionality, then a comparative review by judges."

## Submission requirements

From the overview ("Requirements" and "What judges need from you"):

* "Create a working prototype connected to security or safety. Name the intended user, the situation or risk, and the practical improvement."
* "Clearly distinguish work built during October 17 to November 22, 2026 from pre-existing components."
* "A completed Devpost project page with a name, short pitch, and all contributing team members."
* "A clear explanation of the problem, solution, technologies, challenges, and what you learned."
* "A working demo link, downloadable build, or recorded walkthrough that demonstrates core functionality, with simple setup instructions."
* "Screenshots of the experience. A short demo video of about 2 to 3 minutes is encouraged but optional."
* "A source-code or project-file link where possible, plus credits for libraries, datasets, assets, AI assistance, and pre-existing work."
* "Include one example of the safer outcome and one limitation."
* "Use synthetic examples, sample accounts, or systems you own or have explicit permission to test. Do not expose private data, credentials, or live vulnerabilities."
* "Keep all judging links accessible through November 24."
* "Submit one final entry per project by November 22 at 5:00 PM Eastern Time."

From the rules ("Submission package"): "Complete your Devpost project page with a problem statement, solution, team, credits, screenshots, and an accessible demo, build, or recorded walkthrough. A short video is optional. Keep judging links working through November 24."

## New work rule

Rules, "Scope and original work": "Submit one entry per project with a clear connection to security or safety. Identify work created during the event and credit pre-existing components, third-party assets, datasets, and AI assistance. Any stack may be used when its terms permit it. Submit only material you have permission to use."

Kedayam was started on 4 November 2026, inside the build window, in a new repository. The git history is the record of event work. Pre-existing components are third-party libraries, the Tesseract OCR engine and its language data, and the two public datasets; all are listed in the README credits.

## Responsible demonstration rule

Rules, "Demonstrate responsibly": "Use synthetic data, local demonstrations, or systems you own or have explicit permission to test. Do not attack third-party services, collect private credentials, reveal personal information, or publish live exploit details. A protective tool should not create avoidable risk for its users. Explain limitations rather than promising guaranteed safety. Projects are prototypes and should not be presented as replacements for emergency services."

How Kedayam follows it: every demo message is fictional; phone numbers and UPI IDs in examples are made up; the app never says a message is safe; it points to the 1930 helpline and cybercrime.gov.in rather than acting as a reporting channel itself.

## Entering the same project in other events

The pages say nothing explicit about entering the same project in other hackathons. The only related lines are "Submit one entry per project" and "Submit only material you have permission to use". Organizers and judges may not enter competing projects. If we consider reusing Kedayam elsewhere, we should ask the organizers through the contact link first and keep this entry the original.

## Open item for the entrant

The rules require credits for "AI assistance". The entrant must decide what to write in the Devpost credits section on this point before submitting; it is not covered in this repository.

## Resources page guidance (worth building to)

* "Does it explain why it flags something, rather than simply alarming the user?"
* "Can a user recover from a mistake or dismiss an incorrect warning?"
* "Does it collect less data than the problem requires?"
* "Is the main workflow understandable and accessible?"
* "What happens if the tool is wrong, offline, or unavailable?"
* Demo in four scenes: "Show the situation, the risk or uncertainty, the working solution, and the outcome. Then explain what you built during the event, what you reused, and one important limitation."
* "Test a normal case, a confusing case, and a failure case."
