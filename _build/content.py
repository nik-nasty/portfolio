# Content for the portfolio site. Edit here, then run build.py.
# Rules: first person, British spelling, no client names, prices, IDs or links.

SITE = {
    "name": "Nicola Jade Feldmann",
    "short": "Nikki",
    "title_a": "Automation engineer.",
    "title_b": "Design and build.",
    "intro": (
        "I turn messy sales and operations processes into systems that run on their own, "
        "then design the pages, emails and tools people actually see. Self taught, "
        "working remotely from South Africa with UK clients."
    ),
    "email": "njfeldmann44@gmail.com",
    "upwork": "https://www.upwork.com/freelancers/~0167c1fafee283184b",
    "location": "South Africa",
    "how": [
        ("Fix the capture before the campaign.",
         "Nothing goes live until I know where every enquiry lands and who follows it up. "
         "Most of the lost leads I have found were lost quietly, between two systems."),
        ("Stages hold position, tags hold facts.",
         "A CRM only stays honest when the rules are simple enough that nobody has to remember them. "
         "I write the rules down and make the workflows enforce them."),
        ("Design that checks itself.",
         "Every page, email and proposal I build reads from one design system and passes an automated "
         "check before anyone sees it, so the hundredth file still matches the first."),
    ],
}

CLIENT_BSUK = "UK outdoor wellness manufacturer"
CLIENT_IBZ = "Island events group"

# ---------------------------------------------------------------------------
# helpers used inside content
# ---------------------------------------------------------------------------

def flow(*nodes):
    """Horizontal flow of boxes with arrows; stacks on phones."""
    items = []
    for i, n in enumerate(nodes):
        if i:
            items.append('<span class="arr" aria-hidden="true"></span>')
        items.append(f'<span class="node">{n}</span>')
    return '<div class="flow">' + "".join(items) + "</div>"


def pair(left_title, left, right_title, right):
    return (
        '<div class="pair">'
        f'<div class="pane"><h4>{left_title}</h4>{left}</div>'
        f'<div class="pane"><h4>{right_title}</h4>{right}</div>'
        "</div>"
    )


def shot(caption):
    return f'<figure class="shot"><div class="shot-box"><span>Screenshot to add</span></div><figcaption>{caption}</figcaption></figure>'


