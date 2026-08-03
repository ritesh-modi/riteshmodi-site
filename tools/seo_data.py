# -*- coding: utf-8 -*-
"""Hand-written share metadata, one entry per page.

These are deliberately NOT generated from the first paragraph. A meta description
is ad copy for a search result: it has to say what you *do* on the page, because
"you can drag this and watch it change" is the only thing that distinguishes an
explorable from the twenty blog posts above it in the results.

  desc   140-160 chars, unique, names the interaction. Shown in search results.
  short  <=110 chars for OG/Twitter cards, which truncate harder than Google.
         Omit to reuse desc.
  about  the schema.org `about` Thing - the subject, not the title.

Everything else (date, topic, level, title) is read from the cards in
explorables.html so there is exactly one place to change it.
"""

SITE = "https://www.loopingly.com"
AUTHOR = "Ritesh Modi"

# Top-level pages -------------------------------------------------------------
PAGES = {
    "index": dict(
        desc="Interactive explainers on how AI actually works — each one a single page "
             "you learn by dragging, poking and breaking, not by watching a video.",
        about="Artificial intelligence",
    ),
    "explorables": dict(
        # was: "Interactive, explorable explorables you learn by messing with" — the
        # word appeared twice in nine words.
        desc="Interactive explainers on AI, databases and distributed systems — each a "
             "single page you learn by dragging, poking and breaking. Search and filter them.",
        about="Interactive explorable explanations",
    ),
    "about": dict(
        desc="Ritesh Modi — Head of AI, Microsoft Regional Director, and author of eight "
             "books on cloud and machine learning. What I work on and why I build these.",
        about="Ritesh Modi",
    ),
    "books": dict(
        desc="Eight published books on generative AI, cloud architecture and machine "
             "learning, from Packt and Apress — what each one covers and who it is for.",
        about="Books by Ritesh Modi",
    ),
    "talks": dict(
        desc="Conference talks and workshops on generative AI, Azure architecture and "
             "applied machine learning, with slides and recordings where available.",
        about="Technical talks",
    ),
}

