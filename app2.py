
import os
import pandas as pd
import streamlit as st

# ESKAPE Drug Resistance Explorer


st.set_page_config(
    page_title="ESKAPE Drug Resistance Explorer",
    page_icon="🦠",
    layout="wide"
)


# Find mechanism.csv

POSSIBLE_FILES = [
    "mechanism.csv",
    "mechanisms.csv",
    os.path.join("data", "mechanism.csv"),
    os.path.join("data", "mechanisms.csv"),
]

DATA_FILE = None

for file in POSSIBLE_FILES:
    if os.path.exists(file):
        DATA_FILE = file
        break



# Load data


@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Clean string columns
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str).str.strip()

    return df



# Header


st.title("🦠 ESKAPE Drug Resistance Explorer")

st.markdown(
    """
### Explore antimicrobial resistance mechanisms across ESKAPE pathogens

Enter an antimicrobial drug to see the **different resistance
mechanisms, associated genes/proteins, evidence and explanations**
reported across the ESKAPE pathogens.
"""
)

st.divider()



# Check database


if DATA_FILE is None:

    st.error("❌ Knowledge base `mechanism.csv` was not found.")

    st.info(
        """
        Put `mechanism.csv` in the same folder as `app_2.py`.

        Expected structure:

        ```
        Documents/
        ├── app_2.py
        └── mechanism.csv
        ```
        """
    )

    st.stop()


df = load_data(DATA_FILE)



# Required columns


required_columns = [
    "pathogen",
    "drug",
    "mechanism",
    "gene",
    "description",
    "evidence"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        "Your CSV is missing these required columns: "
        + ", ".join(missing_columns)
    )

    st.write("Columns detected in your CSV:")
    st.write(list(df.columns))

    st.stop()



# Normalize drug names


df["drug"] = (
    df["drug"]
    .astype(str)
    .str.strip()
)

df["pathogen"] = (
    df["pathogen"]
    .astype(str)
    .str.strip()
)

df["mechanism"] = (
    df["mechanism"]
    .astype(str)
    .str.strip()
)

# Drug selection


st.subheader("💊 Select an antimicrobial drug")

drugs = sorted(
    [
        drug
        for drug in df["drug"].unique()
        if drug
    ]
)

col1, col2 = st.columns([4, 1])

with col1:

    selected_drug = st.selectbox(
        "Drug",
        drugs,
        index=0,
        label_visibility="collapsed"
    )

with col2:

    analyze = st.button(
        "🔍 Analyze",
        type="primary",
        use_container_width=True
    )



# Custom drug search


st.markdown("**Or type a drug name:**")

custom_drug = st.text_input(
    "Drug name",
    placeholder="Example: meropenem",
    label_visibility="collapsed"
)

if custom_drug.strip():
    selected_drug = custom_drug.strip()



# Analyze