def steps(*items):
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def bullets(*items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


# ---------------------------------------------------------------------------
# Case studies. Order here is the order on the home page.
# ---------------------------------------------------------------------------

CASES = [
    # 1 ------------------------------------------------------------------
    dict(
        slug="call-classification",
        glyph="route",
        title="AI call classification for a sales team",
        card="Every answered sales call is read, classified and written back onto the contact, with the closer's promise turned into a task.",
        client=CLIENT_BSUK,
        dates="July to September 2026",
        tools="GoHighLevel, Zapier, OpenAI, Google Sheets, WhatsApp",
        lede=(
            "After a sales call, the closer was meant to write up what was said, what was promised and when to follow up. "
            "In practice nothing was written down, promises were forgotten and leads went cold. I built a system that reads "
            "every call transcript, classifies the outcome, writes a structured note onto the contact and tells the right "
            "person what was promised."
        ),
        sections=[
            ("The problem",
             "<p>The CRM showed call transcripts on screen, but its own workflow engine could not read them. I tested every "
             "candidate transcript variable in a notification and each one came back blank. An existing call workflow was "
             "firing and producing nothing: no tag, no summary, no alert.</p>"
             "<p>The business needed every answered call read, classified and written back automatically, so the follow-up "
             "workflows could act on the outcome and the team could see a readable record without listening to recordings.</p>"),
            ("What I built",
             bullets(
                 "A twenty step automation that grew through seven published versions over the summer, one fault at a time.",
                 "The CRM workflow cut down to two steps: trigger on a completed call, then send the contact to the automation.",
                 "A structured call note written onto every contact: summary, outcome, product discussed, objections, next touch, what the closer promised, what the customer will do, then the full transcript.",
                 "A daily call log in a spreadsheet, a task for the closer carrying the promise, and a WhatsApp alert to me.",
                 "A one page explainer for the owner on how the classifier decides, and how to correct it.",
                 "A pre-call brief pinned to the contact's next appointment, so the closer sees it in the mobile app before dialling.",
             )),
            ("How it works",
             flow("Call ends", "CRM sends the contact", "Wait for the transcript", "Fetch it through the API",
                  "Flatten into speaker text", "AI classifies seven fields", "Note, task, sheet row, alert", "Outcome routes the follow-up")
             + "<p>The intelligence lives outside the CRM because the CRM cannot read its own transcripts. The automation "
             "waits for transcription to finish, then calls the CRM's API to find the right call message and pull the transcript. "
             "A code step flattens it into labelled speaker text, and the AI step receives only that, with fixed written "
             "instructions: work out which speaker is the salesperson and return exactly seven fields, with the outcome limited "
             "to one of four words.</p>"
             "<p>I proved every API endpoint in an API client before writing a line of automation. That became a standing rule "
             "after a one character typo in an endpoint caused three days of silent failures.</p>"),
            ("Problems I hit, and the fixes",
             bullets(
                 "<b>Daily error emails next to successful runs.</b> Very short calls have a message record but never a transcript. I added a found flag and a filter so those stop cleanly instead of erroring.",
                 "<b>Doubled surnames in alerts.</b> The full name had been written into the first name field on hundreds of contacts. I built a fallback chain for the alert name and exported the affected contacts for clean-up.",
                 "<b>A 24 minute call that never arrived.</b> Three faults stacked on one night: a trigger filter that depended on the field the automation itself fills, a wait step that stopped a second call enrolling, and two classifiers disagreeing on the spelling of one word. I removed the filter that night and verified fresh runs the next morning.",
                 "<b>Appointment notes refused by the API.</b> The integration token lacked one permission. Added, tested on a throwaway appointment, published.",
             )),
            ("Result",
             "<p>Every answered call that produces a transcript now leaves a readable note, a task with the closer's promise, "
             "a sheet row and an alert. The outcome drives two follow-up routers. The team told me they loved the note format, "
             "and from the last version the closer sees a pre-call brief on the appointment itself.</p>"),
        ],
        shots=[
            "A redacted call note as it appears on a contact: summary, outcome, promise, next touch, transcript below.",
            "The automation's step list, version 15, with the fault each version fixed written alongside.",
            "The one page explainer the owner received on how classification works.",
        ],
    ),

    # 2 ------------------------------------------------------------------
    dict(
        slug="live-transfer-lead-system",
        glyph="phone",
        title="A live transfer lead system for a Facebook ad campaign",
        card="Fourteen workflows that message a new lead, hold until the closer is online, ring a caller and hand the lead straight over.",
        client=CLIENT_BSUK,
        dates="August to September 2026",
        tools="GoHighLevel, Zapier, Conversation AI, WhatsApp templates, Fathom",
        lede=(
            "The first ad wave had shown that leads die when nobody calls promptly and stages rely on humans. The second wave "
            "had to call within business hours, route every outcome automatically, chase no-answers, book design calls and "
            "stay fenced off from the first wave's automations, which shared the same triggers."
        ),
        sections=[
            ("The problem",
             "<p>A caller needed to ring every new lead quickly and hand interested people straight to the closer. Everything "
             "around that call had to happen on its own: the first message, the wait until the closer was online, the chase if "
             "nobody answered, the booking, and the long tail of follow-up. And none of it could trip the live automations "
             "already running on the first wave.</p>"),
            ("What I built",
             bullets(
                 "An interactive planning board, a draggable sticky note page saved locally, which the owner and I used to agree an eight stage pipeline where seven stages move on system events and one needs a person.",
                 "The pipeline and fourteen workflows in their own folder, with a naming scheme and WhatsApp templates submitted for approval.",
                 "A twenty two workflow audit of what already existed, and a tag library of nine plain lowercase tags for the call team, delivered as paste blocks.",
                 "An AI booking agent audited and pointed at the right calendar, with autopilot held back until a tag gate existed.",
                 "An unclear call net: a 48 hour wait, an internal alert, and goal events that skip the alert if the lead resolves itself.",
                 "An interactive training manual for the call team, and a contact journey page for the owner covering all fourteen workflows.",
             )),
            ("How it works",
             flow("New lead from the ad", "Tag and opportunity", "WhatsApp, SMS fallback", "Hold until the closer is online",
                  "Ring the caller", "Caller presses a key to connect", "Outcome routes the next step")
             + "<p>The first workflow tags the lead, creates the opportunity and sends a WhatsApp with SMS and email fallback. "
             "It then waits until the weekday afternoon window when the closer is online, and only then rings the caller, who "
             "presses a key to connect the lead. A second workflow routes connected versus not connected calls. Two routers "
             "receive the outcome from the call classification system and send warm, cold and unclear leads down different "
             "paths. Others nurture warm leads, chase no-answers over two rounds, handle bookings behind a tag gate, and run the "
             "long tail: showroom visits, natural silence, estimate chasing. If the caller transfers a lead, one tag stops the chase.</p>"),
            ("Decisions that mattered",
             bullets(
                 "Treat the whole build as build-only until reviewed with the owner, so nothing went live half finished.",
                 "Fence every workflow on the wave's tag. A live workflow from the first wave was found moving every answered call into the wrong pipeline, and was gated.",
                 "Set goal events to continue anyway, so a lead that resolves itself skips the alert and an unresolved one exits cleanly.",
                 "On launch day, publish the new intake and set the old one to draft seconds apart, accepting a brief double handle over dropped leads.",
             )),
            ("Result",
             "<p>The wave went live on 23 September with live transfers to the closer. A week later the same calling "
             "infrastructure was reused to work the old backlog, with automated messaging fenced off, dripping one contact "
             "every five minutes.</p>"),
        ],
        shots=[
            "The draggable planning board used to agree the pipeline with the owner.",
            "The contact journey page: all fourteen workflows on one page for the owner.",
            "The call team's interactive manual with tick boxes and a progress bar.",
        ],
    ),

    # 3 ------------------------------------------------------------------
    dict(
        slug="self-moving-pipeline",
        glyph="pipeline",
        title="Making a lead pipeline move itself",
        card="An eleven stage pipeline that only moved when someone dragged a card, rebuilt so every stage moves on a system event.",
        client=CLIENT_BSUK,
        dates="July to September 2026",
        tools="GoHighLevel, Meta lead forms, WhatsApp Business templates",
        lede=(
            "The ad pipeline had eleven stages that only moved when a person dragged a card, and nobody did. By September "
            "hundreds of leads sat in it and roughly four in five were stranded in two stages with nothing chasing them. "
            "I made every stage move on the event that causes it, and built a gated sweeper to recover the backlog."
        ),
        sections=[
            ("The problem",
             "<p>Lists built on stages were unreliable for the same reason the stages were: nobody moved cards. Along the way "
             "I found that the default WhatsApp sender had never been set, so every automated WhatsApp in every workflow had "
             "been failing silently, and that the missed call workflows were telling people we had tried to call after real "
             "conversations had already happened.</p>"),
            ("The rule everything hangs on",
             pair("Stages", "<p>Position only. One stage per contact, set by the workflow that causes the event. The single source of truth for where someone is.</p>",
                  "Tags", "<p>Facts. Where a lead came from, whether they are in a live conversation, whether they asked not to be contacted. Short lived signals that cross stages.</p>")
             + "<p>No manual tagging as a mechanism, because the team would not apply tags reliably. Every branch reads system "
             "data instead: appointment status, call direction, delivery status.</p>"),
            ("What I built",
             bullets(
                 "A stage move inside every workflow that causes an event: the intro message, a reply, a booking, a missed call, a call outcome.",
                 "A reply detection workflow that works on any channel, after the original only caught WhatsApp replies to one workflow.",
                 "Missed call workflows rebuilt into multi touch chases that stop the moment someone books.",
                 "A tag gate on bookings so repeat appointment events exit silently, because the CRM has no created-only trigger.",
                 "A follow-up call system: an AI summary of each call into a note, nudges at day five and day seven, and keyword tagging from a controlled vocabulary.",
                 "A catch-up sweeper with a multi condition safety gate and three limbs, one per stranded group, with reused approved copy.",
             )),
            ("How the sweeper works",
             flow("Enrol a batch by hand", "Safety gate", "WhatsApp touch", "Wait for a reply", "Booking email", "Long shot list")
             + "<p>The sweeper is enrolled in batches during business hours, oldest and coldest group first. Its gate skips anyone "
             "currently in conversation, already booked, already classified or already spoken to by a person. Anything it "
             "cannot revive moves to a long shot marketing list rather than sitting in a sales stage.</p>"),
            ("Result",
             "<p>The pipeline moves itself for every system event, replies move contacts on any channel, missed calls are chased "
             "without a person, and the stranded backlog has an automated, gated recovery path. The pipeline count reflects "
             "reality for the first time.</p>"),
        ],
        shots=[
            "The pipeline map: eleven stages, with the workflow that sets each one.",
            "The sweeper workflow with its safety gate expanded.",
            "Before and after counts on the two stranded stages.",
        ],
    ),

    # 4 ------------------------------------------------------------------
    dict(
        slug="design-system",
        glyph="swatch",
        title="A design system that checks itself before every build",
        card="One master file, eleven versions, two automated gates and a delivery checklist, so pages, emails and proposals stop drifting.",
        client=CLIENT_BSUK,
        dates="July to September 2026",
        tools="HTML and CSS, Python, Playwright, GitHub Pages, GoHighLevel email templates",
        lede=(
            "When I started, the brand lived in a Word document with the wrong greens, the wrong fonts and a placeholder "
            "company name in the title. Every page, email and proposal was being built without a stable reference, so every "
            "session drifted. I built a living design system that every build reads first, and two automated checks that run "
            "on every file before anyone sees it."
        ),
        sections=[
            ("The problem",
             "<p>Off palette colours, retired fonts, square buttons in one file and round in another. The deeper problem "
             "surfaced later: a rulebook full of hex codes and banned words produced pages that passed every check and still "
             "looked flat. The pieces I loved most, the line drawings, the white lift cards, the circle photo inserts, kept being "
             "left out because nothing required them. I needed a system that both stopped bad output and forced the good parts in.</p>"),
            ("Eleven versions, one lesson each",
             steps(
                 "Audit and rebuild the brand kit from the live site. Correct the greens, name the fonts, flag a wrong font on the two highest intent forms.",
                 "A machine readable spec with bounded bold and italics, a wider palette and a changelog.",
                 "Ten visual directions behind toggle buttons. I chose a white ground with structural hairlines and graduated green fields, and retired two colours for good.",
                 "Three named page templates. The file was accidentally deleted, so one was rebuilt from memory and labelled as a reconstruction.",
                 "A bold exploration: five further directions. I decided not to add a fourth template.",
                 "Written from a fourteen screenshot mood board. All templates stripped out, leaving rules plus a component shelf. Creative direction defined in one sentence.",
                 "White as the default surface, body weight up from 300 to 400. Rebuilt as a rendered HTML document with live swatches and specimens.",
                 "A full proposals chapter modelled on a real proposal. Hard rules: every button fully rounded, every emoji inside a centred disc, the accent colour never on a green tint.",
                 "Signature components and a delivery checklist. The accent colour split three ways so email pills, page buttons and accents on dark each have one correct value.",
                 "One merged master that absorbs the email library and every rule, with one stable filename forever and the version number inside the file.",
             )),
            ("The two gates",
             pair("What must not be there", bullets("Retired hex values", "Em and en dashes", "Banned words and the old domain", "Retired fonts", "The founder's real name in customer material", "Unbalanced tags"),
                  "What must be there", bullets("Four tickable lists, one per document class", "State saved in the browser", "A Not needed button on every row", "A skip recorded as a decision, never raised again on that build"))
             + "<p>The first gate is a script that greps every HTML file before it is presented. The second is a checklist, "
             "because one universal list fails every email. I wrote it to ask rather than argue: I needed reminding, not overruling.</p>"),
            ("The order of authority",
             "<p>The master file states its own order of authority: the copy rules first, then my direct instruction, then the "
             "live refined pages and emails, then the document itself. If a new build matches the document but does not feel "
             "like the live pages, the build is wrong.</p>"),
            ("Result",
             "<p>By the end of September the brand had one authoritative, self demonstrating document that every build session "
             "reads first, two automated gates, and a checklist with recorded skips. The live estimate pages, emails, proposals "
             "and deposit page all build from it. The repeated frustration of forgotten components and drifting colours was the "
             "trigger; a single file plus a checklist was the structural fix.</p>"),
        ],
        shots=[
            "The original brand kit palette beside the final token board.",
            "The ten direction comparator from version four, with the toggle buttons.",
            "The delivery checklist with a Not needed skip in action.",
            "A pre-flight report line: one grep result and one tag balance count.",
        ],
    ),

    # 5 ------------------------------------------------------------------
    dict(
        slug="custom-proposals",
        glyph="page",
        title="Proposal pages built around the customer's own questions",
        card="Custom proposal pages with AI renders of the customer's actual garden, two option estimates, and a drag and drop tool that made the renders repeatable.",
        client=CLIENT_BSUK,
        dates="September 2026",
        tools="HTML and CSS, Gamma, Playwright, GitHub Pages, vanilla JavaScript",
        lede=(
            "A holiday let owner booked a call with a nine point checklist he would score suppliers against. A homeowner wanted "
            "renders and specs the same day, from a thirty six second phone video of his garden. For both I built a custom "
            "proposal page that answered their questions in their order, and then built a tool so the renders stopped taking "
            "five attempts."
        ),
        sections=[
            ("The checklist proposal",
             "<p>Each of the nine questions was sorted into two groups: answered from approved copy, or not yet in approved copy. "
             "The second group was checked against the spec sheet and warranty documents before anything reached the owner. "
             "Two build options sit side by side at the same length and price, each with its own render set, and the price "
             "sits at the very bottom so the content is read before the number.</p>"
             + flow("Nine questions", "Sorted by source", "Checked against documents", "Mapped to page sections", "Two options side by side", "Price last")
             + "<p>Competitor catalogue images could not be used, so the second option was remade as our own renders, using the "
             "catalogue only as a reference. Origin claims were kept honest: the handcrafted copy stayed on the option that earned it.</p>"),
            ("The same day proposal",
             "<p>I pulled stills from the customer's video, cleared the scene, then placed the sauna and ice bath on his actual "
             "concrete pad. The image model kept inflating the pad and shrinking the sauna, so I used an object already in the "
             "photo as a ruler, then described sizes as ratios the model could hold. When it kept drawing the wrong heater, I "
             "stopped rendering and added a callout bubble over the image naming the real one.</p>"
             "<p>When the sales call came back with two objections, no interior photos and a higher price than expected, the "
             "page answered with new interior renders. When the customer changed his mind about the building twice in a week, "
             "it became a two option page within two days, carrying the original build as option one rather than overwriting "
             "what had already been approved.</p>"),
            ("The fix that made it feel right",
             pair("Before", "<p>Every element sat in the same boxed column width. Correct, and flat.</p>",
                  "After", "<p>The After render runs edge to edge. The Before became a thin strip above it. Each card grid leads with a full width feature card. Two interior views carry one split sentence across them, rain on the left, sunset on the right.</p>")),
            ("The layout tool",
             "<p>Getting a bath deck and a sauna into the right place in a render had cost five passes in one evening, because "
             "generative tools give no control over where things land. So I built an internal page: load a ground photo, add "
             "product cutouts, drag them into place, export at full resolution, then give the image one relighting pass. Every "
             "product is rendered once at a standard angle and light, so pieces from different jobs sit together believably. "
             "It went live the day after the idea and became the first step of every custom render.</p>"),
            ("Result",
             "<p>The checklist proposal went live within about a day and became my reference format for later jobs. The same "
             "day proposal went out when it was promised, answered the sales objections, and its structure, view hero, full "
             "bleed after, dream band, two option estimate, became the template for the proposals that followed.</p>"),
        ],
        shots=[
            "The raw video still beside the final After render, prices and names removed.",
            "The two option layout on desktop and on a phone.",
            "The heater callout bubble over the render.",
            "The layout tool: a ground photo with two pieces placed, before the relight pass.",
        ],
    ),

    # 6 ------------------------------------------------------------------
    dict(
        slug="playbook-and-manual",
        glyph="book",
        title="A sales playbook and a role based CRM manual",
        card="Twenty one script cards from the founder's own words, real call examples, and one CRM manual gated by role instead of a guide per person.",
        client=CLIENT_BSUK,
        dates="July to September 2026",
        tools="HTML, CSS and JavaScript, GitHub Pages, ffmpeg, inline SVG, localStorage",
        lede=(
            "The founder's sales knowledge lived in his head, in voice notes and in meeting rants. New closers had nothing "
            "consistent to say, product rules were being broken, and nobody had been trained on the CRM. I built a single "
            "file playbook from his own transcripts, then a CRM manual that gates its chapters by role."
        ),
        sections=[
            ("The playbook",
             "<p>Twenty one cards from open to close. Each card has what to say, the move behind it, and an anecdote box "
             "written as a prompt to adapt rather than an invented line. The scripts are verbatim from transcripts: I stopped "
             "the AI inventing lines attributed to real people. Five tabs sit over the cards: scripts, questions and answers, "
             "fast facts, the deposit gate, and live call examples with annotations tied to the cards they illustrate.</p>"
             "<p>One update alone was thirty nine edits from a document and a meeting transcript, all resolved from the "
             "transcript without a single question to the founder. Five call recordings were converted for the web at a "
             "fraction of their size with no audible loss. Later the same knowledge became a partner guide with the scripts, "
             "pitch language and internal warnings removed.</p>"),
            ("The manual",
             pair("What was there", "<p>Separate guides per person, multiplying. Early drafts that talked down to capable colleagues. Nobody logging in as themselves, so actions were not attributed.</p>",
                  "What I built", "<p>One manual gated by role: office, sales and call team. A login gate in the first chapter that stays locked until the reader types their own login name. Fourteen captioned screenshots. A global tone rule: readers are capable adults with normal jobs, so never explain the obvious.</p>")
             + "<p>The call team's version is interactive: per section tick boxes, notes that save in the browser, a progress "
             "bar and print to PDF. Its content was corrected against the sixteen live workflows before it went out.</p>"),
            ("Decisions that mattered",
             bullets(
                 "One manual by role, not by person. It avoids condescension and gives one source of truth.",
                 "Teach the why behind the rules, not basic clicks, for staff who already use the CRM daily.",
                 "A generic closer voice in the scripts, with the founder's customer facing name kept only as a real third person reference.",
                 "Live HTML previews instead of image slices, because nobody can zoom into a picture of a page.",
             )),
            ("Result",
             "<p>Closers have one living playbook with real call examples and the product rules explained. The same knowledge "
             "powers a partner guide. One maintained, role based manual replaced the per person guides, and the call team had "
             "an accurate, interactive guide in time for the campaign launch.</p>"),
        ],
        shots=[
            "The playbook: hero, tabs, the progress rail and the hand drawn chip icons.",
            "One script card dissected: say, move, anecdote prompt.",
            "The role picker and the login gate in the manual.",
            "A playbook card next to its partner guide equivalent, showing what was removed.",
        ],
    ),

    # 7 ------------------------------------------------------------------
    dict(
        slug="content-plan",
        glyph="grid",
        title="A filming plan from 61 meeting recordings",
        card="Every content idea from three months of calls, turned into a page the founder could take into a meeting and onto a filming day.",
        client=CLIENT_BSUK,
        dates="September 2026",
        tools="Fathom, Claude with parallel agents, HTML and JavaScript, Google Apps Script, Google Sheets",
        lede=(
            "The founder was meeting a videographer and wanted every content idea the team had ever discussed in one place. "
            "Those ideas were scattered across sixty one recorded calls, and the ones said in passing never reached the call "
            "summaries. I read the transcripts, then built a page he could decide from, carry onto a filming day, and have his "
            "decisions captured without anyone retyping notes."
        ),
        sections=[
            ("The research pass",
             flow("61 recordings", "Six parallel agents, full transcripts", "Project chats swept", "Merged with two existing lists", "63 ideas in eight themes")
             + "<p>Speaker labels in the recordings were unreliable, so every idea was attributed by content rather than by "
             "speaker. Fourteen recordings turned out to be test clips or held no content talk.</p>"),
            ("Twelve versions in a week",
             "<p>The first version had everything: filters, ticks, search, tags, timestamped links back to the moment each idea "
             "was said. It overwhelmed the reader. So I rebuilt it as a plain grouped list with ten ideas to start with. Then "
             "the founder liked the idea of filming days, so it became four days with a shot list each, plus everything else on "
             "an end page, because I did not want to decide for him or cut anything.</p>"
             "<p>Then print sheets inside the same file: one A4 sheet per day with tick boxes and a ruled notes box, sized by "
             "measuring the spare space so the box never spilled onto a new page. Then a floating plan panel that fills as "
             "shots are ticked, with timestamped notes and one email button. Then a live backend.</p>"),
            ("How the backend works",
             flow("Tick or note on any device", "Saved in the browser", "Sent to a script", "Upserted into a sheet", "Reloaded on every device", "Email on demand")
             + "<p>Ticks and notes save locally first, then post to a small web app that upserts rows into two sheet tabs under "
             "a lock. On page load the same app returns everything, so the plan matches on phone and laptop. The email button "
             "sends a structured payload and the script builds a designed email: a count strip, each note as its own card, "
             "the ticked shots grouped by day, and a button to open the sheet. If the sheet is unreachable the page falls back "
             "to the browser and a plain mail link.</p>"),
            ("Result",
             "<p>Sixty one unread recordings became a live, tested page the founder used. He liked the day structure, the "
             "running panel and the notes, and the day sheets got printed because the new unit has a printer. On the call "
             "where I demoed it he proposed the next step himself: a hub that joins the plan to order dates, so content is "
             "planned when a deposit is paid rather than forgotten. I specced it the same evening.</p>"),
        ],
        shots=[
            "The first version beside the four day version.",
            "The floating plan panel with timestamped notes.",
            "A printed day sheet with tick boxes and a script under a shot.",
            "The designed email that lands after the meeting.",
        ],
    ),

    # 8 ------------------------------------------------------------------
    dict(
        slug="website-rebuild",
        glyph="browser",
        title="Rebuilding a Wix site without losing its search ranking",
        card="A hybrid of native Wix text and custom HTML embeds, plus the funnel audit that found enquiries vanishing between the website and the CRM.",
        client=CLIENT_BSUK,
        dates="July to August 2026",
        tools="Wix Editor and Velo, HTML, CSS and JavaScript, GoHighLevel, Playwright, Python",
        lede=(
            "The live site looked like a template, had fourteen menu items, and its key product pages were image tiles with "
            "the words baked into the pictures, so search engines could read none of it. The owner's first question was "
            "whether custom HTML inside Wix would hurt search. That question shaped the whole architecture."
        ),
        sections=[
            ("The architecture",
             pair("Native Wix layer", "<p>All search copy, headings and the main calls to action live in native text, so credit stays on the brand's own domain and analytics can see the clicks.</p>",
                  "Embed layer", "<p>Only the visual chrome: video heroes, layered images, card rows. Nine transparent embeds on the homepage, each positioned independently, because stacked frames could not overlap the hero.</p>")
             + "<p>Embed buttons talk to the page through a short message and a few lines of site code, which open the native "
             "enquiry popup. An enquiry form that renders at a fixed width sits inside a wrapper that measures the box and "
             "scales it to fit. Media queries live inside each embed rather than in the editor's mobile view, because in the "
             "classic editor deleting something in mobile view deletes it on desktop too.</p>"),
            ("What I built",
             bullets(
                 "Navigation trimmed from fourteen items to six plus a dropdown, with the header floated over a full bleed video hero.",
                 "A row of six upright product cards with mirrored heights, tallest at the edges, forming a shallow curve.",
                 "An in stock page rebuilt as alternating editorial rows with real, crawlable copy around the images.",
                 "A layered hero for the mobile range: a landscape, oversized lettering, and a background removed trailer sitting in front of the letters.",
                 "A review pack for the owner: twelve pairs of current and proposed screenshots, with the images shrunk from about 29MB to under 4MB.",
                 "Mobile clean up: three separate WhatsApp entry points reduced to one, a duplicate chat widget removed.",
             )),
            ("The leak audit",
             "<p>While the rebuild was under way I found enquiries vanishing. One form had been landing only in the website "
             "inbox for weeks with no CRM contact. A prospect submitted the design form three times and none appeared on a "
             "contact. Paid search leads had never reached the CRM at all.</p>"
             + flow("Website form", "Automation posts six fields", "CRM webhook", "Create or update the contact", "Tag, opportunity, follow-up")
             + "<p>The design form had three faults from one edit: no create or update contact step, so the CRM ran its "
             "workflow with no contact attached; a goal that ended the workflow after the first alert, so the follow-up had "
             "never run; and one field missing from the mapping. All three fixed, and a rule written down: every inbound "
             "webhook workflow starts with create or update contact.</p>"),
            ("Result",
             "<p>A rebuilt homepage and product pages with a consistent look, real crawlable copy, working enquiry popups and a "
             "review pack that let the owner compare old and new side by side in a three hour walkthrough. Website enquiries "
             "now create contacts and enter follow-up, and a long broken form ran its full sequence for the first time.</p>"),
        ],
        shots=[
            "Before and after homepage, from the review pack.",
            "The product card row sketch next to the built row.",
            "The layered mobile range hero.",
            "The leak map: each form, where it was landing, and the fix.",
        ],
    ),

    # 9 ------------------------------------------------------------------
    dict(
        slug="instant-booking-page",
        glyph="ticket",
        title="An instant booking page sent as a WhatsApp link",
        card="One mobile first page that sells a transfer and lets the client book and pay, with the risky cases fenced off to a conversation.",
        client=CLIENT_IBZ,
        dates="September 2026",
        tools="HTML, CSS and JavaScript, GitHub Pages, Gamma, Python, Playwright",
        lede=(
            "Every quote left as a PDF the client could not act on, so each sale needed a second message asking them to go "
            "and pay. I wanted one branded page I could drop into a WhatsApp chat that sold the transfer and let the client "
            "book and pay, with no server code and no domain changes."
        ),
        sections=[
            ("What I built",
             bullets(
                 "A single mobile first page on free static hosting, with link preview tags so it unfurls as a card in WhatsApp.",
                 "A full bleed hero from an AI render of a branded minibus, with the darkening veil applied in CSS rather than baked into the image, and two saved veil strengths.",
                 "Feature cards inside a dark night strip, a video row that stacks on phones, fleet and group sections, and a cross sell to the sister brand.",
                 "An instant booking form with zone based pricing from the supplier rate card, two fixed price bands, a night surcharge, a 48 hour notice fence and a blocked dates list.",
                 "A transparent logo cut out in Python, after the supplied file turned out to have a picture of transparency baked into its pixels.",
             )),
            ("How the booking logic works",
             flow("Pick up and drop off", "Mapped to supplier zones", "Band by zone and time", "Fence checks", "Pay, or WhatsApp")
             + "<p>The higher band applies if either end is in the outer zones or the pick up is in the small hours. Both bands "
             "are priced against the most expensive supplier's cost, so if the cheaper supplier is busy the margin shrinks but "
             "never goes negative. Unknown locations, large groups, short notice and blocked dates all route to a WhatsApp "
             "message instead of payment. Payment itself stays in the existing store: one pre built product per band, so the "
             "store never needs a custom amount.</p>"),
            ("Small things that took real work",
             bullets(
                 "On phones two videos stayed side by side because the mobile rule sat above the desktop rule in the stylesheet. Moving it fixed the cascade.",
                 "A finished video left the client stuck in a black full screen player. An ended handler now exits full screen and reloads the poster, and a play handler pauses any other video.",
                 "Photos were being cropped too hard. They now show at their uploaded proportions, and never crop unless told became a standing rule.",
                 "Replacing an embedded hero with a hosted one cut the file from about 231KB to about 26KB.",
             )),
            ("Result",
             "<p>The page went live and became the pattern for the brand's shareable pages. Several working standards came "
             "out of it: AI heroes allowed, veils applied in CSS, never crop, and always send the standalone file alongside "
             "the preview.</p>"),
        ],
        shots=[
            "The page on a phone, hero to booking form.",
            "The hero under the light veil and the heavy veil.",
            "The logo with the baked in checkerboard beside the clean cut out.",
        ],
    ),

    # 10 -----------------------------------------------------------------
    dict(
        slug="lead-forms-crm",
        glyph="form",
        title="Lead forms wired into a CRM for two brands",
        card="A booking form that arrived with blank phone numbers and the wrong times, a dead homepage form, and a sister brand with no lead capture at all.",
        client=CLIENT_IBZ,
        dates="August to September 2026",
        tools="WordPress and Elementor, Ecwid, GoHighLevel, HTML email, JavaScript, Python",
        lede=(
            "Transfer enquiries were arriving with a blank phone number and a pick up time that matched the moment of "
            "submission rather than the time the customer chose. A second form on the homepage posted to a webhook nothing "
            "was listening to. The sister brand's site had no lead capture beyond a chat widget bound to someone else's account."
        ),
        sections=[
            ("The diagnosis",
             bullets(
                 "<b>Wrong times.</b> The form builder sends its own metadata item called Time, the moment of submission, which overwrote the customer's field of the same name. Renamed the field.",
                 "<b>Blank phone.</b> The webhook sent the number under a WhatsApp key the CRM does not treat as a phone. Mapped it into the standard phone field.",
                 "<b>Fields that would not match.</b> Two labels had a trailing space, visible only in the raw payload. Retyped them and repointed the trigger's sample.",
                 "<b>Lost homepage enquiries.</b> The short form posted to a second webhook with no workflow behind it. Retired it and replaced it with a tile strip and one WhatsApp button that route to the single full form.",
                 "<b>Unanswered contacts.</b> A contact form workflow had been sitting in draft with dozens of enrolled contacts who never got a reply.",
             )),
            ("The flow, once fixed",
             flow("Form submitted", "Webhook with every field", "Create the contact", "Opportunity in the pipeline", "Customer email", "Internal email with a WhatsApp button", "Sister brand intro after fifteen minutes")
             + "<p>The customer autoresponder is a table based HTML email with a full bleed hero, three summary pills and the "
             "request details. The internal email lists every field, gives a one tap WhatsApp button with an opening line "
             "already typed, and carries a plain card I can screenshot to a supplier to check availability, showing only a "
             "first name. Emoji are stored as numeric entities so the CRM editor cannot garble them.</p>"),
            ("The sister brand form",
             "<p>The site builder offered only a chat widget, so I built a custom form: fifteen real products grouped into five "
             "categories, a hidden honeypot for spam, and a submit handler that posts straight to the CRM webhook and offers a "
             "WhatsApp fallback if it fails. The embed script inserts the form above a named section of the page, with a "
             "fallback position. The email service stripped the hero's CSS fade, so the fade is baked into the image pixels "
             "in Python instead.</p>"),
            ("Result",
             "<p>A test submission confirmed every booking form field landing on the contact, including pick up time and "
             "luggage. The homepage strip went live and the buttons all worked. The sister brand form passed an end to end "
             "test, with the internal notification arriving fully populated.</p>"),
        ],
        shots=[
            "The internal notification email: details list, WhatsApp button and supplier card.",
            "The raw test payload with the metadata Time item and the two trailing spaces marked.",
            "The homepage before and after: dead short form, then the frosted tile strip.",
            "The sister brand form with its grouped product picker.",
        ],
    ),

    # 11 -----------------------------------------------------------------
    dict(
        slug="brand-kits",
        glyph="chips",
        title="Brand kits and a branded document system",
        card="Two brand kits that demonstrate their own rules, a card catalogue with an emoji colour test, and confirmations and tickets built for a WhatsApp chat.",
        client=CLIENT_IBZ,
        dates="July to September 2026",
        tools="HTML and CSS, Python, Playwright, Shopify, GitHub Pages",
        lede=(
            "The design templates for two brands were old and inconsistent, and every new document was styled from scratch. "
            "I built one brand kit per brand as a single page that demonstrates every rule live, then a family of documents "
            "that all build from it: catalogue cards, quotes, product pages, confirmations and an e-ticket."
        ),
        sections=[
            ("The kits",
             "<p>Each kit is one HTML page. The logo section shows three assets with one job each, plus clear space and never "
             "do rules. The colour section pairs every swatch with its job. The type section sets a scale with fallbacks. The "
             "component library is rendered live, so a component is copied rather than described: hero with veil, pills row, "
             "status banner, gradient card, item card, price line with caveat, sign off.</p>"
             "<p>Two rules worth naming. Emoji are the only icon system, with a banned list of the ones that render in "
             "monochrome and a colour test for any new one. And the voice has two registers, one for the girls and one for the "
             "lads, with shared rules: sentence case, literal language, short sentences, no dashes.</p>"),
            ("The catalogue cards",
             "<p>Twenty one activity cards at a fixed size with transparent margins, one per activity, coloured by its product "
             "family so the files sort themselves into folders. The style layers grain, a faint oversized ghost emoji bleeding "
             "off a corner, mesh gradients and a dark scrim behind the text.</p>"
             + flow("Render the emoji alone in a browser", "Count saturated pixels", "Pass or ban", "Swap for a tested alternative")
             + "<p>The emoji test came from a real failure: several cards showed white blocks where emoji should be, because "
             "those glyphs have no colour version in the font. Every emoji is tested before it goes on a card.</p>"),
            ("Documents built for a chat",
             bullets(
                 "Booking confirmations rendered as one tall PDF page, with a contact card and a green WhatsApp button that opens a prefilled message to the driver or host.",
                 "Reminder cards for the client and a matching card for the driver.",
                 "A landscape e-ticket for venue bookings, after a portrait version shrank to an unreadable strip in the chat. Every detail lives in one block at the top of the template, filled in by a short script.",
                 "Product pages in three brand skins with deposit, balance and full payment variants, where the balance page is derived from the deposit page so the two always match.",
             )),
            ("Result",
             "<p>Both kits were delivered the same day and one became the only design source for its brand. The emoji ban "
             "list was written into the kits as a standing rule. The confirmation layout became a saved template, and later "
             "documents were built by swapping names, dates and figures in an existing file.</p>"),
        ],
        shots=[
            "The two kits' hero sections side by side.",
            "A grid of the catalogue cards grouped by colour family.",
            "A client reminder card next to the driver's card.",
            "The rejected portrait ticket beside the landscape one, inside a chat.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# The full list: every project, one line each.
# ---------------------------------------------------------------------------

ALL_WORK = [
    (CLIENT_BSUK, "July to October 2026", [
        ("CRM and automation", [
            ("AI call classification and routing for a sales team", "call-classification"),
            ("Stage automation and backlog recovery for a Facebook lead pipeline", "self-moving-pipeline"),
            ("Building and launching a live transfer ad lead system", "live-transfer-lead-system"),
            ("Turning a deposit payment into a reliable CRM event", None),
            ("Booking calendar clean up and notification rebuild", None),
            ("Finding and fixing silent lead loss across web, social and ad forms", "website-rebuild"),
        ]),
        ("CRM, alerts and operations", [
            ("Stopping automated messages from interrupting live conversations, and catching silent failures", None),
            ("Rebuilding a sales team's cloud phone setup: voicemail, live transfer and emergency routing", None),
            ("Moving a CRM's email off a blocklisted shared pool onto a dedicated authenticated subdomain", None),
            ("A mobile handover and sign off form for installers, with dual signatures and an on device PDF", None),
            ("Getting the right context to the right person before every sales call", None),
            ("Connecting an AI assistant directly to a CRM, then scoping a custom connector for the gaps", None),
            ("Turning recorded meetings into action lists, briefs and call prep", None),
            ("Turning a founder's late night message streams into structured, trackable jobs", None),
            ("Consolidating a team's scattered WhatsApp groups into one structured community", None),
        ]),
        ("Email and sales tools", [
            ("One fluid email master for a thirty plus email CRM library", None),
            ("Customer lifecycle emails from enquiry to deposit and build", None),
            ("Branded email signature and deposit banner", None),
            ("Sales playbook site and partner product guide", "playbook-and-manual"),
            ("Live estimate builder for sales calls", None),
            ("Role based CRM manual for office, sales and call team", "playbook-and-manual"),
            ("White label partner seller pack", None),
        ]),
        ("Web", [
            ("Homepage and multi page rebuild of a Wix website using native elements and custom embeds", "website-rebuild"),
            ("Standalone product pages for a hot tub range, a two person tub, a glamping pod and a hut range", None),
            ("A step by step product configurator that feeds a CRM, with matching customer and team emails", None),
            ("A deposit checkout page embedded in a Wix site", None),
            ("Post estimate and post deposit customer journey pages and emails", None),
            ("SEO blog content and the hosting decision behind it", None),
        ]),
        ("Custom proposals", [
            ("Shepherd's hut and mobile sauna commission", None),
            ("Lochside sauna and hot tub proposal", None),
            ("Commercial floating sauna proposal and reusable template", None),
            ("Indoor wellness fit out pre install specification and estimate", None),
            ("Grant application estimates and a commercial wellness suite proposal", None),
            ("A garden sauna and ice bath proposal built from a phone video, rebuilt to a new spec", "custom-proposals"),
            ("A bespoke garden treatment room with a panoramic dome window", None),
            ("A two option sauna proposal for a coastal holiday let owner", "custom-proposals"),
            ("A wellness area proposal for a holiday park, built for a grant application", None),
            ("A poolside sauna and steam room proposal for a partner seller's client", None),
            ("A one page cold plunge range brochure", None),
        ]),
        ("Brand, design and imagery", [
            ("A living design system, versions three to eleven", "design-system"),
            ("A matched set of product line drawings for every document", None),
            ("Exploring a brand mascot", None),
            ("Signage mock ups for a new workshop unit", None),
            ("Concept landing pages and a range backbone for a sister brand", None),
            ("A repeatable AI image and video pipeline for product marketing", None),
            ("Scripted image finishing: cutouts, colour grading and realism passes", None),
            ("A drag and drop scene builder for custom build proposals", "custom-proposals"),
        ]),
        ("Marketing and content", [
            ("A filming plan from three months of meeting recordings", "content-plan"),
            ("Print collateral for a trade expo: pamphlet, fold viewer, photo picker and booklet storyboard", None),
            ("Rebuilding customer aftercare, handbook and warranty paperwork", None),
            ("A WhatsApp ready spec card and product knowledge checks", None),
        ]),
    ]),
    (CLIENT_IBZ, "June to October 2026", [
        ("Websites and shareable pages", [
            ("An instant booking page for a transfer brand, shared as a WhatsApp link", "instant-booking-page"),
            ("An evergreen mini brochure from an eighty three page source", None),
            ("Website concepts and a brand refresh proposal", None),
            ("Guided review request pages that draft the review for the client", None),
        ]),
        ("CRM, forms and automation", [
            ("Booking form, CRM mapping and email rebuild for a transfer brand", "lead-forms-crm"),
            ("Lead form, CRM routing and chat widget repair for a sister brand", "lead-forms-crm"),
        ]),
        ("Branded document system", [
            ("Brand kits for two brands", "brand-kits"),
            ("Reusable sales templates and one page WhatsApp brochures", None),
            ("An activity catalogue card system with an emoji colour test", "brand-kits"),
            ("Branded quote documents with exact page counts", None),
            ("Product pages for deposits, balances and full payments", "brand-kits"),
            ("Booking confirmations and reminder cards with tap to message buttons", "brand-kits"),
            ("A reusable WhatsApp e-ticket for venue bookings", "brand-kits"),
            ("Bespoke trip itinerary pages", None),
        ]),
        ("Backend and tooling", [
            ("Euro checkout for a bookings store", None),
            ("Image utilities for marketing and email assets", None),
            ("Working standards for building with an AI assistant", None),
        ]),
    ]),
]
