library("networkD3")
library("feather")
library(htmlwidgets)
library(htmltools)
library(magrittr)

# nodes_path <- "/Users/ashjha/Documents/USF/mod_1/msds593_data_viz/Final Project/processed_data/df_nodes.feather"
# links_path <- "/Users/ashjha/Documents/USF/mod_1/msds593_data_viz/Final Project/processed_data/df_links.feather"

nodes_path <- "data/df_nodes.feather"
links_path <- "data/df_links.feather"

df_nodes <- read_feather(nodes_path)
df_links <- read_feather(links_path)

print(df_nodes)
print(df_links)

sankey_title_string <- "Pitchfork Scores                                                      Peak Position on Billboard Charts"

sankeyNetwork(Links = df_links, Nodes = df_nodes, Source = "score_bucket_index",
              Target = "chart_bucket_index", Value = "count", NodeID = "nodes",
              units = "Albums", fontSize = 20, nodeWidth = 20, 
              fontFamily = "sans-serif", iterations = 0) %>% 
  htmlwidgets::prependContent(htmltools::tags$pre(sankey_title_string))