# Explorables -----------------------------------------------------------------
EXPLORABLES = {
    "ai-transformation-explainer": dict(
        desc="Efficiency projects pay back once; reinvention changes what the business "
             "sells. Move the sliders to see which one your AI portfolio is really funding.",
        short="Move the sliders to see whether your AI portfolio funds efficiency or reinvention.",
        about="AI-driven business transformation"),

    "ai-vs-ml-explained": dict(
        desc="Automation, machine learning and AI all watch, decide and act. Flip one "
             "thermostat between all three and see exactly where rules stop and learning starts.",
        short="Flip one thermostat between automation, ML and AI, and see where rules stop.",
        about="Difference between automation, machine learning and artificial intelligence"),

    "azure-service-principals-explainer": dict(
        desc="Build an Azure service principal from scratch, decode the JWT it is handed, "
             "then widen its role assignment and watch the blast radius grow along with it.",
        short="Build a service principal, decode its token, then watch the blast radius grow.",
        about="Azure service principals and OAuth machine identity"),

    "discovering-models-trends-explainer": dict(
        desc="A new model lands every week and the announcements all sound alike. Read a "
             "model card the way engineers do, then track which releases actually mattered.",
        short="Read a model card the way engineers do, and track which releases mattered.",
        about="Evaluating and tracking new AI model releases"),

    "evaluating-models-explainer": dict(
        desc="Two chatbots, two answers, no way to choose by gut. Build a small eval set, "
             "score both models against it, and watch a coin flip turn into a measurement.",
        short="Build an eval set, score two models, and turn a coin flip into a measurement.",
        about="Evaluating and comparing large language models"),

    "genai-vocabulary-explainer": dict(
        desc="Token, embedding, context window, RAG, agent — the GenAI vocabulary in the "
             "order the ideas depend on each other. Click any term to watch it work.",
        short="The GenAI vocabulary, in the order the ideas actually depend on each other.",
        about="Generative AI terminology"),

    "grc-building-blocks": dict(
        desc="A reference for the seven pieces every GRC programme is built from: what each "
             "block is, what it is not, and the question it answers when an auditor asks.",
        short="The seven blocks of GRC: what each is, what it is not, what it answers.",
        about="Governance, risk and compliance building blocks"),

    "grc-building-blocks-lesson": dict(
        desc="The same seven GRC blocks, taught rather than listed — worked through one "
             "organisation in order, showing how a single failing block breaks the six others.",
        short="The seven GRC blocks taught in order, and how one failing block breaks the rest.",
        about="Teaching governance, risk and compliance fundamentals"),

    "grc-explained": dict(
        desc="Frameworks, policies, controls, risk, mitigation, compliance — six words that "
             "sound like bureaucracy but describe one system. Trace a single rule end to end.",
        short="Six bureaucratic-sounding words, one connected system. Trace a rule end to end.",
        about="Governance, risk and compliance"),

    "grc-for-genai": dict(
        desc="Run governance for generative AI end to end through one organisation's real "
             "control library, risk register and compliance posture — not a checklist.",
        short="GenAI governance through a real control library, risk register and posture.",
        about="Governance of generative AI systems"),

    "grc-operating-registers": dict(
        desc="The registers an organisation keeps on itself — risk, control, asset, incident, "
             "exception, vendor. What belongs in every row, and who has to sign it.",
        short="Risk, control, asset, incident, exception, vendor: what goes in each row.",
        about="GRC operating registers"),

    "how-data-becomes-an-equation": dict(
        desc="Eight days of a lemonade stand, worked by hand into a line, a cluster and a "
             "policy — supervised, unsupervised and reinforcement learning from one table.",
        short="One lemonade stand table becomes a line, a cluster and a policy.",
        about="Supervised, unsupervised and reinforcement learning"),

    "how-models-learn": dict(
        desc="A model on a hillside in fog can only feel which way the ground tilts. Set the "
             "learning rate yourself and watch gradient descent converge, crawl, or diverge.",
        short="Set the learning rate and watch gradient descent converge, crawl, or diverge.",
        about="Loss, gradient descent and backpropagation"),

    "is-it-actually-thinking": dict(
        desc="Short answer: no — it is autocomplete that read the internet. See the one trick "
             "underneath, and two of the biggest beginner worries about AI fall away at once.",
        short="It is autocomplete that read the internet. See the trick underneath.",
        about="How large language models generate text"),

    "matchbox-language-model": dict(
        desc="In 1960 a stack of matchboxes learned noughts and crosses using coloured beads. "
             "Point the same machine at words and train a language model by hand, bead by bead.",
        short="Train a language model by hand, using matchboxes and coloured beads.",
        about="How language models learn from examples"),

    "multimodal-explainer": dict(
        desc="A phone pointed at a foreign menu needs sight and language at once. Build the "
             "shared space that lets one model mix its senses, and see how multi-model differs.",
        short="Build the shared space that lets one model see, read and hear at once.",
        about="Multimodal artificial intelligence"),

    "never-use-ai-when-rules-will-do": dict(
        desc="When you can make the promise, do not place the bet. Slide the error tolerance "
             "until the model stops being the cheaper answer and a plain rule wins outright.",
        short="Slide the error tolerance until a plain rule beats the model outright.",
        about="Choosing between rule-based systems and machine learning"),

    "partition-equal-subset-sum": dict(
        desc="Can a pile of numbers split into two stacks of equal weight? Tip the scale with "
             "your finger, then watch the same question solved as a subset-sum table.",
        short="Tip the scale with your finger, then watch it solved as a subset-sum table.",
        about="Partition equal subset sum, LeetCode 416"),

    "postgres-partitioning-explainer": dict(
        desc="Drag a project id and watch the planner skip seven of eight partitions, then see "
             "why retention stops being a slow DELETE and becomes an instant DROP.",
        short="Watch the planner skip seven of eight partitions, then DROP instead of DELETE.",
        about="PostgreSQL table partitioning"),

    "prompt-engineering-explainer": dict(
        desc="Climb from a plain question to ReAct agents on one stubborn problem, and watch "
             "exactly which change of wording moves the answer and which changes nothing.",
        short="From zero-shot to ReAct on one stubborn problem. See which wording matters.",
        about="Prompt engineering techniques"),

    "rate-limiting-explainer": dict(
        desc="Rate limiting is refusing work cheaply so you can keep doing work at all. Starve, "
             "feed and flood a live token bucket, and catch the moment it starts returning 429.",
        short="Starve, feed and flood a live token bucket. Catch the moment it returns 429.",
        about="API rate limiting and token bucket algorithms"),

    "reasoning-models-explainer": dict(
        desc="Ask a reasoning model something hard and it pauses. Open up that pause: what it "
             "does in the gap, how it learned to, and when the extra tokens are wasted money.",
        short="Open up the pause: what a reasoning model does, and when it wastes your money.",
        about="Reasoning models and chain-of-thought inference"),

    "regulatory-atlas": dict(
        desc="GDPR to the EU AI Act: ten frameworks, who each binds, what each demands, and the "
             "controls that satisfy them. Filter by obligation to see where they overlap.",
        short="Ten frameworks, what each demands, and the controls that satisfy them.",
        about="AI and data protection regulatory frameworks"),

    "the-layers-of-intelligence": dict(
        desc="AI, machine learning, neural nets and deep learning nest like India, Maharashtra, "
             "Mumbai, Bandra. Then the diagram keeps going, and GenAI stops fitting inside.",
        short="The nesting works like India, Maharashtra, Mumbai — until GenAI stops fitting.",
        about="How AI, machine learning, deep learning and generative AI relate"),

    "three-types-of-machine-learning": dict(
        desc="Three ways to learn to cook, in the same order as the three kinds of machine "
             "learning. What separates them is one question: when do you find out you were wrong?",
        short="What separates the three types is one question: when do you find out you erred?",
        about="Supervised, unsupervised and reinforcement learning"),

    "tokenization": dict(
        desc="A tokenizer is a frozen record of what was frequent in one pile of text. Type a "
             "sentence, watch it get cut and priced, then break it with an unusual word.",
        short="Type a sentence, watch it get cut and priced, then break it with a rare word.",
        about="Tokenization in large language models"),

    "what-ai-is-good-and-bad-at": dict(
        desc="There is one clean line between what AI does well and badly, and it is not the "
             "one most people guess. Learn to call the green and red lights before you hit send.",
        short="One clean line separates what AI does well from what it does badly.",
        about="Capabilities and limitations of artificial intelligence"),

    "what-is-intelligence": dict(
        desc="Every definition of intelligence lets in something that is not, and shuts out "
             "something that is. Break four of them yourself, then answer the harder questions.",
        short="Break four definitions of intelligence yourself, then face the harder questions.",
        about="Definitions of intelligence and machine intelligence"),
}

