== *1-hop Neighborhood- Label* 

=== *Basic Network Properties*

#figure(
  table(
    columns: 2,
    stroke: none,
    table.header([*Metric*], [*Value*]),
    table.hline(),
    [Nodes], [1707],
    [Edges], [6756],
    [Density], [0.004640],
    [Average Degree], [7.92],
    [Median Degree], [2.00],
    [Standard Deviation Degree], [20.04],
    [Max Degree], [121],
    [Connected Components], [464],
    [Largest Component Size], [1172 (68.66%)]
  ),
  caption: [Basic network properties of the one-hop label network.]
) <network-properties-1hop>

=== *Label Distribution and Homophily Analysis*
The label distribution remains broadly consistent when including 1-hop neighbors. The major labels show similar proportions, with Warner Music Group increasing from 24.75% to 27.77% and Sony Music Entertainment from 11.64% to 13.06%. Minor labels such as BMG slightly decrease, but these variations do not significantly affect the overall distribution.

#figure(
  table(
    columns: 2,
    stroke: none,
    table.header([*Homophily Metric*], [*Value*]),
    table.hline(),
    [Homophily Ratio], [0.4904],
    [Attribute Assortativity Coefficient], [0.1608],
    [Average Blau's Heterogeneity Index], [0.3102],
  ),
  caption: [Homophily measurements in the one-hop label network]
) <homophily-metrics-1hop>

#figure(
  image("../results/1hop/labels/ei_index_major_label.png", width: 90%),
  caption: [E-I Index by label in the one-hop label network]
) <ei-index-plot-1hop>

Expanding the network to include one-hop connections leads to a notable increase in all homophily-related metrics: the homophily ratio rises from 0.3425 to 0.4904, assortativity increases from 0.1239 to 0.1608, and Blau's index also grows. Interestingly, in the 1-hop setting, the E-I Index for Warner Music Group turns negative, indicating that Warner-affiliated artists collaborate more within their own label than with others. This is a sign of internal cohesion and contrasts with the previous labels network, where all labels showed positive E-I values.

==== *Statistical Validation and Community Detection*

Again, the observed homophily and assortativity are significantly higher than in the null models (p < 0.000001). Compared to the original network, the increase in both metrics is substantial when including 1-hop neighbors: homophily rises from 0.3425 to 0.4904 and assortativity from 0.1239 to 0.1608.


However, community detection tells us something different - Louvain and label-based modularity both decrease (0.6140 -> 0.5050 and 0.1845 -> 0.0944), indicating that extending the network with 1-hop results in more mixed and less label-aligned communities.

#figure(
  grid(
    columns: 2,
    gutter: 5mm,
    table(
      columns: 3,
      stroke: none,
      table.header([*Model*], [*Avg Homophily ratio*], [*Avg Assortativity*]),
      table.hline(),
      [Observed], [0.4904], [0.1607],
      [Rewiring Model], [0.3684], [-0.0402],
      [Attribute Shuffling], [0.2605], [-0.0044],
      [P-value], [0.000000], [0.000000],
    ),
    table(
      columns: 2,
      stroke: none,
      table.header([*Metric*], [*Value*]),
      table.hline(),
      [Nodes Analyzed], [1172],
      [Louvain Communities], [12],
      [Label-based Communities], [6],
      [Louvain Modularity], [0.0500],
      [Label-based Modularity], [0.0943],
    ),
  ),
  caption: [Comparison of homophily and assortativity metrics with null models, and community detection results in the one-hop label network]
) <homophily-comparison-1hop-labels>

