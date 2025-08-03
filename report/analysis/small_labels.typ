== Unaggregated Label Network
// QUESTO FILE È DA SISTEMARE
=== Homophily Analysis

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
  caption: [Homophily measurements in the unaggregated label network]
) <homophily-metrics-unaggregated-label>

#figure(
  image("../results/small_labels/ei_index_major_label.png", width: 90%),
  caption: [E-I Index by label in the unaggregated label network]
) <ei-index-plot-unaggregated-label>

==== Statistical Validation

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
  caption: [Comparison with null models in the unaggregated label network]
) <null-comparison-unaggregated-label>

#figure(
  grid(
        columns: 1,
        gutter: 2mm,    // space between columns
        image("../results/small_labels/homophily_distribution.png", width: 80%),
        image("../results/small_labels/assortativity_distribution.png", width: 80%),
    ),
  caption: [Comparison of observed homophily ratio and assortativity values against null model distributions in the unaggregated label network]
) <homophily-comparison-unaggregated-label>

=== Community Detection Results
#figure(
  table(
    columns: 2,
    stroke: none,
    table.header([*Metric*], [*Value*]),
    table.hline(),
    [Nodes Analyzed], [421],
    [Louvain Communities], [13],
    [Label-based Communities], [5],
    [Louvain Modularity], [0.6140],
    [Label-based Modularity], [0.1845],
  ),
  caption: [Community detection comparison in the unaggregated label network]
) <community-metrics-unaggregated-label>

#figure(
  image("../results/small_labels/community_stacked_bar_percent_fixed.png", width: 90%),
  caption: [Label composition of algorithmically detected communities in the unaggregated label network]
) <community-composition-unaggregated-label>