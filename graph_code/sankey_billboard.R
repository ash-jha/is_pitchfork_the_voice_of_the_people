## NOTE: PLEASE USE RSTUDIO TO LOAD THIS SCRIPT

library("networkD3")
library("feather")
library(htmlwidgets)
library(htmltools)
library(magrittr)

# Load the nodes and links for the sankey
nodes_path <- "data/df_nodes.feather"
links_path <- "data/df_links.feather"

df_nodes <- read_feather(nodes_path)
df_links <- read_feather(links_path)

# Axis title for the sankey, note that its very hacky because the library is d3 based, so we need to add
# html components

sankey_title_string <- "Pitchfork                                                                                                                                                   Peak Position on 
 Scores                                                                                                                                                      Billboard Charts"
# color_JS <- JS("d3.scaleOrdinal([\"#1A9641\", \"#A6D96A\", \"#FFFFBF\", \"#FDAE61\", \"#D7191C\",
#                \"#1A9641\", \"#A6D96A\", \"#FFFFBF\", \"#FDAE61\", \"#D7191C\"])")

# Colors for the sankey
color_JS <- JS("d3.scaleOrdinal([\"#006d2c\", \"#31a354\", \"#74c476\", \"#bae4b3\", \"#edf8e9\",
                \"#31a354\", \"#74c476\", \"#bae4b3\", \"#edf8e9\"])")

# d3 Sankey generator
sankeyNetwork(Links = df_links, Nodes = df_nodes, Source = "score_bucket_index",
              Target = "chart_bucket_index", Value = "count", NodeID = "nodes",
              units = "Albums", fontSize = 20, nodeWidth = 20,
              fontFamily = "Arial", iterations = 0, colourScale=color_JS) %>% 
                              # Add the title
  htmlwidgets::prependContent(htmltools::tags$pre(sankey_title_string),
                              # Change the font for the title 
                              htmltools::tags$style("pre{font-family:Arial;font-size:15px; margin:0px;font-weight: bold;}"),
                              # Weird fix for wrong color on sankey nodes
                              htmltools::tags$style("svg g g.node:nth-of-type(6) rect{fill:#006d2c !important;}"))

