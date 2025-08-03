#import "@preview/charged-ieee:0.1.3": ieee

#show: ieee.with(
  title: [Graph-Based Analysis of Collaborations in Music: Identifying Key Collaboration Factors],
  abstract: [
    This project investigates the structural patterns behind artist collaborations in the contemporary music industry using a graph-based approach. By modeling the Spotify artist network as a graph, we analyze how specific artist features influence the formation of these connections. In particular, we focus on two key attributes: musical genre and record label affiliation. Using standard graph analysis techniques we explore how these features relate to network structure and cluster formation. Our results highlight musical genre as the most significant driver of collaborations, with label affiliation  playing a marginal role. The study provides a data-driven perspective on how artist communities are shaped in the modern music ecosystem.
  ],
  authors: (
    (
      name: "Simone Caregnato",
      organization : "2154604",
      email: "simone.caregnato@studenti.unipd.it"
    ),
    (
      name: "Giacomo D'Ovidio",
      organization: "2142907",
      email: "giacomo.dovidio@studenti.unipd.it"
    ),
  ),
  index-terms: (),
  bibliography: bibliography("refs.bib"),
  figure-supplement: [Fig.],
)

= *Introduction*


== *Motivation*

In recent years, collaborations between artists have become a defining trend in the music industry. Popular albums and chart-topping tracks frequently feature guest appearances, and certain artists seem to reappear across numerous projects. This recurring pattern raises a key question: Are these collaborations genuinely the result of artistic choice, or are they influenced by external factors such as commercial strategies, genre alignment, or record label decisions?

This project stems from that question. Our aim is to explore the underlying dynamics of artist collaborations by analyzing them through the lens of network theory. A graph structure offers a natural way to represent these relationships, where artists are nodes and collaborations are edges, enabling a systematic analysis of how connections form.

We specifically focus on two artist features that are both relevant and accessible through Spotify's public API:

1. *Musical genre*, which may reflect artistic compatibility or audience overlap.

2. *Record label affiliation*, which can influence collaborations through contractual or promotional decisions.

By investigating how these features correlate with collaboration patterns, we aim to better understand the forces that shape modern musical partnerships.

== *Graph Structure and Data Collection *
In our analysis, the artist collaboration network is modeled as a graph where nodes represent artists and edges represent collaborations, specifically featuring relationships. A collaboration is defined as the presence of a guest artist (featuring) on one or more tracks within the most recent album released by a given artist. To ensure the relevance and recency of the data, we include only artists who have released an album after 01/01/2023.

The graph construction process is based on data obtained from two main sources: the Last.fm API [@lastfmAPI] and the Spotify API [@spotifyAPI].

We begin by using the Last.fm API to retrieve a list of popular artists, as determined by their listener counts. For each artist identified, we then use the Spotify API to fetch their latest album. From this album, we extract the list of collaborators i.e. featured artists appearing on the tracks. Only collaborations with artists already present in the dataset are retained in the graph, no additional artists are added at this stage, unless the analysis follows the 1-hop expansion method described in @1-hop.

=== *Attribute Collection*

The graph's node attributes are collected in the following ways:

The musical genre of each artist is retrieved directly from the Last.fm API, which provides tags based on user interactions and artist categorization.

The record label is obtained from the metadata associated with the artist's latest album on Spotify. In cases where the album lists multiple labels or distributors, we exclude the artist from the dataset to avoid ambiguity in the affiliation. A notable example of this situation is the latest collaborative album by Future and Metro Boomin, which is released under several different labels and thus is not included in our final graph. These cases are relatively rare, representing approximately 3% of the collected dataset, and therefore do not significantly impact the overall analysis.



=== *Attribute Normalization* <attribute-normalization>

To reduce fragmentation and ensure consistent analysis, a remapping process is applied to both genre and label attributes. This involves grouping a wide range of subgenres and sublabels into a smaller set of main categories. The goal is to capture overarching patterns without being distorted by overly specific or inconsistently labeled data.

For musical genres, many subgenres are mapped to the following top-level categories:
Pop, Hip hop, Rock, Metal, Punk, Electronic, R&B, Latin, Country, Reggae, Classical, Other.

For record labels, sublabels are consolidated under their parent companies or marked as Other. The main categories are:
Warner Music Group, Universal Music Group, Sony Music Entertainment, BMG,  Other.

#figure(
  image("top2000hiphopgraphforthereport.png", width: 110%),
  caption: [
    Example of the resulting artist collaboration graph, with record label attributes normalized,
    relative to the Hip Hop macro-genre
  ]
)

== *Methodology and Metrics* <methodology>

To systematically examine the structural properties and attribute-based patterns across different networks, we employ a consistent framework organized into three main components. This standardized approach ensures statistical rigor and enables meaningful comparisons between networks to extract robust conclusions.

=== *Basic Network Properties*

Each network analysis begins with fundamental structural metrics that characterize the overall topology. These measurements include:

- *Network size and connectivity*: Number of nodes and edges, network density, and degree distribution statistics (mean, median, standard deviation, and range)
- *Component structure*: Number of connected components, size of the largest component, and its relative proportion of the total network


=== *Homophily and Assortativity Analysis*

The core of our analysis focuses on understanding how nodes with similar attributes tend to connect more frequently than expected by chance. This is accomplished by employing several complementary metrics:

