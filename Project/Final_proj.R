library(Seurat)
library(tximport)
library(pcaReduce)
library(igraph)
library(dplyr)
library(Rtsne)
library(ggplot2)
library(monocle)

nbt=1
q=9

setwd("CMSC858D/Project/")
files <- file.path("full_em/alevin/quants_mat.gz")
file.exists(files)

txi <- tximport(files, type="alevin")

pbmc <- CreateSeuratObject(counts=txi$counts, min.cells=3, min.features=200, project="10X_PBMC")
pbmc[["percent.mt"]] <- PercentageFeatureSet(pbmc, pattern="^MT-")
pbmc <- subset(pbmc, subset=nFeature_RNA > 200 & nFeature_RNA < 4000 & percent.mt < 10)
pbmc <- NormalizeData(pbmc, normalization.method="LogNormalize", scale.factor=10000)
pbmc <- FindVariableFeatures(pbmc, selection.method="vst", nfeatures=2000)

all.genes <- rownames(pbmc)
pbmc <- ScaleData(pbmc, features=all.genes)
exprs <- as.matrix(GetAssayData(object=pbmc, slot="counts"))

Input <- t(exprs) # data matrix, cells in rows, genes in columns
exprsMTX <- exprs # data matrix for k-means clustering

#====RUN K-means clustering=====================================
exprsMTX.Z <- sweep(exprsMTX,1,apply(exprsMTX,1,mean),"-")
indx.sd <- (apply(exprsMTX,1,sd))==0 # these will produce NAs
exprsMTX.Z <- sweep(exprsMTX.Z,1,apply(exprsMTX.Z,1,sd),"/")
exprsMTX.Z[indx.sd,] <- 0
if(sum(is.na(exprsMTX.Z))!=0){print("NAs in exprsMTX.Z Zscores!")}

wss <- (nrow(exprsMTX.Z)-1)*sum(apply(exprsMTX.Z,2,var))
for (i in 2:30) wss[i] <- sum(kmeans(exprsMTX.Z, centers=i)$withinss)

pdf("pdf/Elbow.pdf")
plot(1:30, wss, type="l", lty=1,
     xlab="Number of Clusters",
     ylab="Within groups sum of squares (wss)") 
points(1:30, wss, pch=19, cex=0.7)
abline(v=10, col="purple", lty=2)
dev.off()

#====RUN pcaReduce==============================================
Output_S <- PCAreduce(Input, nbt=nbt, q=q, method='S')
# will produce a list, where each element in the list is a matrix/sample
# (i.e. we will have 100 runs of pcaReduce algorithm, where merging was achieved based on sampling);
# each row in each sample matrix corresponds to a clustering; first row contains data partition into K=q+1 clusters, and last row will contain K=2 clusters.
# 
Output_M <- PCAreduce(Input, nbt=nbt, q=q, method='M')
# output is similar list, however the merging was achieved based on largest probability value.
save.image(file="PCArecude_result.RData")
load(file="PCArecude_result.RData")

# get the hierarchical structure of the data from PCAReduce
hs <- Output_M[[1]]

# Since there are redundant patterns, so we just take the unique pattern
hs_unique <- unique(hs)[,seq(q,1)]

# PCA reduce stops at K = 2, so we need to create a common ancestor by ourself
hs_unique <- cbind("root"=rep(1,nrow(hs_unique)), (hs_unique))

# Since in each K iteration, the cluster order starts from 1, 
# so we need to identify the clusters in each iteration, 
# I name it as Level `K` _ (# of cluster)
# for example, Level1_1, Level 31_1

## First step is build up a exmpty matrix
hs_unique_label <- matrix(NA, nrow=nrow(hs_unique), ncol=0)

## for each column(K), get the cluster labels for this column and combine it as a matrix.
for (cols in seq(nrow(hs_unique))) {
  hs_unique_label <- cbind(hs_unique_label, paste0("Lv", cols, "_", hs_unique[,cols]))
}

# build the hierarchical graph using igraph package

## First, get a empty graph with all nodes(with the same size of hs_unique_label
hierarchical_graph <- igraph::graph.empty(n=length(unique(c(hs_unique_label))), directed=TRUE)

# Second, change the node names in the graph
V(hierarchical_graph)$name <- unique(c(hs_unique_label))

# Third, assign the edges according to the hierarchical structure we get
for (i in seq(nrow(hs_unique_label))) {
  edge_path <- unique(hs_unique_label[i,])
  edge_path <- edge_path[c(1, rep(seq(2, length(edge_path)-1), each=2), length(edge_path))]
  hierarchical_graph = add_edges(graph=hierarchical_graph, edge_path)
}
hierarchical_graph <- simplify(graph=hierarchical_graph)

