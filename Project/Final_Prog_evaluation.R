##########################################################################################################################################
# Find hierarchical markers
# Authors: Bixuan Wang, Muzi Li, Hyeon Jin Cho, Dongze He
# Last updated: 12/19/2019
##########################################################################################################################################

#=========================================================================================#
# Set some global options
#=========================================================================================#
options(contrasts=c("contr.treatment", "contr.poly"))
options(max.print=1e6)
options(digits=12)
options(echo=TRUE)
#options(warn=-1)
#options(error=utils::recover)
set.seed(17)

#=========================================================================================#
# Loading Package Libraries
#=========================================================================================#

library(Seurat)
library(tximport)
library(pcaReduce)
library(igraph)
library(dplyr)
library(Rtsne)
library(ggplot2)

#===============================================================================================================================#
#==============#
# Usage         :
#==============#
# hierarchical_structre <- function(exprs_matrix, 
#                                   nbt, 
#                                   q)

#==============#
# Description   :
#==============#
# Function to run PCAReduce using the expression matrix.
# Query the cells included in a node's children, it will be 2 matrice included in a list, each matrix
# is a exprs matrix of a subpopulation. 
# For example, the cluster Level1_1 has two children clusters, Level2_1 and Level3_2, 
# the function will return the exprs of cells in the cluster Level2_1 as a matrix, 
# and the exprs of cells in the cluster Level3_2.

hierarchical_structre <- function(exprs_matrix, 
                                  nbt = 1, 
                                  q = 10)
  {
  Output_M <- PCAreduce(Input, nbt=nbt, q=q, method='M')
  hs <- Output_M[[1]]
  # Since there are redundant patterns, so we just take the unique pattern
  hs_unique <- unique(hs)[,seq(q,1)]
  
  # PCA reduce stops at K = 2, so we need to create a common ancestor by ourself
  hs_unique <- cbind("root" = rep(1,nrow(hs_unique)),(hs_unique))
  
  # Since in each K iteration, the cluster order starts from 1, 
  # so we need to identify the clusters in each iteration, 
  # I name it as Level `K` _ (# of cluster)
  # for example, Level1_1, Level 31_1
  
  ## First step is build up a exmpty matrix
  hs_unique_label <- matrix(NA,nrow = nrow(hs_unique),ncol = 0)
  
  ## for each column(K), get the cluster labels for this column and combine it as a matrix.
  for (cols in seq(nrow(hs_unique))) {
    hs_unique_label <- cbind(hs_unique_label, paste0("Lv",cols,"_", hs_unique[,cols]))
  }
  
  # build the hierarchical graph using igraph package
  
  ## First, get a empty graph with all nodes(with the same size of hs_unique_label
  hierarchical_graph <- igraph::graph.empty(n =length(unique(c(hs_unique_label))),directed = TRUE)
  
  # Second, change the node names in the graph
  V(hierarchical_graph)$name <- unique(c(hs_unique_label))
  
  # Third, assign the edges according to the hierarchical structure we get
  for (i in seq(nrow(hs_unique_label))) {
    edge_path <- unique(hs_unique_label[i,])
    edge_path <- edge_path[c(1, rep(seq(2,length(edge_path)-1), each = 2), length(edge_path))]
    hierarchical_graph = add_edges(graph = hierarchical_graph,edge_path)
  }
  hierarchical_graph <- simplify(graph = hierarchical_graph)
  
  # Plot it you can see that there are a bunch of redundant nodes, which ar ethe linear paths in the graph
  
  # plot(hierarchical_graph,layout=layout_as_tree,vertex.label.color="black", vertex.label.dist=1,
  #      vertex.size=2,edge.arrow.size = .1, vertex.label="")
  
  # collaps a linear path to a single node and do that for the whole graph
  
  ## First step is get all the vertice in the graph, which will be iterated one by one
  node_names <- V(hierarchical_graph)$name
  
  # Do the collapsing step for every leave. 
  # The procedure is that if the out degree of a leaf's parent(cuz it is a tree, every node has only a parent)
  # is 1, we will know that the leaf and its parent are the parts of linear path, so I will remove the parent, and assign
  # a edge from parent's partent to the leaf. and do this step for all leave.
  
  for(i in 1:vcount(hierarchical_graph)){
    # specify current working node
    current_node <-  node_names[i]
    if(degree(graph = hierarchical_graph,v = current_node, mode = "out") == 1 &
       degree(graph = hierarchical_graph,v = current_node, mode = "in") == 1){
      hierarchical_graph <- hierarchical_graph + edge(neighbors(graph = hierarchical_graph,v = current_node,mode = "in")$name,neighbors(graph = hierarchical_graph,v = current_node,mode = "out")$name)
      hierarchical_graph <- hierarchical_graph -current_node
    }
  }
  
  # Now we updated the node names of the graph, next we need to update the graph
  hierarchical_graph <- graph_from_data_frame(igraph::as_data_frame(hierarchical_graph)) %>% simplify
  
  # write.csv(as_data_frame(hierarchical_graph), file = "pbmc4K_edgelist",quote = F)
  # Here is the result!
  
  # Query the hierarchical structure 
  plot(hierarchical_graph,layout=layout_as_tree,vertex.label.color="black", vertex.label.dist=0,
       vertex.size=15, edge.arrow.size = .1, vertex.label.cex = 0.5)
  
  return(list("hierarchical_graph" = hierarchical_graph, "hs" = hs))
}
#===============================================================================================================================#



