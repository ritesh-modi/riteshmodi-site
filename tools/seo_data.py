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
        desc="Loopingly is where Ritesh Modi publishes interactive explainers on how AI actually "
             "works: single pages you learn by dragging, poking and breaking.",
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
    "agentic-rag": {
        "desc": "Ordinary retrieval searches once. Watch a question loop through numbered stations, get judged too thin, and go round again — then set the cap that stops it.",
        "short": "Watch a question loop through retrieval, get judged thin, and go round again.",
        "about": "Agentic RAG and retrieval-augmented generation",
    },
    "03-words-to-vectors": dict(
        desc="Spin a compass between two words and watch the angle turn into a similarity score, "
             "then point it at ten real vectors and read off the neighbours.",
        short="Spin a compass between two words and watch the angle become a similarity score.",
        about="Word embeddings and cosine similarity"),

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

    "classification-metrics-by-hand": dict(
        desc="Drag one threshold across fifteen emails and watch the confusion matrix, precision "
             "and recall swing while accuracy sits at 0.87 and tells you nothing.",
        short="Drag one threshold and watch precision and recall swing while accuracy sits still.",
        about="Classification metrics: accuracy, precision, recall, F1 and ROC"),

    "delta-table-api-explained": dict(
        desc="A table here is a folder of files plus a log saying which ones count. Overwrite, "
             "merge, time travel and vacuum, watching the folder change at every call.",
        short="Overwrite, merge and time travel, with the folder open beside you.",
        about="The Delta Lake table API"),

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

    "generative-ai": dict(
        desc="Old classifiers picked an answer off a list. Watch a sentence become numbers, then a "
             "spread of odds, and make the sampling choice for yourself.",
        short="Watch a sentence become numbers, then a spread of odds you sample from yourself.",
        about="How generative AI models produce text"),

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
        desc="The risk register and the five kept beside it — policies, controls, mitigations, "
             "findings, mappings. What belongs in every row, and who has to sign it.",
        short="Policies, controls, risks, mitigations, findings, mappings: what goes in each row.",
        about="GRC operating registers"),

    "history-of-generative-ai": dict(
        desc="Play Shannon's 1948 letter-guessing game, drag n across a bigram table until counting "
             "collapses, then watch backpropagation pick up where it failed.",
        short="Play Shannon's letter-guessing game, then watch pure counting collapse.",
        about="The history of generative AI from 1948 to the present"),

    "how-data-becomes-an-equation": dict(
        desc="Eight days of a lemonade stand, worked by hand into a line, a cluster and a "
             "policy — supervised, unsupervised and reinforcement learning from one table.",
        short="One lemonade stand table becomes a line, a cluster and a policy.",
        about="Supervised, unsupervised and reinforcement learning"),

    "how-models-learn": dict(
        desc="Training a model is walking downhill in fog, feeling which way the ground tilts. "
             "Set the learning rate yourself and watch gradient descent converge or diverge.",
        short="Set the learning rate and watch gradient descent converge, crawl, or diverge.",
        about="Model training: loss, gradient descent and backpropagation"),

    "how-twenty-companies-run-generative-ai": dict(
        desc="Twenty production deployments across six layers. Resize the retrieval chunks until "
             "they ruin an answer, turn the queue dial, and find each system's scar.",
        short="Resize retrieval chunks until they ruin the answer, then find each system's scar.",
        about="Generative AI systems in production"),

    "is-it-actually-thinking": dict(
        desc="Short answer: no — an LLM is autocomplete that read the internet. See the one "
             "trick underneath, and two of the biggest beginner worries fall away at once.",
        short="It is autocomplete that read the internet. See the trick underneath.",
        about="How large language models (LLMs) generate text"),

    "matchbox-language-model": dict(
        desc="In 1960 a stack of matchboxes learned noughts and crosses using coloured beads. Point "
             "it at words and train a language model by hand, bead by bead.",
        short="Train a language model by hand, using matchboxes and coloured beads.",
        about="How language models (LLMs) learn from examples"),

    "medallion-ten-rows-a-day": dict(
        desc="Ten rows a night through bronze, silver and gold. Append the raw file, merge one "
             "row per order, rebuild the report, then drop a late row in and watch it move.",
        short="Append to bronze, merge into silver, rebuild gold, then break it with a late row.",
        about="Medallion architecture with Delta Lake"),

    "multimodal-explainer": dict(
        desc="A phone pointed at a foreign menu needs sight and language at once. Build the "
             "shared space that lets one model mix its senses, and see how multi-model differs.",
        short="Build the shared space that lets one model see, read and hear at once.",
        about="Multimodal artificial intelligence"),

    "neural-network-by-hand": dict(
        desc="A neural network with fifteen weights, all on the page. Walk a row forward through two "
             "hidden layers, then watch backpropagation carry the error back.",
        short="Walk one row forward through two hidden layers, then watch the error walk back.",
        about="Neural network forward and backward passes"),

    "never-use-ai-when-rules-will-do": dict(
        desc="When you can make the promise, do not place the bet. Slide the error tolerance "
             "until the model stops being the cheaper answer and a plain rule wins outright.",
        short="Slide the error tolerance until a plain rule beats the model outright.",
        about="Choosing between rule-based systems and machine learning"),

    "partition-equal-subset-sum": dict(
        desc="Can a pile of numbers split into two stacks of equal weight? Tip the scale with your "
             "finger, then solve it again as a dynamic programming table, cell by cell.",
        short="Tip the scale with your finger, then watch it solved as a subset-sum table.",
        about="Partition equal subset sum, LeetCode 416"),

    "playground-controls": dict(
        desc="Every control on the OpenAI Playground, one at a time. Move reasoning effort, "
             "verbosity and text format, and watch what each one changes in the request.",
        short="Move each Playground control and watch what it changes in the request.",
        about="The OpenAI Playground controls and model parameters"),

    "postgres-partitioning-explainer": dict(
        desc="Drag a project id and watch the planner skip seven of eight partitions, then see "
             "why retention stops being a slow DELETE and becomes an instant DROP.",
        short="Watch the planner skip seven of eight partitions, then DROP instead of DELETE.",
        about="PostgreSQL table partitioning"),

    "predicting-the-next-character": dict(
        desc="Fill a 625-box count grid by hand, smooth it so unseen pairs stop breaking it, then "
             "train an eight-number embedding and watch the loss come down.",
        short="Fill a 625-box count grid by hand, then train a small network on the same job.",
        about="Character-level language models and neural networks"),

    "prompt-engineering-explainer": dict(
        desc="Climb from a plain question to ReAct agents on one stubborn problem, and watch "
             "exactly which change of wording moves the answer and which changes nothing.",
        short="From zero-shot to ReAct on one stubborn problem. See which wording matters.",
        about="Prompt engineering techniques"),

    "prompting-techniques": dict(
        desc="Eleven prompting techniques against one task. Fence off pasted text so it cannot give "
             "orders, force a shape, sample five times and count the answers.",
        short="Run eleven prompting techniques against one task and see which change the answer.",
        about="Prompt engineering techniques for large language models"),

    "rate-limiting-explainer": dict(
        desc="Rate limiting is refusing work cheaply so you can keep doing work at all. Starve, feed "
             "and flood a live token bucket, and catch it returning 429.",
        short="Starve, feed and flood a live token bucket. Catch the moment it returns 429.",
        about="API rate limiting and token bucket algorithms"),

    "reasoning-models-explainer": dict(
        desc="Ask a reasoning model something hard and it pauses. Open up that pause: what it "
             "does in the gap, how it learned to, and when the extra tokens are wasted money.",
        short="Open up the pause: what a reasoning model does, and when it wastes your money.",
        about="Reasoning models and chain-of-thought inference"),

    "regression-metrics-by-hand": dict(
        desc="Add ten gaps one at a time, then drop a cracked-screen laptop into the test set and "
             "watch MAE, MSE, RMSE and R squared disagree about the very same model.",
        short="Drop one cracked-screen laptop into the test set and watch four scores disagree.",
        about="Regression metrics: MAE, MSE, RMSE and R squared"),

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

    "three-motions-of-a-model": dict(
        desc="Twenty-two logged commutes, three models, one loop. Nudge a rule downhill, hold "
             "rows back, drag a threshold, then bend a straight line with two hidden layers.",
        short="Nudge a rule downhill, hold rows back, then bend it with two hidden layers.",
        about="Classification, regression and deep learning"),

    "three-types-of-machine-learning": dict(
        desc="Three ways to learn to cook, in the order of supervised, unsupervised and "
             "reinforcement learning. What separates them: when do you find out you were wrong?",
        short="What separates the three types is one question: when do you find out you erred?",
        about="Supervised, unsupervised and reinforcement learning"),

    "tokenization": dict(
        desc="An LLM reads tokens, not words, and a tokenizer is a frozen record of one pile "
             "of text. Type a sentence, watch it get cut and priced, then break it.",
        short="Type a sentence, watch it get cut and priced, then break it with a rare word.",
        about="Tokenization in large language models (LLMs)"),

    "what-ai-is-good-and-bad-at": dict(
        desc="There is one clean line between what AI does well and what it does badly, and it is "
             "not the one most people guess. Learn to call it before you send.",
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
    # jobTitle takes a list, and the extra two are what a reader is actually weighing
    # when they decide whether to trust an explainer. They match the hero pills on the
    # home page exactly: a structured claim that contradicts the visible page is worse
    # than no claim at all.
    "jobTitle": ["Head of AI", "AI/ML Researcher", "Forward Deployed Engineer"],
    "description": "AI/ML researcher and Head of AI at MarketOnce. Ex-Microsoft "
                   "forward deployed engineer, and the author of Loopingly, a "
                   "collection of interactive explainers on how AI actually works.",
    "worksFor": {"@type": "Organization", "name": "MarketOnce"},
    "alumniOf": {"@type": "Organization", "name": "Microsoft"},
    "knowsAbout": ["Generative AI", "Large Language Models", "Machine Learning",
                   "Deep Learning", "Prompt Engineering", "Retrieval-Augmented Generation",
                   "AI Agents", "AI Governance", "Data Engineering", "Medallion Architecture",
                   "Delta Lake", "Cloud Architecture", "Azure", "PostgreSQL",
                   "Distributed Systems"],
    # sameAs is how Google is told these accounts are one entity. Every profile
    # listed here should also link back to loopingly.com — a one-way claim is much
    # weaker than a reciprocated one, and the whole point is the brand association.
    "sameAs": [
        "https://github.com/ritesh-modi",
        "https://www.linkedin.com/in/ritesh-modi",
        "https://medium.com/@ritesh.modi",
        "https://x.com/automationnext",
        "https://riteshmodi.com/",
    ],
}