# Plot it you can see that there are a bunch of redundant nodes, which ar ethe linear paths in the graph

plot(hierarchical_graph, layout=layout_as_tree, vertex.label.color="black", vertex.label.dist=1,
     vertex.size=2, edge.arrow.size=0.1, vertex.label="")

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
  if(degree(graph=hierarchical_graph, v=current_node, mode="out")==1 &
     degree(graph=hierarchical_graph, v=current_node, mode="in")==1){
    hierarchical_graph <- hierarchical_graph+edge(neighbors(graph=hierarchical_graph, v=current_node, mode="in")$name, neighbors(graph=hierarchical_graph, v=current_node, mode="out")$name)
    hierarchical_graph <- hierarchical_graph-current_node
  }
}

# Now we updated the node names of the graph, next we need to update the graph
hierarchical_graph <- graph_from_data_frame(igraph::as_data_frame(hierarchical_graph)) %>% simplify

write.csv(as_data_frame(hierarchical_graph), file="pbmc4K_edgelist", quote=FALSE)
# Here is the result!

# Query the hierarchical structure 
plot(hierarchical_graph, layout=layout_as_tree, vertex.label.color="black", vertex.label.dist=0,
     vertex.size=15, edge.arrow.size=0.1, vertex.label.cex=0.5)

# Query the node names
V(hierarchical_graph)$name

# Query the edge information
E(hierarchical_graph)


# Query the cells included in a node's children, it will be 2 matrice included in a list, each matrix
# is a exprs matrix of a subpopulation. 
# For example, the cluster Level1_1 has two children clusters, Level2_1 and Level3_2, 
# the function will return the exprs of cells in the cluster Level2_1 as a matrix, 
# and the exprs of cells in the cluster Level3_2.

find_children_exprs <- function(node_name, hierarchical_graph, hs){
  # Returns the exprs matrice of the node's two children population
  exprs_list <- list()
  children <- neighbors(graph=hierarchical_graph, v=node_name, mode="out")$name
  for (ichild_index in seq(length(children))) {
    ichild <- children[ichild_index]
    ichild_children <- names(bfs(graph=hierarchical_graph, root=ichild, neimode="out", order=TRUE, unreachable=FALSE)$order)
    ichild_leaves <- ichild_children[grep(paste0("Lv", q+1), ichild_children)]
    involved_leave <- sapply(strsplit(ichild_leaves, paste0("Lv", q+1, "_")), function(x) x[2])
    exprs_list[[ichild]] <- exprs[,which(hs[,1] %in% involved_leave)]
  }
  return(exprs_list)
}

#====Draw t-SNE plot============================================
set.seed(10)

norm_0_1 <- function(x) {(x-min(x))/(max(x)-min(x))}
t_tsne <- Rtsne(t(exprsMTX), dim=2, perplexity=10, check_duplicates=FALSE)

# set a target gene
gene <- "LILRA4"

pd <- data.frame(hs[,1])
colnames(pd) <- c("Cluster")
pd$colors <- ifelse(pd$Cluster==1, "blue",
                    ifelse(pd$Cluster==2, "yellow",
                           ifelse(pd$Cluster==3, "green",
                                  ifelse(pd$Cluster==4, "black",
                                         ifelse(pd$Cluster==5, "orange",
                                                ifelse(pd$Cluster==6, "red",
                                                       ifelse(pd$Cluster==7, "purple",
                                                              ifelse(pd$Cluster==8, "pink",
                                                                     ifelse(pd$Cluster==9, "grey", "lightblue"))))))))) 

pd$size <- norm_0_1(exprsMTX[which(rownames(exprsMTX)==gene),])
pd$gradient <- round(pd$size*1000,0)+1
pd$gradient_cols <- gradient_cols[match(pd$gradient, gradient_cols$number),1]

# t-SNE plot for 10 clusters
pdf("pdf/tSNE_all.pdf")
plot(t_tsne$Y, pch=19, col=pd$colors,
     cex=0.5, main=paste0("TSNE of 10 Clusters"),
     xlab=paste0("t-SNE 1"), 
     ylab=paste0("t-SNE 2"))
legend("topright", paste0(c("Cluster 1", "Cluster 2", "Cluster 3", "Cluster 4", "Cluster 5",
                            "Cluster 6", "Cluster 7", "Cluster 8", "Cluster 9", "Cluster 10")),
       col=c("blue", "yellow", "green", "black", "orange",
             "red", "purple", "pink", "grey", "lightblue"),
       pch=c(rep(16, 10)), cex=0.6, pt.cex=0.6, bty="n")
dev.off()