#===============================================================================================================================#
#==============#
# Usage         :
#==============#
# find_children_exprs <- function(node_name, 
#                                 hierarchical_graph, 
#                                 hs)

#==============#
# Description   :
#==============#
# Function to find the expression of children clusters of a node

find_children_exprs <- function(node_name, 
                                hierarchical_graph, 
                                hs){
  # Returns the exprs matrice of the node's two children population
  exprs_list = list()
  children <- neighbors(graph = hierarchical_graph,v = node_name,mode = "out")$name
  for (ichild_index in seq(length(children))) {
    ichild = children[ichild_index]
    ichild_children = names(bfs(graph = hierarchical_graph,root = ichild,neimode = "out",order = T,unreachable = FALSE)$order)
    ichild_leaves <- ichild_children[grep(paste0("Lv", q+1), ichild_children)]
    involved_leave = sapply(strsplit(ichild_leaves, paste0("Lv", q+1,"_")), function(x) x[2])
    exprs_list[[ichild]] <- exprs[,which(hs[,1] %in% involved_leave)]
  }
  return(exprs_list)
}

#===============================================================================================================================#



#===============================================================================================================================#
#==============#
# Usage         :
#==============#
# find_children_exprs <- function(node_name, 
#                                 hierarchical_graph, 
#                                 hs)

#==============#
# Description   :
#==============#
# Function to find the expression of children clusters of a node


find_diff_genes <- function(pbmc,hierarchical_graph,hs){
  queue <- c("Lv1_1")
  marker <- list()
  parent <- unique(ends(hierarchical_graph, E(hierarchical_graph))[,1])
  while (length(queue)>0){
    node <- queue[1]
    if (node %in% parent){
      #----------find differentially expressed genes------
      child_list <- find_children_exprs(node_name = node, hierarchical_graph = hierarchical_graph, hs = hs)
      c1.name <- names(child_list)[1]
      c2.name <- names(child_list)[2]
      message(paste0('Comparing', c1.name, c2.name))
      c1 <- child_list[[c1.name]]
      c2 <- child_list[[c2.name]]
      pbmc <- SetIdent(object = pbmc, cells = colnames(c1), value = c1.name)
      pbmc <- SetIdent(object = pbmc, cells = colnames(c2), value = c2.name)
      pbmc.markers <- FindMarkers(pbmc, ident.1 = c1.name, ident.2 = c2.name, min.pct = 0.25)
      pbmc.markers <- pbmc.markers[pbmc.markers$p_val_adj<0.01,]
      if (log2(length(child_list))>5){
        n <- log2(length(child_list))
      } else{n <- 5}
      top.c1 <- row.names(pbmc.markers[order(pbmc.markers$avg_logFC, decreasing=T),])[1:n]
      top.c2 <- row.names(pbmc.markers[order(pbmc.markers$avg_logFC),])[1:n]
      marker[[c1.name]] <- top.c1
      marker[[c2.name]] <- top.c2
      queue <- c(queue[-1], c1.name, c2.name)
      
      #-----------generate plots--------------
      #png(paste0(c1.name,'_','vlnplot.png'))
      #pic=VlnPlot(pbmc, features = marker[[c1.name]][1])
      #print(pic)
      #dev.off()
      
      #png(paste0(c2.name,'_','vlnplot.png'))
      #pic=VlnPlot(pbmc, features = marker[[c2.name]][1])
      #print(pic)
      #dev.off()
      
      features <- unique(as.character(unlist(marker)))
      exp <- rbind(t(c1[features,]), rbind(t(c2[features,])))
      tsne <- Rtsne(exp, perplexity=10, check_duplicates = FALSE)
      cluster <- as.factor(c(rep(c1.name,ncol(c1)), rep(c2.name,ncol(c2))))
      tsne.df <- as.data.frame(tsne$Y)
      tsne.df$cluster <- cluster
      png(paste0(c1.name,'_',c2.name,'_tsne2.png'))
      pic <- ggplot(tsne.df, aes(x=V1, y=V2, color=cluster)) +
        geom_point(size=1) +
        labs(title = paste0(c1.name,' vs ', c2.name), x='tSNE_1', y='tSNE_2') + 
        theme(axis.line = element_line(colour = "black"),
              panel.grid.major = element_blank(),
              panel.grid.minor = element_blank(),
              panel.border = element_blank(),
              panel.background = element_blank(),
              legend.text = element_text(size=20),
              axis.text.x = element_text(size=20),
              axis.text.y = element_text(size=20),
              axis.title = element_text(size=20),
              plot.title = element_text(size=20, face='bold', hjust=0.5),
              legend.title = element_text(size=20)) 
      print(pic)
      dev.off()
      
      pbmc <- RunPCA(pbmc, features = features)
      pbmc <- RunTSNE(pbmc, check_duplicates = FALSE)
      png(paste0(c1.name,'_',c2.name,'_dimplot.png'))
      pic <- DimPlot(pbmc, reduction = "tsne") + 
        theme(legend.text = element_text(size=20),
              axis.text.x = element_text(size=20),
              axis.text.y = element_text(size=20),
              axis.title = element_text(size=20))
      print(pic)
      dev.off()
      
      png(paste0(c1.name,'_',c2.name,'_featureplot.png'))
      pic <- FeaturePlot(pbmc, features = c(marker[[c1.name]][1], marker[[c2.name]][1]), combine = FALSE)
      pic <- lapply(X = pic, FUN = function(x) x + theme(plot.title = element_text(size = 20),
                                                         legend.text = element_text(size=15),
                                                         axis.text.x = element_text(size=20),
                                                         axis.text.y = element_text(size=20),
                                                         axis.title = element_text(size=20)))
      pic <- CombinePlots(plots = pic)
      print(pic)
      dev.off()
    } else{queue <- c(queue[-1])}
  }
  return(list(marker,pbmc))
}