- *Homophily ratio*: The proportion of edges connecting nodes of the same attribute value
- *Blau's Heterogeneity Index*: Measures the diversity of attribute connections for each node
- *E-I Index by attribute*: Quantifies the tendency for each attribute category to form internal versus external connections
- *Attribute assortativity coefficient*: Measures the overall tendency for similar attributes to connect, ranging from -1 (perfect disassortativity) to +1 (perfect assortativity)


==== *Statistical Validation*

To determine whether observed patterns are statistically significant, we compare our results against two null models:

- *Rewiring model*: Preserves degree sequence while randomizing connections
- *Attribute shuffling*: Maintains network structure while randomizing attribute assignments

Statistical significance is assessed through 100 iterations of each null model type, with p-values calculated to determine if observed homophily and assortativity exceed random expectations. The comparative analysis is illustrated through histogram plots showing the distribution of homophily ratios and assortativity coefficients from null models against the observed values, clearly demonstrating statistical significance.

=== *Community Detection*

This final component of analysis is performed on the largest connected component of each graph. We employ the Louvain algorithm to identify communities that maximize modularity without prior knowledge of attribute labels.

To analyze the results, we compare the modularity scores between attribute-based and algorithmically detected partitions. Moreover, a more intuitive visualization is presented through percentage-based stacked bar charts, where each bar represents a detected community and colors indicate the proportion of different attribute categories within that community.


== *Conducted Analyses*
Our analysis is applied multiple times to different graphs.
Initially we examine the full network of collaborations, by focusing each on the genre and label attributes. 

=== *Second-Order Effects by Genre*
Since genre exhibits strong clustering behavior in the global network, we further investigate whether label-based patterns become more evident when we control for genre.
To this end, we isolate subgraphs corresponding to the four largest genres —Pop, Rock, Hip hop, and Electronic— and perform community detection and homophily analysis with respect to the label attribute.

This second-order analysis allows us to examine whether, within genre-specific communities, labels act as organizing principles.

=== *1-hop Neighborhood Network Expansion* <1-hop>
To better capture the complexity of collaboration patterns in the music industry, we extend the traditional direct-link approach through a 1-hop neighborhood network expansion. While the original graph only considered edges between artists in the top-N list retrieved via the Last.fm API, this expanded representation relaxes that constraint by incorporating both first-degree collaborators of top artists and the connections among those secondary artists themselves. For instance, if a top artist A has collaborated with a non-top artist B, and B has also collaborated with another non-top artist C that collaborated with A, both links A-B and B-C are included in the network.


Due to the substantial increase in node count introduced by second-degree collaborations, we take into account only 1000 top artists based on their Last.fm popularity, and then used the 1-hop expansion to include their collaborators. 



#pagebreak()

= *Obtained Results*
While all analyses are conducted according to the methodology outlined in @methodology, the results are not always presented in the same structured manner. This choice is made to enhance readability and to focus attention on the most relevant findings.




For the full set of results, including all data and figures, please refer to the [*report/results*]) directory in the #link("https://github.com/Dovid308/MusicCollabNetworkAnalysis") \ repo, where the results are divided into subdirectories based on the graphs analyzed.


#include "analysis/genre_results.typ"

#include "analysis/label_results.typ"


#pagebreak()
#include "analysis/label_by_genre.typ"
#pagebreak()
#include "analysis/1hop_genre.typ"

#include "analysis/1hop_label.typ"



= *Conclusion*

== *Main Findings*

Across all analyses, genre consistently emerged as the stronger predictor of collaboration. The genre network displayed moderate homophily (homophily ratio: 0.5362; assortativity: 0.3653). In contrast, label-based networks exhibited weaker homophily (homophily ratio: 0.3425; assortativity: 0.1239), and communities detected algorithmically were not properly aligned with actual labels.

Second-order analyses, where label effects were examined after filtering the collaboration graph based on genre, confirmed that label affiliation has minimal influence on collaboration patterns. Even in dense genre graphs such as the Hip Hop one, label-driven clustering appears to be weak.

Expanding the network by 1-hop neighborhood increased all homophily-related metrics, especially for genre, where assortativity hit 0.6243. On the other hand, the 1-hop label network showed increased homophily, but a decrease in label-based modularity.

Collectively, these analyses reveal that genre is the primary organizing principle behind collaborations. The role of record labels in defining these collaborations is much weaker, directly challenging our initial expectation that label affiliation would be a significant driver.

== Limitations and Future Directions

We recognize several limitations in our methodology that could have influenced the results. In this section we outline these limitations and hypotethesize how they could be addressed.

Firstly, our approach to constructing the collaboration graph treated all collaborations equally, not weighting the number of times artists collaborated. A single collaboration held the same weight as joint projects. Future work could benefit from incorporating weighted edges based on collaboration frequency.

Our decision to analyze the global music market presents a second limitation. This market is in fact a composite of geographically localized markets. This inherent diversity might obscure the true influence of specific factors like label affiliation. Future research could benefit from focusing on more homogeneous markets, such as the European, US, or individual national markets.

Finally, the categorization of record labels into five macro-groups was, to some extent, arbitrary. While this simplification made our analysis manageable, it's quite possible that a more detailed classification of labels would reveal more subtle collaboration trends. Future analyses could explore this direction by refining the label categorization process.