# Per-page keywords for the Article JSON-LD.
#
# This is schema.org "keywords", which Google does read as a topic signal. It is NOT
# <meta name="keywords">, which Google has ignored since 2009 and which is not emitted
# anywhere on this site — do not add it.
#
# Every entry must be true of the page it sits on. The value of this field comes
# entirely from its accuracy: a keyword the page does not actually teach is stuffing,
# it earns nothing, and it puts the honest entries in doubt. Where a page teaches a
# concept the world searches for under a different name, both names belong here
# ("language model" and "LLM"); where a word means something unrelated, it does not
# (rate limiting's "token bucket" has nothing to do with an LLM token).
KEYWORDS = {
    "agentic-rag": ["what is agentic RAG", "agentic RAG explained", "agentic RAG vs RAG", "how does RAG work",
                    "when does RAG search again", "RAG retry loop", "AI agent retrieval loop"],
    "03-words-to-vectors": ["what are word embeddings", "how does cosine similarity work",
                            "how do vector databases find similar text", "embeddings explained simply"],
    "ai-transformation-explainer": ["AI transformation strategy", "how to lead AI transformation",
                                    "AI efficiency vs reinvention", "AI business case", "where to invest in AI"],
    "ai-vs-ml-explained": ["AI vs machine learning", "difference between AI and machine learning",
                           "machine learning vs automation", "is automation the same as AI", "AI vs ML vs automation"],
    "azure-service-principals-explainer": ["what is an Azure service principal", "service principal vs managed identity",
                                           "how to decode a JWT", "Azure role assignment blast radius", "Entra ID app registration"],
    "classification-metrics-by-hand": ["confusion matrix explained", "precision vs recall", "why accuracy is misleading",
                                       "what is F1 score", "how to read an ROC curve"],
    "delta-table-api-explained": ["what is Delta Lake", "Delta Lake time travel", "how does MERGE work in Delta",
                                  "what does VACUUM do", "Delta transaction log explained"],
    "discovering-models-trends-explainer": ["how to choose an AI model", "how to read a model card", "which AI model should I use",
                                            "tracking new AI model releases"],
    "evaluating-models-explainer": ["how to evaluate an LLM", "what are LLM benchmarks", "how to compare AI models",
                                    "LLM evals explained"],
    "genai-vocabulary-explainer": ["generative AI terms explained", "what is a token embedding context window",
                                   "GenAI glossary", "AI jargon explained", "what is RAG and fine-tuning"],
    "generative-ai": ["how does generative AI work", "how do LLMs generate text", "what is temperature in AI",
                      "sampling explained", "GenAI explained simply"],
    "grc-building-blocks": ["what is GRC", "GRC framework components", "governance risk and compliance explained",
                            "policies controls and risks difference"],
    "grc-building-blocks-lesson": ["GRC training", "how to teach GRC", "GRC fundamentals lesson",
                                   "governance risk compliance for beginners"],
    "grc-explained": ["what is governance risk and compliance", "GRC explained simply",
                      "difference between policy and control", "what is a compliance control"],
    "grc-for-genai": ["AI governance framework", "how to govern generative AI", "GenAI risk management",
                      "LLM compliance", "responsible AI in practice"],
    "grc-operating-registers": ["what is a risk register", "what goes in a risk register",
                                "control register vs risk register", "GRC registers explained"],
    "history-of-generative-ai": ["history of generative AI", "who invented generative AI",
                                 "Shannon information theory language", "how LLMs evolved"],
    "how-data-becomes-an-equation": ["supervised vs unsupervised learning", "what is reinforcement learning",
                                     "how does machine learning work", "types of machine learning explained"],
    "how-models-learn": ["how are AI models trained", "gradient descent explained", "what is backpropagation",
                         "what is a learning rate", "how does model training work"],
    "how-twenty-companies-run-generative-ai": ["generative AI in production", "real world LLM examples", "how companies use generative AI",
                                               "LLM production architecture", "retrieval chunk size"],
    "is-it-actually-thinking": ["how does an LLM work", "do LLMs actually think", "is AI really thinking",
                                "how do chatbots generate text", "next token prediction explained"],
    "matchbox-language-model": ["how do language models learn", "build a language model by hand",
                                "language model explained simply", "MENACE matchboxes"],
    "medallion-ten-rows-a-day": ["what is medallion architecture", "bronze silver gold layers explained",
                                 "medallion architecture example", "Delta Lake medallion", "lakehouse layers"],
    "multimodal-explainer": ["what is multimodal AI", "multimodal vs multi-model", "how do vision language models work",
                             "AI that sees and reads"],
    "neural-network-by-hand": ["how does a neural network work", "backpropagation explained", "neural network by hand",
                               "what is a hidden layer", "forward pass and backward pass"],
    "never-use-ai-when-rules-will-do": ["when not to use machine learning", "rules vs machine learning", "do I need AI for this",
                                        "when is a rule better than a model"],
    "partition-equal-subset-sum": ["partition equal subset sum", "LeetCode 416 solution", "subset sum dynamic programming",
                                   "how does the dp table work"],
    "playground-controls": ["what does temperature do in AI", "what is top-p sampling",
                            "OpenAI playground settings explained", "LLM parameters explained"],
    "postgres-partitioning-explainer": ["Postgres table partitioning", "how does partition pruning work",
                                        "Postgres partition by range", "DROP partition vs DELETE",
                                        "Postgres performance partitioning"],
    "predicting-the-next-character": ["how next token prediction works", "character level language model",
                                      "build a neural network by hand", "embeddings explained"],
    "prompt-engineering-explainer": ["what is prompt engineering", "how to prompt an LLM", "prompt engineering for beginners",
                                     "better AI prompts"],
    "prompting-techniques": ["prompt engineering techniques", "few-shot prompting explained",
                             "chain of thought prompting", "how to write better AI prompts"],
    "rate-limiting-explainer": ["how does rate limiting work", "token bucket algorithm explained", "what is a 429 error",
                                "API throttling explained", "leaky bucket vs token bucket"],
    "reasoning-models-explainer": ["how do reasoning models work", "what is chain of thought",
                                   "why do reasoning models think longer", "test time compute explained"],
    "regression-metrics-by-hand": ["MAE vs RMSE", "what is R squared", "which regression metric to use",
                                   "why RMSE punishes outliers", "regression metrics explained"],
    "regulatory-atlas": ["EU AI Act explained", "GDPR and AI", "AI compliance frameworks",
                         "which regulations apply to AI", "mapping obligations to controls"],
    "the-layers-of-intelligence": ["AI vs machine learning vs deep learning", "how do AI and ML relate",
                                   "is deep learning part of AI", "where does generative AI fit"],
    "three-motions-of-a-model": ["classification vs regression", "what is deep learning", "types of models explained",
                                 "when to use regression vs classification"],
    "three-types-of-machine-learning": ["types of machine learning", "supervised vs unsupervised vs reinforcement",
                                        "what is supervised learning", "machine learning types explained"],
    "tokenization": ["how tokenization works", "what are tokens in an LLM", "why do LLMs use tokens",
                     "byte pair encoding explained", "tokenizer explained", "why LLMs miscount letters"],
    "what-ai-is-good-and-bad-at": ["what is AI good at", "AI limitations", "what can AI not do", "when does AI fail",
                                   "should I use AI for this task"],
    "what-is-intelligence": ["what is intelligence", "is AI actually intelligent", "definition of intelligence",
                             "can machines be intelligent", "is AI conscious"],
}
