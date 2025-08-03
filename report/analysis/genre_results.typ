== *Attribute: Genre*

=== *Basic Network Properties*

The network exhibits a sparse structure with limited connectivity between artists. The fundamental structural characteristics are summarized in Table 1.

#figure(
  table(
    columns: 2,
    stroke: none,
    table.header([*Metric*], [*Value*]),
    table.hline(),
    [Nodes], [1,319],
    [Edges], [925],
    [Density], [0.001064],
    [Average Degree], [1.40],
    [Median Degree], [0.00],
    [Standard Deviation Degree], [2.82],
    [Max Degree], [27],
    [Connected Components], [817],
    [Largest Component Size], [421 (31.92%)]
  ),
  caption: [Basic network properties.]
) <network-properties>

=== *Genre Distribution and Homophily Analysis*

#figure(
  table(
    columns: 2,
    stroke: none,
    table.header([*Genre*], [*Count (%)*]),
    table.hline(),
    [Pop], [298 (22.59%)],
    [Rock], [253 (19.18%)],
    [Hip Hop], [234 (17.74%)],
    [Electronic], [124 (9.40%)],
    [Other], [112 (8.49%)],
    [R&B], [108 (8.19%)],
    [Punk], [49 (3.71%)],
    [Metal], [40 (3.03%)],
    [Unknown], [39 (2.96%)],
    [Country], [21 (1.59%)],
    [Latin], [19 (1.44%)],
    [Classical], [15 (1.14%)],
    [Reggae], [7 (0.53%)],
  ),
  caption: [Genre distribution in the network]
) <genre-distribution>

#figure(
  table(
    columns: 2,
    stroke: none,
    table.header([*Homophily Metric*], [*Value*]),
    table.hline(),
    [Homophily Ratio], [0.5362],
    [Attribute Assortativity Coefficient], [0.3653],
    [Average Blau's Heterogeneity Index], [0.2337],
  ),
  caption: [Homophily measurements]
) <homophily-metrics>

// #figure(
//   table(
//     columns: 2,
//     stroke: none,
//     table.header([*Genre*], [*E-I Index*]),
//     table.hline(),
//     [Classical], [-0.5942],
//     [Hip Hop], [-0.1693],
//     [Pop], [0.5593],
//     [Electronic], [0.5856],
//     [Rock], [0.6296],
//     [Latin], [0.6522],
//     [Other], [0.7015],
//     [R&B], [0.7765],
//     [Country], [0.8621],
//     [Metal], [0.8788],
//     [Unknown], [1.0000],
//     [Punk], [1.0000],
//     [Reggae], [1.0000],
//   ),
//   caption: [E-I Index by genre (negative values indicate internal clustering)]
// ) <ei-index>

#figure(
  image("../results/genre/ei_index_main_genre.png", width: 90%),
  caption: [E-I Index by genre]
) <ei-index-plot>

The analysis shows that genres with a strongly negative E-I Index — indicating a higher tendency to form internal
connections — are Classical (-0.5942) and Hip Hop (-0.1693). In contrast, genres with higher positive values
exhibit a clear prevalence of external links over within-group ties: Pop (0.5593), Electronic (0.5856),
Rock (0.6296), Latin (0.6522), R&B (0.7765), Country (0.8621), Metal (0.8788), and Punk, and Reggae,
each reaching the maximum value of 1.0000. 

=== *Statistical Validation*

#figure(
  table(
    columns: 3,
    stroke: none,
    table.header([*Model*], [*Avg Homophily ratio*], [*Avg Assortativity*]),
    table.hline(),
    [Observed], [0.5362], [0.3653],
    [Rewiring Model], [0.2656], [-0.0050],
    [Attribute Shuffling], [0.1441], [-0.0049],
    [P-value], [0.000000], [0.000000],
  ),
  caption: [Comparison with null models]
) <null-comparison>

#figure(
  grid(
        columns: 1,
        gutter: 2mm,    // space between columns
        image("../results/genre/homophily_distribution.png", width: 95%),
        image("../results/genre/assortativity_distribution.png", width: 95%),
    ),
  caption: [Comparison of observed homophily ratio and assortativity values against null model distributions]
) <homophily-comparison>

The analysis confirms the significance of the observed homophily ratio (0.5362) and assortativity coefficient (0.3653) compared to null models. This confirms that the observed genre-based clustering is not a result of random chance.

=== *Community Detection Results*

#figure(
  table(
    columns: 2,
    stroke: none,
    table.header([*Metric*], [*Value*]),
    table.hline(),
    [Nodes Analyzed], [421],
    [Louvain Communities], [13],
    [Genre-based Communities], [12],
    [Louvain Modularity], [0.6140],
    [Genre-based Modularity], [0.1845],
  ),
  caption: [Community detection comparison]
) <community-metrics>

#figure(
  image("../results/genre/community_stacked_bar_percent_fixed.png", width: 90%),
  caption: [Genre composition of algorithmically detected communities]
) <community-composition>

The results show a substantial difference between the modularity scores of the Louvain-detected communities (0.6140) and those grouped by genre (0.1845), indicating that genre alone does not fully explain the observed community structure. While some Louvain communities are relatively homogeneous (e.g., dominated by hip hop or rock), many contain a mix of genres, suggesting that other factors may play a more prominent role in shaping artist communities.
