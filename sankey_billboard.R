library("networkD3")
library("feather")
library(htmlwidgets)
library(htmltools)
library(magrittr)

nodes_path <- "data/df_nodes.feather"
links_path <- "data/df_links.feather"

df_nodes <- read_feather(nodes_path)
df_links <- read_feather(links_path)

print(df_nodes)
print(df_links)

sankey_title_string <- "Pitchfork                                                                                     Peak Position on 
 Scores                                                                              Billboard Charts"
# color_JS <- JS("d3.scaleOrdinal([\"#1A9641\", \"#A6D96A\", \"#FFFFBF\", \"#FDAE61\", \"#D7191C\",
#                \"#1A9641\", \"#A6D96A\", \"#FFFFBF\", \"#FDAE61\", \"#D7191C\"])")
color_JS <- JS("d3.scaleOrdinal([\"#1A9641\", \"#A6D96A\", \"#FFFFBF\", \"#FDAE61\", \"#1A9641\",
               \"#A6D96A\", \"#FFFFBF\", \"#FDAE61\", \"#D7191C\", \"#D7191C\"])")
               
sankeyNetwork(Links = df_links, Nodes = df_nodes, Source = "score_bucket_index",
              Target = "chart_bucket_index", Value = "count", NodeID = "nodes",
              units = "Albums", fontSize = 20, nodeWidth = 20,
              fontFamily = "Arial", iterations = 0, colourScale=color_JS) %>% 
  htmlwidgets::prependContent(htmltools::tags$pre(sankey_title_string),
                              htmltools::tags$style("pre{font-family:Arial;font-size:15px; margin:0px;font-weight: bold;}"))

