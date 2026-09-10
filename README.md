# 🦠 ESKAPE-AMR Drug Resistance Explorer

An interactive **Streamlit-based research tool** for exploring antimicrobial drug-resistance mechanisms across the six ESKAPE pathogen groups.

The application takes an **antimicrobial drug as input** and presents the different resistance mechanisms reported across ESKAPE pathogens, including associated resistance genes/proteins, biological explanations, evidence levels, and supporting literature.

---

## 🧬 ESKAPE Pathogens

The project focuses on:

| Letter | Pathogen                  |
| ------ | ------------------------- |
| E      | *Enterococcus faecium*    |
| S      | *Staphylococcus aureus*   |
| K      | *Klebsiella pneumoniae*   |
| A      | *Acinetobacter baumannii* |
| P      | *Pseudomonas aeruginosa*  |
| E      | *Enterobacter* spp.       |

---

## 💊 What Does It Do?

The user selects or enters an antimicrobial drug, for example:

```text
Meropenem
```

The application then organizes resistance information by pathogen:

```text
Meropenem
│
├── Klebsiella pneumoniae
│   ├── Carbapenemase production
│   │   ├── blaKPC
│   │   ├── blaNDM
│   │   └── blaOXA-48
│   │
│   └── Reduced permeability
│       ├── ompK35
│       └── ompK36
│
├── Pseudomonas aeruginosa
│   ├── Reduced permeability
│   │   └── oprD
│   │
│   └── Efflux
│       └── mexAB-oprM
│
└── Acinetobacter baumannii
    └── Carbapenemase production
        └── blaOXA-23
```

---

## 🔬 Resistance Mechanisms

The knowledge base can contain mechanisms such as:

* Drug inactivation
* Target modification
* Target protection
* Reduced permeability
* Increased efflux
* Cell-wall modification
* Lipid A modification
* Biofilm-associated resistance
* Enzymatic degradation
* Regulatory changes
* Acquired resistance genes
* Mutation-associated resistance

---

## 📊 Information Provided

For each drug-pathogen combination, the application can display:

* Pathogen
* Antimicrobial drug
* Resistance mechanism
* Associated gene/protein
* Biological mechanism
* Evidence level
* Supporting research papers
* DOI information
* Cross-pathogen comparison

---

## 🖥️ Application Interface

The application is built using **Streamlit** and provides:

1. Antimicrobial drug selection
2. Custom drug search
3. Mechanism-by-pathogen analysis
4. Resistance gene information
5. Evidence classification
6. Supporting literature
7. Cross-pathogen comparison
8. Knowledge-base statistics

---

## 📁 Project Structure

```text
ESKAPE-AMR-Drug-Resistance-Explorer/
│
├── app_2.py
├── mechanism.csv
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

### `app_2.py`

Main Streamlit application.

### `mechanism.csv`

Knowledge base containing drug-pathogen-resistance mechanism relationships.

### `requirements.txt`

Python dependencies required to run the application.

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ESKAPE-AMR-Drug-Resistance-Explorer.git
```

Enter the project directory:

```bash
cd ESKAPE-AMR-Drug-Resistance-Explorer
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app_2.py
```

The application will open in your browser.

---

## 📋 Knowledge Base Format

The knowledge base is stored as a CSV file.

The main fields are:

```text
pathogen
drug
mechanism
gene
description
evidence
paper_title
year
doi
```

Example:

```csv
pathogen,drug,mechanism,gene,description,evidence
Klebsiella pneumoniae,Meropenem,Carbapenemase production,blaKPC,Carbapenem hydrolysis,High
Pseudomonas aeruginosa,Meropenem,Reduced permeability,oprD,Reduced drug uptake,High
Acinetobacter baumannii,Colistin,Lipid A modification,pmrAB,Altered LPS structure,High
```

---

## 🔎 Example Queries

Examples of drugs that can be explored:

```text
Meropenem
Ciprofloxacin
Colistin
Methicillin
Vancomycin
Ceftriaxone
```

The application is designed around the question:

> **"What resistance mechanisms are associated with this drug across ESKAPE pathogens?"**

---

## 🧠 Scientific Interpretation

The application is a **literature-assisted knowledge exploration tool**.

A resistance mechanism reported in the database should not automatically be interpreted as experimentally confirmed for every strain of a pathogen.

Evidence should therefore be evaluated in the context of the original research literature.

---

## 🚀 Future Development

Potential extensions include:

* PubMed and Europe PMC integration
* Automated research-paper retrieval
* Retrieval-Augmented Generation (RAG)
* Large Language Model-based literature analysis
* Semantic search
* Resistance-gene extraction
* Mutation-level resistance analysis
* CARD integration
* NCBI AMRFinderPlus integration
* ResFinder integration
* AMR knowledge graph construction
* Automated citation generation
* Drug-mechanism prediction
* Comparative analysis between ESKAPE pathogens

---

## 🎯 Project Goal

The long-term goal is to develop an **evidence-aware computational research assistant** capable of connecting:

```text
Antimicrobial drug
        ↓
ESKAPE pathogen
        ↓
Resistance mechanism
        ↓
Resistance gene / mutation
        ↓
Biological effect
        ↓
Resistance phenotype
        ↓
Scientific literature
```

---

## ⚠️ Disclaimer

This project is intended for **research and educational purposes**.

The information presented by the application should be verified against the original scientific literature before being used for clinical, diagnostic, therapeutic, or public-health decisions.

---

## 👩‍💻 Author

**Nikita Accamma Mathew**

Bioinformatics / Computational Biology

---

## 📄 License

This project is released under the MIT License.
