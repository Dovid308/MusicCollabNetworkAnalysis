== *Second-Order Effects: Labels Conditioned on Genre*

To assess the influence of record labels on collaboration patterns, we examined subnetworks for four major genres: Pop, Rock, Hip Hop, and Electronic. The analysis reveals that when controlling for genre, label affiliation exhibits minimal predictive power regarding collaboration structures, with most metrics failing to surpass random expectations.

The Pop subnetwork (294 nodes, 37 edges) demonstrates weak label-based clustering. The homophily ratio (0.3243) and assortativity coefficient (0.0237 versus 0.1239 in the full network) both approach random values. While Blau's Heterogeneity Index (0.0900) suggests marginally more uniform connections than the full network (0.2745), statistical tests confirm this difference is insignificant. These results indicate that label affiliation does not meaningfully structure collaborations even within this homogeneous genre.

#figure(
  grid(
        columns: 1,
        gutter: 2mm,    // space between columns
        image("../results/pop/analysis_results/labels/homophily_distribution.png", width: 80%),
        image("../results/pop/analysis_results/labels/assortativity_distribution.png", width: 80%),
    ),
  caption: [Comparison of observed homophily ratio and assortativity values against null model distributions, specifically for the Pop subgraph]
) <homophily-comparison-POP-label>

The Rock subnetwork (250 nodes, 9 edges) suffers from extreme sparsity, rendering its metrics unreliable. Though the homophily ratio (0.4444) appears elevated and Blau's Index (0.0667) suggests homogeneity, the near-zero assortativity (0.0110) and limited edge count prevent definitive conclusions about label effects.

In contrast, the dense Hip Hop subnetwork (226 nodes, 301 edges) provides robust evidence against label-driven collaboration patterns. Both homophily (0.2724) and assortativity (0.0455) fall below the full network averages (0.3425 and 0.1239 respectively), while Blau's Index (0.3778) indicates substantial cross-label collaboration. This contradicts industry assumptions about Hip Hop's label-centric nature.

The Electronic subnetwork (122 nodes, 20 edges) shows negative assortativity (-0.0850), suggesting a slight tendency toward cross-label collaborations. However, the limited number of edges makes this finding unreliable, and statistical validation aligns these patterns with random distributions. As with the other genres, we find no evidence of meaningful label-based homophily within this genre-specific context.

_Methodological Considerations:_

The selected genres (Pop, Rock, Hip Hop) represent broad musical categories encompassing diverse artistic styles. This heterogeneity may dilute potential label effects. Conversely, niche genres like Classical (represented by only ~15 artists in our dataset) might exhibit stronger label homophily due to their specialized markets and tighter artistic communities. However, our sample size precludes definitive analysis of such genre-specific dynamics


This second-order analysis systematically demonstrates the absence of significant label-based homophily when examining collaborations within individual genres. While genre membership strongly predicts collaboration patterns, our findings show that record label affiliations do not meaningfully influence artist partnerships when controlling for musical genre. 

// DRAFT
// - Pop
//   - Nodes: 294
//   - Edges: 37

//   Homophily Ratio: 0.3243 (basically unchanged)
//   Attribute Assortativity Coefficient: 0.0237 (lower result wrt all-genres graph) (all: 0.1239)
//   Average Blau's Heterogeneity Coefficient: 0.0900 (better) (all: 0.2745)
//   EI Index: not a significant improvement (basically unchanged)
//   "bad" results of Homophily and assortativity in the statistical validation with rewiring and attribute shuffling, suggesting that it is not significantly different from random.

// - Rock

//   The small relevance of this is already given by the small number of edges in proportion to the number of nodes (- Nodes: 250 Edges: 9). For this reason, the results are very influenced by this and for example homophily ratio is higher (0.4444) and Average Blau's Heterogeneity Coefficient is lower (0.0667) (better) nevertheless, assortativity coefficient is lower (0.0110) and EI Index is not a significant improvement (basically unchanged). The statistical validation with rewiring and attribute shuffling suggests that it is not significantly different from random.

// - Hip hop

//     - Nodes: 226
//     - Edges: 301 (differently from the previous it is has a lot of connections)
//     But still worse results wrt all-genres graph:
//     Homophily Ratio (original): 0.2724 (all: 0.3425)
//   Average Blau's Heterogeneity Index: 0.3778 (all: 0.2745)
//   Attribute Assortativity Coefficient: 0.0455 (all: 0.1239)
//   EI Index: not a significant improvement (basically unchanged)
//   The statistical validation with rewiring and attribute shuffling suggests that it is not significantly different from random.

// - Electronic
//   - Nodes: 122
// - Edges: 20 (not significant)

// Homophily Ratio (original): 0.2500
// Average Blau's Heterogeneity Index: 0.1106
// Attribute Assortativity Coefficient: -0.0850

// Addirittura assortativity coefficient negativo che indica eterofilia

// Neanche da dirlo che annche qui è come random.