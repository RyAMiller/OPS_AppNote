# Supplementary information: Example workflows 

This repository has examples workflows that supplement this paper:

```text
PUT CITATION HERE
```

Currently, two example workflows are presented, one in Python and one in HTML and JavaScript.

## Python

This is an example workflow for Open PHACTS that uses the /pathways/getInteractions call for WikiPathways to retrieve the directed interactions that are involved in the pathway and the source and target of the interaction.  
When running the script, the workflow asks the user which pathway they would like to query.  The script then performs an Open PHACTS API call to the /pathway/getInteractions method and gets the results as JSON.  The results of the call that are parsed by the script are the WikiPathways (WP) interaction ID info from the WP RDF, the type of interaction it is (catalysis, inhibition, or generic directed interaction, for example), and identifiers.org IDs for the source and target of the interactions.  That is what the first part of the script does.

The difficult thing for humans reading this is that, a gene ID comes back from the call as identifiers.org/ensembl/ENSG00000XYZ.  This identifiers.org ID links back to gene or entity that the user is interested in studying further, but if reading the results, it can be difficult to quickly identify it as the gene/protein/RNA/metabolite that is of interest.  To solve this, the workflow script then takes the identifiers.org IDs from the Open PHACTS API call, and performs a simple SPARQL query against the WP RDF to find the label that is associated with that ID.  This means that the alias that is returned for http://identifiers.org/ensembl/ENSG00000105221 becomes AKT2.

The script then writes the results to a file and creates a CSV file with a table that records the original API call CURL at the top.  The first column has info about the types of data, so the first row of this column will be the interaction ID, the second row will be the interaction type, followed by rows for sources and targets.  The rows for the sources and targets also have common names for the IDs, when available.  If an ID is not able to be resolved to an alias, it is given a NA value.

Also note that the API Key and API ID are hardcoded for this example, and if the user wishes to use the workflow, they should replace these elemnts with their own ID info.  

## HTML + JavaScript

A second workflow example (`interactingGenes.html`) is written in HTML and JavaScript using the
[ops.js](https://github.com/openphacts/ops.js/) library. The web page can be opened in a webbrowser and default
to showing interactions for AKT2. Second, for each interacting biological entity (gene, miRNA, drug, etc) found in
pathways, it reports the number that entity has too. That can be clicked for further detail.