# Unlisted pages ---------------------------------------------------------------
#
# Live at /notes/<slug>. Reachable by anyone with the URL and crawlable by Google
# (they are in sitemap.xml and carry ordinary metadata), but deliberately absent
# from three places: the card grid on /explorables, the site's own search box, and
# the Atom feed.
#
# They sit in their own directory rather than in explorables/ on purpose. Every
# mechanism that surfaces a page - the sitemap builder, the search reindexer, the
# metadata pass - finds its work with glob("explorables/*.html"). Keeping notes
# outside that glob means a tool written next year cannot leak one by forgetting an
# exclusion list. Being unlisted is a property of where the file lives, not of
# every script remembering a rule.
#
# Same shape as EXPLORABLES: desc, optional short, about.
NOTES_DIR = "notes"
NOTES = {
    "ai-vs-ml-explained-questions": dict(
        desc="Forty questions on where automation ends and learning begins, following the "
             "observe–analyse–infer–recalibrate loop. Answers stay hidden until you commit.",
        short="Forty questions on where automation ends and learning begins.",
        about="Difference between automation, machine learning and artificial intelligence"),

    "case-studies-ai-transformation-questions": dict(
        desc="Thirty-seven questions on nine real deployments — a public reversal, a legal "
             "precedent, a $62m failure — and how to read any case study without being fooled.",
        short="Nine real deployments, including a $62m failure, read honestly.",
        about="Case studies of enterprise AI transformation"),

    "coe-and-scaling-strategies-questions": dict(
        desc="Thirty-eight questions on turning pilots into production — the three failure "
             "modes, the 10-20-70 split, and the move from pilot to platform to portfolio.",
        short="What turns pilots into production: three failure modes and 10-20-70.",
        about="AI centres of excellence and scaling strategy"),

    "from-use-case-to-production-questions": dict(
        desc="Fifty questions on governance intake, the six risk domains, lifecycle gates and "
             "assurance — plus the forces that quietly bend every GenAI business case.",
        short="Governance intake, six risk domains, gates, and what bends a GenAI number.",
        about="Taking generative AI from use case to production"),

    "how-models-learn-questions": dict(
        desc="Thirty questions on loss, gradient descent, the learning rate, backpropagation "
             "and overfitting. No maths beyond subtraction; every number checks out on paper.",
        short="Loss, gradient descent, learning rate and overfitting — checkable on paper.",
        about="How machine learning models are trained"),

    "identifying-high-value-opportunities-questions": dict(
        desc="Thirty-five questions on finding the GenAI work worth doing — visibility bias, "
             "picking the right altitude, the six shapes, and scoring an idea honestly.",
        short="Visibility bias, the right altitude, and scoring an idea honestly.",
        about="Identifying high-value generative AI opportunities"),

    "never-use-ai-when-rules-will-do-questions": dict(
        desc="Thirty-seven questions on when a plain rule beats a model — the checklist, three "
             "worked examples, and the layered designs real systems actually ship with.",
        short="When a plain rule beats a model: the checklist and three worked examples.",
        about="Choosing between rule-based systems and machine learning"),

    "the-layers-of-intelligence-questions": dict(
        desc="Thirty-two questions on how AI, machine learning, deep learning, GenAI, LLM and "
             "GPT nest — and the exact point where the usual diagram stops being true.",
        short="How the words nest, and where the usual diagram goes wrong.",
        about="How AI, machine learning, deep learning and generative AI relate"),

    "the-method-in-one-week-questions": dict(
        desc="Fifty-eight questions in the order a real project runs — from whether to use AI "
             "at all, through build and launch, to the ninety-day review afterwards.",
        short="Whether to use AI at all, through launch, to the ninety-day review.",
        about="Running a generative AI project end to end"),

    "three-types-of-machine-learning-questions": dict(
        desc="Thirty-five questions on supervised, unsupervised and reinforcement learning — "
             "and the one that matters most: which situation are you actually in?",
        short="Supervised, unsupervised, reinforcement — and which one you are in.",
        about="Supervised, unsupervised and reinforcement learning"),

    "workforce-reskilling-and-leadership-questions": dict(
        desc="Thirty-eight questions on the people half — the novice paradox, the jagged "
             "frontier, the three layers of reskilling, shadow AI, and what changes for a manager.",
        short="The novice paradox, the jagged frontier, shadow AI, and the manager's job.",
        about="Workforce reskilling and leadership for AI adoption"),
}

# Renames applied by rename_slug(); old path keeps a 301 for anything already linking it.
RENAMES = {"tokenization-03A": "tokenization"}

PERSON = {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": AUTHOR,
    "url": SITE + "/",
    "jobTitle": "Head of AI",
    "worksFor": {"@type": "Organization", "name": "MarketOnce"},
    "alumniOf": {"@type": "Organization", "name": "Microsoft"},
    "knowsAbout": ["Generative AI", "Machine Learning", "Cloud Architecture",
                   "Azure", "PostgreSQL", "Distributed Systems"],
    "sameAs": [
        "https://github.com/ritesh-modi",
        "https://www.linkedin.com/in/ritesh-modi",
    ],
}