colfunc <- colorRampPalette(c("grey", "red"))
gradient_cols <- data.frame(colfunc(1001))
gradient_cols$number <- rownames(gradient_cols)
y <- cbind(1:1001)

# t-SNE plot with marker gene expression
pdf(paste0("pdf/tSNE_",gene,".pdf"))
plot(t_tsne$Y, pch=19, col=adjustcolor(pd$gradient_cols, alpha.f=0.5),
     cex=0.7, main=paste0("TSNE (",gene,")"),
     xlab=paste0("t-SNE 1"), 
     ylab=paste0("t-SNE 2"))
dev.off()

#====RUN Seurat=================================================

find_diff_genes <- function(pbmc, hierarchical_graph, hs){
  set.seed(10)
  queue <- c("Lv1_1")
  marker <- list()
  parent <- unique(ends(hierarchical_graph, E(hierarchical_graph))[,1])
  while (length(queue)>0){
    node <- queue[1]
    if (node %in% parent){
      #----------find differentially expressed genes------
      child_list <- find_children_exprs(node_name=node, hierarchical_graph=hierarchical_graph, hs=hs)
      c1.name <- names(child_list)[1]
      c2.name <- names(child_list)[2]
      message(paste0('Comparing', c1.name, c2.name))
      c1 <- child_list[[c1.name]]
      c2 <- child_list[[c2.name]]
      pbmc <- SetIdent(object=pbmc, cells=colnames(c1), value=c1.name)
      pbmc <- SetIdent(object=pbmc, cells=colnames(c2), value=c2.name)
      pbmc.markers <- FindMarkers(pbmc, ident.1=c1.name, ident.2=c2.name, min.pct=0.25)
      pbmc.markers <- pbmc.markers[pbmc.markers$p_val_adj < 0.01,]
      if (log2(length(child_list))>5){
        n <- log2(length(child_list))
      } else{n <- 5}
      top.c1 <- row.names(pbmc.markers[order(pbmc.markers$avg_logFC, decreasing=T),])[1:n]
      top.c2 <- row.names(pbmc.markers[order(pbmc.markers$avg_logFC),])[1:n]
      marker[[c1.name]] <- top.c1
      marker[[c2.name]] <- top.c2
      queue <- c(queue[-1], c1.name, c2.name)
      
      #-----------generate plots--------------
      png(paste0('pdf/', c1.name, '_', 'vlnplot.png'))
      pic=VlnPlot(pbmc, features=marker[[c1.name]][1])
      print(pic)
      dev.off()
      
      png(paste0('pdf/', c2.name, '_', 'vlnplot.png'))
      pic=VlnPlot(pbmc, features=marker[[c2.name]][1])
      print(pic)
      dev.off()
      
      features <- unique(as.character(unlist(marker)))
      exp <- rbind(t(c1[features,]), rbind(t(c2[features,])))
      tsne <- Rtsne(exp, perplexity=10, check_duplicates=FALSE)
      cluster <- as.factor(c(rep(c1.name, ncol(c1)), rep(c2.name, ncol(c2))))
      tsne.df <- as.data.frame(tsne$Y)
      tsne.df$cluster <- cluster
      png(paste0('pdf/', c1.name, '_', c2.name, '_tsne2.png'))
      pic <- ggplot(tsne.df, aes(x=V1, y=V2, color=cluster)) +
        geom_point(size=1) +
        labs(title=paste0(c1.name,' vs ', c2.name), x='tSNE_1', y='tSNE_2') + 
        theme(axis.line=element_line(colour="black"),
              panel.grid.major=element_blank(),
              panel.grid.minor=element_blank(),
              panel.border=element_blank(),
              panel.background=element_blank(),
              legend.text=element_text(size=20),
              axis.text.x=element_text(size=20),
              axis.text.y=element_text(size=20),
              axis.title=element_text(size=20),
              plot.title=element_text(size=20, face='bold', hjust=0.5),
              legend.title=element_text(size=20)) 
      print(pic)
      dev.off()
      
      pbmc <- RunPCA(pbmc, features=features)
      pbmc <- RunTSNE(pbmc, check_duplicates=FALSE)
      
      png(paste0('pdf/', c1.name,'_', c2.name, '_dimplot.png'))
      pic <- DimPlot(pbmc, reduction="tsne") + 
        theme(legend.text=element_text(size=20),
              axis.text.x=element_text(size=20),
              axis.text.y=element_text(size=20),
              axis.title=element_text(size=20))
      print(pic)
      dev.off()
      
      png(paste0('pdf/', c1.name, '_', c2.name, '_featureplot.png'), width=960)
      pic <- FeaturePlot(pbmc, features=c(marker[[c1.name]][1], marker[[c2.name]][1]), combine=FALSE)
      pic <- lapply(X=pic, FUN=function(x) x + theme(plot.title=element_text(size=20),
                                                     legend.text=element_text(size=15),
                                                     axis.text.x=element_text(size=20),
                                                     axis.text.y=element_text(size=20),
                                                     axis.title=element_text(size=20)))
      pic <- CombinePlots(plots=pic)
      print(pic)
      dev.off()
    } else{queue <- c(queue[-1])}
  }
  return(list(marker, pbmc))
}

