== *Attribute: Label*

=== *Basic Network Properties*
Network properties are nearly the same as for the genre network, only with a smaller number of nodes (1289) and edges (832), as we did not include artists whose last album was distributed by more than one labels.

=== *Label Distribution and Homophily Analysis*

#figure(
  table(
    columns: 2,
    stroke: none,
    table.header([*Label*], [*Count (%)*]),
    table.hline(),
    [Other], [456 (35.38%)],
    [Warner Music Group], [319 (24.75%)],
    [Universal Music Group], [316 (24.52%)],
    [Sony Music Entertainment], [150 (11.64%)],
    [BMG], [48 (3.72%)],
  ),
  caption: [Label distribution in the network]
) <label-distribution>

#figure(
  table(
    columns: 2,
    stroke: none,
    table.header([*Homophily Metric*], [*Value*]),
    table.hline(),
    [Homophily Ratio], [0.3425],
    [Attribute Assortativity Coefficient], [0.1239],
    [Average Blau's Heterogeneity Index], [0.2745],
  ),
  caption: [Homophily measurements]
) <homophily-metrics-label>

#figure(
  image("../results/labels/ei_index_major_label.png", width: 90%),
  caption: [E-I Index by label]
) <ei-index-plot-label>

The label distribution shows a significant proportion of independent artists. However, homophily metrics suggest a weak tendency for artists to collaborate within their own label. The low assortativity coefficient (0.1239) and the moderate homophily ratio (0.3425) indicate limited label-based clustering. This is further supported by the E-I Index, which remains relatively high across all label groups.
// poi mettiamo che siccome non sembrano mostrare homophily ,proviamo a fare un'analisi su più livelli (vedi appunti incontro)

// ANALYSIS

=== *Statistical Validation*

#figure(
  table(
    columns: 3,
    stroke: none,
    table.header([*Model*], [*Avg Homophily ratio*], [*Avg Assortativity*]),
    table.hline(),
    [Observed], [0.3425], [0.1239],
    [Rewiring Model], [0.2462], [-0.0046],
    [Attribute Shuffling], [0.2607], [-0.0074],
    [P-value], [0.000000], [0.000000],
  ),
  caption: [Comparison with null models]
) <null-comparison-label>

#figure(
  grid(
        columns: 1,
        gutter: 2mm,    // space between columns
        image("../results/labels/homophily_distribution.png", width: 80%),
        image("../results/labels/assortativity_distribution.png", width: 80%),
    ),
  caption: [Comparison of observed homophily ratio and assortativity values against null model distributions]
) <homophily-comparison-label>

Despite the relatively low absolute values of homophily and assortativity, statistical validation confirms that these values are significantly higher than what would be expected by chance. Both null models - degree-preserving rewiring and attribute shuffling - yield substantially lower averages, indicating that label affiliation does exert a measurable, though limited, influence on collaboration patterns.

=== *Community Detection Results*
#figure(
  table(
    columns: 2,
    stroke: none,
    table.header([*Metric*], [*Value*]),
    table.hline(),
    [Nodes Analyzed], [383],
    [Louvain Communities], [15],
    [Label-based Communities], [5],
    [Louvain Modularity], [0.6269],
    [Label-based Modularity], [0.0457],
  ),
  caption: [Community detection comparison]
) <community-metrics-label>
#figure(
  image("../results/labels/community_stacked_bar_percent_fixed.png", width: 90%),
  caption: [Label composition of algorithmically detected communities]
) <community-composition-label>

Community detection further supports this interpretation. While the Louvain algorithm identifies 15 communities with a high modularity score (0.6269), grouping artists based solely on their major label affiliation (as defined in @attribute-normalization, where labels were mapped to 5 major categories: Other, Warner, Universal, Sony, and BMG) results in a much lower modularity (0.0457). The barplot reveals that algorithmic communities tend to mix artists from different labels, reinforcing the idea that while labels matter, they are not the dominant factor shaping collaborative structure.