#===============================================================================================================================#




#===============================================================================================================================#
#==============#
# Usage         :
#==============#
# performance_validation <- function(original_hierarchical_structre,
#                                    prediction_hierarchical_structre){

#==============#
# Description   :
#==============#
# Function to judge the performance of our prediction


performance_validation <- function(original_hierarchical_structre,
                                   prediction_hierarchical_structre){
  original_hs <- original_hierarchical_structre$hs
  prediction_hs <- prediction_hierarchical_structre$hs
  q = ncol(original_hs) + 1
  comparison_result <- matrix(0, ncol = 2, nrow = q)
  colnames(comparison_result) <- c("Cluster", "Precision")
  comparison_result[,1] <- 1:q
  
  for (original_clusters in seq(q)) {
    temp_diff <- c()
    real <- rownames(original_hs[which(original_hs[,1] == as.character(original_clusters)),])
    for (KeyGene_clusters in seq(q)) {
      prediction <- rownames(prediction_hs[which(prediction_hs[,1] == as.character(KeyGene_clusters)),])
      precision <- length(which(prediction %in% real))/length(Seurat_prediction)
      temp_diff <- c(temp_diff, precision)
      # print(paste0(temp_diff))
    }
    comparison_result[original_clusters,2] <- max(temp_diff)
  }
  return(comparison_result)
}


#=========================================================================================#
# Real codes
#=========================================================================================#

# Global parameters
nbt = 1
q = 9

# Preprocessing
files <- file.path("quants_mat.gz")
txi <- tximport(files, type="alevin")

pbmc <- CreateSeuratObject(counts=txi$counts, min.cells=3, min.features=200, project="10X_PBMC")
pbmc[["percent.mt"]] <- PercentageFeatureSet(pbmc, pattern = "^MT-")
pbmc <- subset(pbmc, subset = nFeature_RNA > 200 & nFeature_RNA < 4000 & percent.mt < 10)
pbmc <- NormalizeData(pbmc, normalization.method="LogNormalize", scale.factor=10000)
pbmc <- FindVariableFeatures(pbmc, selection.method="vst", nfeatures=2000)

all.genes <- rownames(pbmc)
pbmc <- ScaleData(pbmc, features=all.genes)
exprs <- as.matrix(GetAssayData(object=pbmc, slot="counts"))

Input <- t(exprs) # data matrix, cells in rows, genes in columns

original_hierarchical_structre <- hierarchical_structre(Input,nbt = nbt, q = q)

#===============================================================================================================================#
# Seurat FindMarkers as the marker finder
de <- find_diff_genes(pbmc,hierarchical_graph,hs)
Seurat_markers <- unique(as.character(unlist(de[[1]])))

## this function will return to you the hierarchical structure 
Seurat_hierarchical_structre <- hierarchical_structre(Input[,Seurat_markers],nbt = nbt, q = q)

## performance
Seurat_performance_validation <- performance_validation(original_hierarchical_structre = original_hierarchical_structre,
                                                        prediction_hierarchical_structre = Seurat_hierarchical_structre)
Seurat_performance_validation
#===============================================================================================================================#
# Monocle as the marker finder
Monocle_markers <- as.vector(t(read.table("Monocle_markers", sep = ",")[1,]))

## this function will return to you the igraph hierarchical structure
Monocle_hierarchical_structre <- hierarchical_structre(Input[,Monocle_markers],nbt = nbt, q = q)

## performance
Monocle_performance_validation <- performance_validation(original_hierarchical_structre = original_hierarchical_structre,
                                                        prediction_hierarchical_structre = Monocle_hierarchical_structre)
Monocle_performance_validation