de <- find_diff_genes(pbmc, hierarchical_graph, hs)
markers <- unique(as.character(unlist(de[[1]])))
pbmc.new <- de[[2]]


#====RUN Monocle================================================
markerGeneDetection_monocle <- function(num_genes){
  hs_matrix <- as.matrix(hs)
  cluster_number <- length(colnames(hs_matrix))
  colnames(hs_matrix) <- paste0("level",as.character(c(cluster_number:1)))
  
  # count matrix in use
  txi_used <- txi$counts[,rownames(hs_matrix)]
  
  # if we use 10 as the cluster number
  for (i in 1:cluster_number) {
    # samplesheet:
    print(paste0("Level:",i))
    if (i>1) {
      new_cluster <- i+1
      new_index <- which(hs_matrix[,paste0("level",i)]==i+1)
      upper_level <- hs_matrix[new_index[1], paste0('level', i-1)]
      sample_idx <- which(hs_matrix[,paste0("level", i)] %in% c(new_cluster, upper_level))
      sample_idx <- rownames(hs_matrix)[sample_idx]
    } else {
      sample_idx <- rownames(hs_matrix)
    }
    
    sample_sheet <- matrix(data=paste0("cluster", as.character(c(hs_matrix[sample_idx, paste0('level',i)]))), nrow=length(sample_idx))
    rownames(sample_sheet) <- sample_idx
    colnames(sample_sheet) <- paste0("level",i)
    
    # expr matrix
    expr_matrix <- txi_used[,sample_idx]
    
    # gene annotation/feature data
    gene_annotation <- matrix(data=rownames(txi_used), nrow=length(rownames(txi_used)))
    rownames(gene_annotation) <- rownames(txi_used)
    colnames(gene_annotation) <- c("gene_short_name")
    gene_annotation <- as.data.frame(gene_annotation)
    
    # Differential expression
    # CellDataSet objects
    pd_mon <- new("AnnotatedDataFrame", data=as.data.frame(sample_sheet))
    fd_mon <- new("AnnotatedDataFrame", data=gene_annotation)

    # Sparse?
    HSMM <- newCellDataSet(as(expr_matrix,"sparseMatrix"), phenoData=pd_mon, featureData=fd_mon, lowerDetectionLimit=0.1, expressionFamily=negbinomial.size())
    
    # Data QC?
    HSMM <- detectGenes(HSMM, min_expr=0.1)
    expressed_genes <- row.names(subset(fData(HSMM), num_cells_expressed >= 10))
    HSMM <- HSMM[expressed_genes,]
    HSMM <- estimateSizeFactors(HSMM)
    HSMM <- estimateDispersions(HSMM)

    # original pic
    disp_table <- dispersionTable(HSMM)
    HSMM <- reduceDimension(HSMM, max_components=2, num_dim=6, reduction_method='tSNE', verbose=T)
    HSMM <- clusterCells(HSMM, num_clusters=2)

    png(paste0("pdf/level",i,"_original.png"), res=150, width=7, height=7, units="in")
    pl1 <- plot_cell_clusters(HSMM, 1, 2, color=paste0("level",i))
    print(pl1)
    dev.off()
    
    # Marker gene test
    diff_test_res <- differentialGeneTest(HSMM, fullModelFormulaStr=paste0("~level",i))
    diff_test_res[,c("gene_short_name", "pval", "qval")]
    diff_test_res1 <- diff_test_res[order(diff_test_res$pval, diff_test_res$num_cells_expressed, decreasing = c(FALSE,TRUE)),]

    diff_test_res1 <- diff_test_res1[1:num_genes,] #get top 10
    sig_gene_names <- rownames(diff_test_res1)
    HSMM2 <- reduceDimension(HSMM[sig_gene_names,], max_components=2, num_dim=6, reduction_method='tSNE', verbose=T, check_duplicates=FALSE)
    HSMM2 <- clusterCells(HSMM2, num_clusters=2)
    
    p <- plot_cell_clusters(HSMM2, 1, 2, color=paste0("level",i))
    png(paste0("pdf/level",i,".png"), res=150, width=7, height=7, units="in")
    print(p)
    dev.off()
  }
  
}

markerGeneDetection_monocle(10)

