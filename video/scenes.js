// MVA Hackathon 2026 — Track 2 pitch video (~3 min)
// Visual direction: editorial (warm paper + signal red, serif display) —
// research-report register for a rare-disease mechanism pitch.
module.exports = [
  { name: "cover",
    card: { preset: "editorial",
            title: "Readthrough for MVA",
            kicker: "Rare Disease, Real Kid · MVA Hackathon 2026 · Track 2",
            sub: "A drug repurposing proposal for a BUB1B compound-heterozygous proband",
            foot: "Georgefifth" },
    duration: 4,
    vo: "A drug repurposing proposal for mosaic variegated aneuploidy — a real child, a real variant, a mechanism we can act on." },

  { name: "patient",
    card: { image: "/home/yap/Hack/Disease/video/assets/s2.png" },
    duration: 3,
    vo: "Mosaic variegated aneuploidy is an ultra-rare chromosome instability disorder — fewer than fifty cases ever reported. Our proband was born premature, growth-restricted, and is already fighting rhabdomyosarcoma. Nothing touches the cause. Our job: repurpose an existing drug against the mechanism." },

  { name: "finding",
    card: { image: "/home/yap/Hack/Disease/video/assets/s3.png" },
    duration: 3,
    vo: "From the whole genome, we identified a compound-heterozygous pair in BUB1B — the gene behind MVA type one. Allele one is a nonsense change: leucine-737 becomes a premature stop, already classified pathogenic in ClinVar. Allele two is a novel missense inside the pseudokinase domain. Two different hits, one broken gene." },

  { name: "mechanism",
    card: { image: "/home/yap/Hack/Disease/video/assets/s4.png" },
    duration: 3,
    vo: "Here is the mechanism that makes repurposing possible. The premature stop triggers nonsense-mediated decay — the messenger RNA is destroyed before it can make protein. But this class of truncation is stable when expressed: the protein isn't broken, the message is being shredded. That gives us two ways in — read through the stop, or save the transcript." },

  { name: "clinvar",
    url: "https://www.ncbi.nlm.nih.gov/clinvar/variation/533901/",
    actions: [
      { type: "waitFor", sel: ".germline-info", timeout: 15000 },
      { type: "scrollIntoView", sel: ".germline-info" },
      { type: "wait", ms: 1200 },
      { type: "hover", sel: ".germline-info .single-item-value" },
      { type: "wait", ms: 2500 },
    ],
    vo: "This is the public evidence. ClinVar variation 533901 — our allele one — already carries a pathogenic classification for MVA syndrome." },

  { name: "analyzer",
    url: "file:///home/yap/Hack/Disease/video/assets/analysis.html",
    actions: [
      { type: "waitFor", sel: "#score" },
      { type: "wait", ms: 800 },
      { type: "hover", sel: "#c-codon" },
      { type: "wait", ms: 2200 },
      { type: "hover", sel: "#score" },
      { type: "wait", ms: 2600 },
    ],
    vo: "We built a tool that scores any nonsense variant for readthrough amenability — NMD eligibility, codon class, context, salvageable truncation. Ours scores seven of seven: a UGA stop — the most responsive codon — on a transcript NMD will degrade." },

  { name: "drugs",
    card: { image: "/home/yap/Hack/Disease/video/assets/s5.png" },
    duration: 3,
    vo: "Two approved drugs map onto those two levers. Ataluren — EMA-approved for nonsense-mutation Duchenne — suppresses termination so the ribosome reads through the stop and restores full-length BUBR1, with an established pediatric record. Amlexanox inhibits NMD itself — rescuing the stable truncated protein. Different bottlenecks: they may work better together." },

  { name: "threshold",
    card: { image: "/home/yap/Hack/Disease/video/assets/s6.png" },
    duration: 3,
    vo: "This disease is dose-sensitive — carriers with half the normal BUBR1 stay healthy, so partial rescue may cross the threshold. And honestly: this slows new aneuploidy — it does not treat the existing tumor. Next step: treat patient fibroblasts, measure BUBR1, measure the checkpoint." },

  { name: "closing",
    card: { preset: "editorial",
            title: "Mechanism-driven answer",
            kicker: "ataluren · amlexanox · one hypothesis",
            sub: "Report, code, and reasoning — reproducible, public-data only",
            foot: "github.com/Georgefifth/mva-hackathon-2026-track1" },
    duration: 4,
    vo: "A rare disease deserves a mechanism-driven answer. The report, the analysis, and the code are on GitHub." },
];