if analyze or custom_drug.strip():

    search_drug = selected_drug.lower().strip()

    results = df[
        df["drug"]
        .str.lower()
        .str.strip()
        == search_drug
    ].copy()

    st.divider()

    st.header(
        f"🔬 Resistance mechanisms for {selected_drug}"
    )


    
    # No result
    

    if results.empty:

        # Try partial matching
        partial_results = df[
            df["drug"]
            .str.lower()
            .str.contains(
                search_drug,
                na=False
            )
        ]

        if not partial_results.empty:

            st.warning(
                f"No exact match found for **{selected_drug}**."
            )

            st.write(
                "Did you mean:"
            )

            for drug in sorted(
                partial_results["drug"].unique()
            ):

                st.markdown(
                    f"- **{drug}**"
                )

        else:

            st.warning(
                f"No resistance information for "
                f"**{selected_drug}** is currently present "
                f"in the knowledge base."
            )

        st.stop()


    
    # Summary metrics
    

    pathogens_count = results["pathogen"].nunique()

    mechanisms_count = results["mechanism"].nunique()

    genes_count = results["gene"].nunique()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "ESKAPE pathogens",
            pathogens_count
        )

    with col2:
        st.metric(
            "Resistance mechanisms",
            mechanisms_count
        )

    with col3:
        st.metric(
            "Genes / proteins",
            genes_count
        )


    st.divider()


    
    # Mechanisms by pathogen


    st.subheader(
        "🧬 Mechanisms by ESKAPE pathogen"
    )

    # Preferred ESKAPE order
    eskape_order = [
        "Enterococcus faecium",
        "Staphylococcus aureus",
        "Klebsiella pneumoniae",
        "Acinetobacter baumannii",
        "Pseudomonas aeruginosa",
        "Enterobacter"
    ]


    # Match known pathogens first
    existing_pathogens = results["pathogen"].unique().tolist()

    ordered_pathogens = []

    for pathogen in eskape_order:

        matches = [
            p
            for p in existing_pathogens
            if pathogen.lower() in p.lower()
        ]

        for match in matches:
            if match not in ordered_pathogens:
                ordered_pathogens.append(match)


    # Add anything else
    for pathogen in sorted(existing_pathogens):

        if pathogen not in ordered_pathogens:
            ordered_pathogens.append(pathogen)


    
    # Display pathogen sections


    for pathogen in ordered_pathogens:

        pathogen_data = results[
            results["pathogen"] == pathogen
        ]

        with st.container(border=True):

            st.markdown(
                f"## 🦠 {pathogen}"
            )

            # Unique mechanisms
            pathogen_mechanisms = (
                pathogen_data["mechanism"]
                .drop_duplicates()
                .tolist()
            )

            for mechanism in pathogen_mechanisms:

                mechanism_data = pathogen_data[
                    pathogen_data["mechanism"]
                    == mechanism
                ]

                st.markdown(
                    f"### ⚙️ {mechanism}"
                )

                # Genes
                genes = (
                    mechanism_data["gene"]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                genes = [
                    g for g in genes
                    if g.strip()
                ]

                if genes:

                    st.markdown(
                        "**Associated genes / proteins:** "
                        + ", ".join(
                            f"`{gene}`"
                            for gene in genes
                        )
                    )


                # Description
                descriptions = (
                    mechanism_data["description"]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                descriptions = [
                    d for d in descriptions
                    if d.strip()
                ]

                if descriptions:

                    st.markdown(
                        "**Mechanistic explanation:**"
                    )

                    for description in descriptions:

                        st.write(
                            description
                        )


                # Evidence
                evidence_values = (
                    mechanism_data["evidence"]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                evidence_values = [
                    e for e in evidence_values
                    if e.strip()
                ]

                if evidence_values:

                    evidence_text = ", ".join(
                        evidence_values
                    )

                    evidence_lower = evidence_text.lower()

                    if "high" in evidence_lower:

                        st.success(
                            f"Evidence: {evidence_text}"
                        )

                    elif "moderate" in evidence_lower:

                        st.warning(
                            f"Evidence: {evidence_text}"
                        )

                    else:

                        st.info(
                            f"Evidence: {evidence_text}"
                        )


                # Papers
                if "paper_title" in mechanism_data.columns:

                    papers = mechanism_data[
                        [
                            "paper_title",
                            "year",
                            "doi"
                        ]
                    ].drop_duplicates()

                    valid_papers = papers[
                        papers["paper_title"]
                        .astype(str)
                        .str.strip()
                        != ""
                    ]

                    if not valid_papers.empty:

                        st.markdown(
                            "**Supporting literature:**"
                        )

                        for _, paper in valid_papers.iterrows():

                            title = str(
                                paper["paper_title"]
                            )

                            year = str(
                                paper["year"]
                            )

                            doi = str(
                                paper["doi"]
                            )

                            if doi and doi != "nan":

                                if not doi.startswith(
                                    "http"
                                ):
                                    doi_url = (
                                        "https://doi.org/"
                                        + doi
                                    )
                                else:
                                    doi_url = doi

                                st.markdown(
                                    f"- [{title}]"
                                    f"({doi_url}) "
                                    f"({year})"
                                )

                            else:

                                st.markdown(
                                    f"- {title} ({year})"
                                )

                st.divider()


    
    # Comparison table
    

    st.subheader(
        "📊 Cross-pathogen comparison"
    )

    comparison_columns = [
        "pathogen",
        "mechanism",
        "gene",
        "evidence"
    ]

    comparison = (
        results[
            [
                c for c in comparison_columns
                if c in results.columns
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )


    
    # Mechanism categories
    

    st.subheader(
        "🧩 Resistance mechanism categories"
    )

    mechanism_counts = (
        results["mechanism"]
        .value_counts()
        .reset_index()
    )

    mechanism_counts.columns = [
        "Mechanism",
        "Number of records"
    ]

    st.dataframe(
        mechanism_counts,
        use_container_width=True,
        hide_index=True
    )


    
    # Scientific warning
    

    st.divider()

    st.warning(
        """
        **Scientific interpretation**

        The mechanisms shown here represent information contained
        in the current knowledge base. A mechanism reported for one
        strain or study should not automatically be interpreted as
        experimentally confirmed for every strain of that pathogen.

        Always verify important findings against the original
        research paper.
        """
    )



# Sidebar


with st.sidebar:

    st.header("📚 Knowledge Base")

    st.write(
        f"File: `{DATA_FILE}`"
    )

    st.metric(
        "Total records",
        len(df)
    )

    st.metric(
        "Drugs",
        df["drug"].nunique()
    )

    st.metric(
        "Pathogens",
        df["pathogen"].nunique()
    )

    st.metric(
        "Mechanisms",
        df["mechanism"].nunique()
    )

    st.divider()

    st.markdown(
        """
        ### ESKAPE

        **E** — *Enterococcus faecium*

        **S** — *Staphylococcus aureus*

        **K** — *Klebsiella pneumoniae*

        **A** — *Acinetobacter baumannii*

        **P** — *Pseudomonas aeruginosa*

        **E** — *Enterobacter* spp.
        """
    )

