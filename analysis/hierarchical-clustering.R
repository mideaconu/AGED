#
# Hierarchical Clustering analysis of RNA-seq Alzheimer's Disease data
#

library(gplots)
library(data.table)
library(devtools)

# Import the heatmap method from source

source_url("https://raw.githubusercontent.com/obigriffith/biostar-tutorials/master/Heatmaps/heatmap.3.R")

data <- read.csv("data/log_expression.csv", row.names=1, check.names=FALSE)
data <- data.frame(data)

genes <- head(rownames(data), -5)

t <- transpose(data)

colnames(t) <- rownames(data)
rownames(t) <- colnames(data)

# Transform the label values into colours for the heatmap key

tissue <- unlist(lapply(t$Tissue, function(x) { if (x=="Cerebellum") "yellow" else "forestgreen" }))
diagnosis <- unlist(lapply(t$Diagnosis, function(x) { if (x=="AD") "red3" else if (x=="PSP") "slateblue3" else if (x=="Control") "cyan2" else "darkorange" }))
gender <- unlist(lapply(t$Gender, function(x) { if (x=="M") "dodgerblue3" else "lightpink" }))
age_at_death <- unlist(lapply(t$AgeAtDeath, function(x) { if (x=="40-50") "gray94" else if (x=="50-60") "gray88" else if (x=="60-70") "gray82" else if (x=="70-80") "gray61" else if (x=="80-90") "gray36" else "gray15" }))

clab = cbind(tissue, gender, diagnosis, age_at_death)

data <- head(data, -5)
data <- apply(as.matrix(data), 2, as.numeric)
rownames(data) <- genes

# Plot the heatmap

par(xpd=TRUE)
heatmap.3(data, scale="row", col=redgreen(75), margins=c(4,7), trace="none", density.info="density", Rowv=TRUE, Colv=TRUE, labCol=colnames(data), labRow=rownames(data), symbreaks=FALSE, key=TRUE, ColSideColors=clab, ColSideColorsSize=3, cexRow=0.8, cexCol=0.2)
dev.off()
