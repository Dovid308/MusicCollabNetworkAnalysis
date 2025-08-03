=== *1-hop Neighborhood - Genre*
// === Basic Network Properties

// #figure(
//   table(
//     columns: 2,
//     stroke: none,
//     table.header([*Metric*], [*Value*]),
//     table.hline(),
//     [Nodes], [1,289],
//     [Edges], [1,014],
//     [Density], [0.001522],
//     [Average Degree], [1.57],
//     [Median Degree], [0.00],
//     [Standard Deviation Degree], [3.16],
//     [Max Degree], [27],
//     [Connected Components], [1,005],
//     [Largest Component Size], [421 (32.69%)]
//   ),
//   caption: [Basic network properties of the two-hop genre network.]
// ) <network-properties-1hop-genre>

==== *Genre Distribution and Homophily Analysis*

// #figure(
//   table(
//     columns: 2,
//     stroke: none,
//     table.header([*Genre*], [*Count (%)*]),
//     table.hline(),
//     [Pop], [298 (23.14%)],
//     [Rock], [253 (19.63%)],
//     [Hip Hop], [234 (18.16%)],
//     [Electronic], [124 (9.62%)],
//     [Other], [112 (8.69%)],
//     [R&B], [108 (8.38%)],
//     [Punk], [49 (3.81%)],
//     [Metal], [40 (3.10%)],
//     [Unknown], [39 (3.03%)],
//     [Country], [21 (1.63%)],
//     [Latin], [19 (1.47%)],
//     [Classical], [15 (1.17%)],
//     [Reggae], [7 (0.54%)],
//   ),
//   caption: [Genre distribution in the two-hop genre network]
// ) <genre-distribution-1hop>

The genre distribution remains broadly stable with 1-hop expansion, but some notable shifts emerge, e.g. hip hop increases from 17.74% to 23.47%, and the genre classical grows from 1.14% to 9.16%. This rise anticipates the high homophily we will observe for classical, where artists tend to collaborate predominantly within their own genre.
//simone l'ultima frase non la capisco
//ma noi non osserviamo mai direttamente lomofilia per il genere clasical, o almeno non mi sembra, forse è questo che non mi è chiaro a questo punto. 


All homophily metrics increase in the 1-hop network, with the assortativity coefficient rising from 0.3653 to 0.6243.

The E-I Index pattern also becomes more pronounced, reinforcing the observation that some genres exhibit stronger internal collaboration than others.

// RIPETITIVO:

// #figure(
//   table(
//     columns: 2,
//     stroke: none,
//     table.header([*Homophily Metric*], [*Value*]),
//     table.hline(),
//     [Homophily Ratio], [0.4321],
//     [Attribute Assortativity Coefficient], [0.2012],
//     [Average Blau's Heterogeneity Index], [0.1987],
//   ),
//   caption: [Homophily measurements in the two-hop genre network]
// ) <homophily-metrics-1hop-genre>

// #figure(
//   image("../results/1hop/genre/ei_index_main_genre.png", width: 90%),
//   caption: [E-I Index by genre in the two-hop genre network]
// ) <ei-index-plot-1hop-genre>

// ==== Statistical Validation

// #figure(
//   table(
//     columns: 3,
//     stroke: none,
//     table.header([*Model*], [*Avg Homophily ratio*], [*Avg Assortativity*]),
//     table.hline(),
//     [Observed], [0.4321], [0.2012],
//     [Rewiring Model], [0.2656], [-0.0050],
//     [Attribute Shuffling], [0.1441], [-0.0049],
//     [P-value], [< 0.000001], [< 0.000001],
//   ),
//   caption: [Comparison with null models in the two-hop genre network]
// ) <null-comparison-1hop-genre>

// #figure(
//   grid(
//         columns: 1,
//         gutter: 2mm,    // space between columns
//         image("..//resu1hop/genre/homophily_distribution.png", width: 80%),
//         image("../results/1hop/genre/assortativity_distribution.png", width: 80%),
//     ),
//   caption: [Comparison of observed homophily ratio and assortativity values against null model distributions in the two-hop genre network]
// ) <homophily-comparison-1hop-genre>

// === Community Detection Results

// #figure(
//   table(
//     columns: 2,
//     stroke: none,
//     table.header([*Metric*], [*Value*]),
//     table.hline(),
//     [Nodes Analyzed], [421],
//     [Louvain Communities], [13],
//     [Genre-based Communities], [12],
//     [Louvain Modularity], [0.6140],
//     [Genre-based Modularity], [0.1845],
//   ),
//   caption: [Community detection comparison in the two-hop genre network]
// ) <community-metrics-1hop-genre>

// #figure(
//   image("../results/1hop/genre/community_stacked_bar_percent_fixed.png", width: 90%),
//   caption: [Genre composition of algorithmically detected communities in the two-hop genre network]
// ) <community-composition-1hop-genre>